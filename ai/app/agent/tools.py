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

logger = logging.getLogger(__name__)


# Claves de resultado conocidas del backend (orden importa- más específica primero)
_CLAVES_RESULTADO = ("brechas", "evolucion", "programas", "regiones")


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
    model: ChatOpenAI,
    fecha: str | None = None,
    filtros: dict | None = None,
    request_id: str = "-",
    model_fallback: ChatOpenAI | None = None,
) -> dict:
    """
    Genera SQL con el modelo primary y lo ejecuta contra MySQL (solo SELECT).
    Si el modelo primary rate-limita (429 TPM/TPD), usa model_fallback (pool
    de límites separado) en vez de esperar el rate-limit.
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
    try:
        response = await model.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content=consulta)
        ])
    except RateLimitError:
        if model_fallback is None:
            raise
        logger.warning("[%s] SQL | rate limit en %s- fallback a %s",
                       request_id, model.model_name, model_fallback.model_name)
        response = await model_fallback.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content=consulta)
        ])
    
    sql = _limpiar_sql(response.content.strip())

    logger.debug("[%s] SQL generado por el agente:\n%s", request_id, sql)

    # Validación mínima de seguridad
    sql_upper = sql.upper()
    if not sql_upper.startswith("SELECT"):
        logger.warning("[%s] SQL generado no es SELECT - abortando: %s", request_id, sql)
        return {"resultado": [], "fuentes": []}

    for keyword in ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"):
        if keyword in sql_upper:
            logger.warning("[%s] SQL contiene keyword peligroso '%s' - abortando.", request_id, keyword)
            return {"resultado": [], "fuentes": []}

    # validación SQL reforzada
    # Garantizar LIMIT
    if "LIMIT" not in sql_upper:
        logger.warning("[%s] SQL sin LIMIT- agregando LIMIT 50", request_id)
        sql = sql.rstrip(";") + " LIMIT 50"

    # Prevenir full scan en tablas grandes: solo si falta WHERE o si el WHERE
    # no filtra day_date. Bug previo: se comparaba "where" (minúscula) contra
    # sql_upper (MAYÚSCULA) -> nunca matcheaba -> el guard disparaba SIEMPRE y
    # duplicaba el filtro de fecha -> syntax error 1064 (eval_028).
    _TABLAS_GRANDES = ("concentracao", "mobilidade_agregada")
    for tabla in _TABLAS_GRANDES:
        if tabla in sql.lower():
            tiene_where = "WHERE" in sql_upper
            filtra_fecha = "day_date" in sql.lower()
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