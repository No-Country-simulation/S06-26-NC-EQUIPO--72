import logging
import json
import re
import httpx
import aiomysql
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from openai import RateLimitError
from app.core.config import settings
from app.agent.retry import http_retry
from app.agent.security import validar_endpoint, filtrar_params, envolver_consulta

logger = logging.getLogger(__name__)


# Claves de resultado conocidas del backend (orden importa- más específica primero)
_CLAVES_RESULTADO = ("brechas", "evolucion", "programas", "regiones")

# Tablas conocidas del esquema (only-read). Cualquier tabla fuera de esta lista
# referenciada en el SQL generado por el LLM se rechaza (exfiltración).
# `dual` es la pseudo-tabla de MySQL (SELECT 1) — inofensiva.
_TABLAS_PERMITIDAS = frozenset({
    "concentracao", "mobilidade_agregada", "mobilidade",
    "flujo_od", "fluxo_vias", "indicadores_territoriales", "dual",
})

# Keywords que anulan el SQL completo. Se verifica por substring case-insensitive
# sobre el SQL en mayúsculas (defensa en capas, no única).
_KEYWORDS_PELIGROSAS = (
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "UNION", "INTO OUTFILE", "INTO DUMPFILE", "LOAD_FILE", "SLEEP",
    "INFORMATION_SCHEMA", "@@", "/*",
)


@http_retry(max_attempts=settings.max_retries_tool + 1)
async def _do_request(metodo: str, url: str, params: dict) -> dict:
    """
    Ejecuta el HTTP request con retry tenacity sobre errores transitorios
    (red / 5xx). Devuelve el JSON parseado.
    """
    async with httpx.AsyncClient() as client:
        if metodo == "GET":
            response = await client.get(url, params=params, timeout=10.0)
        else:
            response = await client.post(url, json=params, timeout=10.0)
        response.raise_for_status()
        return response.json()


def _limpiar_sql(raw: str) -> str:
    cleaned = re.sub(r"```(?:sql)?\s*", "", raw).strip()
    return cleaned


def _limitar_filas(sql: str, request_id: str, max_filas: int = 50) -> str:
    """
    Garantiza LIMIT siempre presente y acotado:
    - Si no hay LIMIT, agrega LIMIT {max_filas}.
    - Si hay LIMIT N con N > max_filas, lo reescribe a LIMIT {max_filas}
      (el modelo inducido puede emitir LIMIT 1000000 para exfiltrar).
    - Si hay LIMIT N con N <= max_filas, no lo toca.
    """
    limite = re.search(r"\blimit\s+(\d+)\s*;?\s*$", sql, re.IGNORECASE)
    if limite:
        n = int(limite.group(1))
        if n > max_filas:
            logger.warning(
                "[%s] SQL | LIMIT %d excede el máximo- reescribiendo a LIMIT %d",
                request_id, n, max_filas
            )
            base = sql[:limite.start()].rstrip(" \n\t;")
            return f"{base} LIMIT {max_filas}"
        return sql
    logger.warning("[%s] SQL sin LIMIT- agregando LIMIT %d", request_id, max_filas)
    return sql.rstrip(";") + f" LIMIT {max_filas}"


def _tablas_uso(sql: str) -> list[str]:
    """Extrae los nombres de tabla referenciados en FROM/JOIN (con prefijo opcional)."""
    tablas = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)",
        sql,
        re.IGNORECASE,
    )
    # Quitar el prefijo de esquema (p.ej. "db.concentracao" -> "concentracao")
    return [t.split(".")[-1] for t in tablas]


def _where_filtra_fecha(sql: str) -> bool:
    """
    True si la cláusula WHERE (hasta el LIMIT o el final) filtra day_date.
    Busca en el segmento WHERE real, no en todo el SQL: un substring
    de "day_date" en otra posición (p.ej. dentro de un SELECT) no se considera
    filtro de fecha, así el full-scan guard no se puede engañar con eso.
    """
    m_where = re.search(r"\bWHERE\b", sql, re.IGNORECASE)
    if not m_where:
        return False
    m_limit = re.search(r"\bLIMIT\b", sql, re.IGNORECASE)
    fin = m_limit.start() if m_limit else len(sql)
    clausula_where = sql[m_where.start():fin]
    return "day_date" in clausula_where.lower()


def _sanitizar_sql(sql: str, request_id: str) -> str | None:
    """
    Validación de seguridad del SQL generado por el LLM.
    Devuelve el SQL saneado, o None si es inseguro (abortar sin ejecutar).

    Checks (defensa en profundidad, ninguno es la única barrera):
    1. Debe empezar con SELECT.
    2. Sin multi-statement (punto y coma seguido de más contenido).
    3. Sin keywords peligrosas (substring case-insensitive).
    4. Tablas referenciadas solo dentro de la allowlist.
    5. LIMIT siempre presente y <= 50.
    6. Full scan en tablas grandes requiere filtro de fecha en el WHERE real.
    """
    sql_upper = sql.upper()

    # 1. Solo SELECT
    if not sql_upper.startswith("SELECT"):
        logger.warning("[%s] SQL generado no es SELECT - abortando: %s", request_id, sql)
        return None

    # 2. Multi-statement: ";" seguido de más contenido (no solo el final).
    if re.search(r";\s*\S", sql):
        logger.warning("[%s] SQL multi-statement - abortando: %s", request_id, sql)
        return None

    # 3. Keywords peligrosas
    for keyword in _KEYWORDS_PELIGROSAS:
        if keyword in sql_upper:
            logger.warning(
                "[%s] SQL contiene keyword peligroso '%s' - abortando.",
                request_id, keyword
            )
            return None

    # 4. Tablas dentro de la allowlist (exfiltración de tablas arbitrarias).
    for tabla in _tablas_uso(sql):
        if tabla not in _TABLAS_PERMITIDAS:
            logger.warning(
                "[%s] SQL referencia tabla fuera de allowlist '%s' - abortando: %s",
                request_id, tabla, sql
            )
            return None

    # 5. LIMIT acotado (después de los checks, para operar sobre SQL confiable).
    sql = _limitar_filas(sql, request_id)

    # 6. Full scan en tablas grandes: sin filtro de fecha en el WHERE real,
    #    agregar filtro por el día más reciente (evita barrer el histórico).
    #    Bug previo: se comparaba "where" (minúscula) contra sql_upper
    #    (MAYÚSCULA) -> nunca matcheaba -> el guard disparaba SIEMPRE y
    #    duplicaba el filtro de fecha -> syntax error 1064 (eval_028).
    _TABLAS_GRANDES = ("concentracao", "mobilidade_agregada")
    for tabla in _TABLAS_GRANDES:
        if tabla in sql.lower():
            tiene_where = re.search(r"\bWHERE\b", sql, re.IGNORECASE) is not None
            filtra_fecha = _where_filtra_fecha(sql)
            if not tiene_where or not filtra_fecha:
                logger.warning(
                    "[%s] Full scan en tabla grande '%s'- agregando filtro de fecha",
                    request_id, tabla
                )
                cond = f"{tabla}.day_date = (SELECT MAX(day_date) FROM {tabla})"
                conector = " AND " if tiene_where else " WHERE "
                # WHERE/AND después de LIMIT es syntax error. El LIMIT puede
                # venir con salto de línea ("LIMIT\n50")- regex tolera
                # cualquier whitespace y el punto y coma final.
                limite = re.search(r"\blimit\s+(\d+)\s*;?\s*$", sql, re.IGNORECASE)
                if limite:
                    base = sql[:limite.start()].rstrip(" \n\t;")
                    sql = f"{base}{conector}{cond} LIMIT {limite.group(1)}"
                else:
                    base = sql.rstrip(" \n\t;")
                    sql = f"{base}{conector}{cond} LIMIT 50"
                break

    return sql


TEXT_TO_SQL_PROMPT = """
Usa SQL profesional. Genera una consulta SQL de solo lectura (SELECT) para MySQL.

Schema disponible:
{schema}

## Filtros ya resueltos (usar estos valores EXACTOS en el WHERE, no reinterpretar la consulta)
{filtros}

Si un filtro es null, no lo incluyas en el WHERE. Si el filtro `municipio` o `cluster`
tiene un valor, usalo tal cual está escrito arriba- ya fue validado contra la lista
oficial de municipios/clusters, así que no intentes corregirlo ni interpretarlo de la
consulta en lenguaje natural.

Reglas:
- Solo SELECT, nunca INSERT/UPDATE/DELETE/DROP
- Limita los resultados a 50 filas máximo con LIMIT 50
- Usa alias claros en español cuando sea posible
- Responde SOLO con el SQL, sin explicaciones ni markdown

## Regla crítica sobre fechas (day_date)
Si la tabla tiene columna `day_date` y no hay un filtro de fecha explícito arriba,
NUNCA agregues (SUM, COUNT, AVG) sobre todos los días históricos disponibles.
En su lugar, filtrá siempre por el día más reciente:

    WHERE day_date = (SELECT MAX(day_date) FROM <misma_tabla>)

Consulta original del usuario (solo como contexto para entender la intención,
no para extraer nombres de zonas/municipios- usá los filtros de arriba para eso):
{consulta}
"""

async def llamar_endpoint(metodo: str, endpoint: str, params: dict, request_id: str = "-") -> dict:
    """
    Llama a un endpoint del backend y retorna los datos crudos.
    Los errores transitorios se reintentan en _do_request (tenacity);
    tras agotar intentos se degrada a lista vacía sin romper el pipeline.
    """
    # Security el endpoint y params pueden venir del LLM
    # (decomposer/react_reasoner) y ser manipulados por prompt injection.
    # Allowlist determinística fuera del control del modelo.
    if not validar_endpoint(endpoint, request_id):
        return {
            "resultado": [],
            "fuentes": [],
            "error": f"endpoint '{endpoint}' no permitido",
        }
    params = filtrar_params(endpoint, params, request_id)
    url = f"{settings.backend_url}{endpoint}"

    try:
        data = await _do_request(metodo, url, params)

        # for/else garantiza que listas vacías se traten como listas vacías,
        # no como falsy que cae al dict completo. Si el backend devuelve un
        # array en el top-level (como /programas), no matchea ninguna clave
        # y se usa el array completo.
        resultado = None
        for key in _CLAVES_RESULTADO:
            if isinstance(data, dict) and key in data:
                resultado = data[key]
                break
        if resultado is None:
            resultado = data

        # Normalizar SIEMPRE a lista- el resto del pipeline asume list[dict]
        if isinstance(resultado, dict):
            resultado = [resultado] if resultado else []
        elif not isinstance(resultado, list):
            resultado = []

        fuentes = [{"nombre": "Backend AppBiT", "endpoint": endpoint}]
        return {"resultado": resultado, "fuentes": fuentes}

    except httpx.HTTPStatusError as e:
        logger.warning("[%s] HTTP %s en %s- %s", request_id,
                       e.response.status_code, endpoint, e)
        return {"resultado": [], "fuentes": []}
    except httpx.HTTPError as e:
        logger.warning("[%s] Error de red en %s- %s", request_id, endpoint, e)
        return {"resultado": [], "fuentes": []}


async def ejecutar_sql(
    consulta: str,
    schema_minimo: str,
    model: ChatOpenAI | None = None,
    fecha: str | None = None,
    filtros: dict | None = None,
    request_id: str = "-",
    model_alt: ChatOpenAI | None = None,
    modelos: list[ChatOpenAI] | None = None,
    model_fallback: ChatOpenAI | None = None,
) -> dict:
    """
    Genera SQL con el modelo primary y lo ejecuta contra MySQL (solo SELECT).
    Ante rate-limit 429 (TPM/TPD) rota a la siguiente cuenta del pool
    (`modelos` = una instancia por cuenta Groq, o `model`/`model_alt`) y, si
    todas agotan, usa model_fallback (pool de límites separado, Gemini).
    """
    filtros = filtros or {}
    if fecha:
        filtros = {**filtros, "fecha": fecha}

    filtros_relevantes = {k: v for k, v in filtros.items() if v is not None}
    filtros_texto = json.dumps(filtros_relevantes, ensure_ascii=False) if filtros_relevantes else "(ninguno)"

    # 1. Genera el SQL
    prompt = TEXT_TO_SQL_PROMPT.format(
        schema=schema_minimo,
        consulta=consulta,
        filtros=filtros_texto,
    )
    if modelos:
        cadena = list(modelos)
    else:
        cadena = [model] + ([model_alt] if model_alt else [])
    cadena = [m for m in cadena if m is not None]
    response = None
    for m in cadena:
        try:
            response = await m.ainvoke([
                SystemMessage(content=prompt),
                HumanMessage(content=envolver_consulta(consulta))
            ])
            break
        except RateLimitError:
            logger.warning("[%s] SQL | rate limit en %s- probando siguiente cuenta Groq",
                           request_id, m.model_name)
    if response is None:
        if model_fallback is None:
            raise RuntimeError("sin modelos válidos para SQL")
        logger.warning("[%s] SQL | todas las cuentas Groq rate-limit - fallback a %s",
                       request_id, model_fallback.model_name)
        response = await model_fallback.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content=envolver_consulta(consulta))
        ])
    
    sql = _limpiar_sql(response.content.strip())

    logger.debug("[%s] SQL generado por el agente:\n%s", request_id, sql)

    # --- Validación de seguridad  ---
    sql = _sanitizar_sql(sql, request_id)
    if sql is None:
        return {"resultado": [], "fuentes": []}

    # 2. Ejecuta el SQL
    try:
        conn = await aiomysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            db=settings.db_name,
            user=settings.db_readonly_user,
            password=settings.db_readonly_password.get_secret_value(),
        )
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            rows = await cur.fetchall()
        conn.close()

        rows = list(rows) if rows else []
        logger.info("[%s] SQL ejecutado OK - %d filas obtenidas.", request_id, len(rows))
        logger.debug("[%s] SQL resultado (primeras 10): %s",
                     request_id, [dict(r) for r in rows[:10]])

        fuentes = [{"nombre": "Vísent CDRView v2", "codigo_origem": "text_to_sql"}]
        return {"resultado": rows, "fuentes": fuentes}

    except Exception as e:
        logger.exception("[%s] Error ejecutando SQL: %s", request_id, sql)
        return {"resultado": [], "fuentes": []}