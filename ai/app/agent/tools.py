import logging
import re
import httpx
import aiomysql
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings

logger = logging.getLogger(__name__)


def _limpiar_sql(raw: str) -> str:
    cleaned = re.sub(r"```(?:sql)?\s*", "", raw).strip()
    return cleaned


TEXT_TO_SQL_PROMPT = """
Usa SQL profesional. Genera una consulta SQL de solo lectura (SELECT) para MySQL.

Schema disponible:
{schema}

Reglas:
- Solo SELECT, nunca INSERT/UPDATE/DELETE/DROP
- Limita los resultados a 50 filas máximo con LIMIT 50
- Usa alias claros en español cuando sea posible
- Responde SOLO con el SQL, sin explicaciones ni markdown

## Regla crítica sobre fechas (day_date)
Si la tabla tiene columna `day_date` y la consulta del usuario NO especifica una fecha
o rango de fechas explícito, NUNCA agregues (SUM, COUNT, AVG) sobre todos los días
históricos disponibles - eso da resultados inflados y sin sentido temporal.

En su lugar, filtrá siempre por el día más reciente disponible en esa tabla, usando
una subquery de este tipo:

    WHERE day_date = (SELECT MAX(day_date) FROM <misma_tabla>)

Ejemplo - MAL (sin filtrar por fecha, suma todo el histórico):
    SELECT municipio, SUM(n_usuarios) AS total_usuarios
    FROM concentracao
    WHERE municipio = 'São José'
    GROUP BY municipio

Ejemplo - BIEN (toma solo el día más reciente):
    SELECT municipio, day_date, SUM(n_usuarios) AS total_usuarios
    FROM concentracao
    WHERE municipio = 'São José'
      AND day_date = (SELECT MAX(day_date) FROM concentracao)
    GROUP BY municipio, day_date

Si la consulta del usuario SÍ menciona una fecha específica o un rango
("el 15 de marzo", "la última semana", "en enero"), usá esa fecha/rango en vez
del día más reciente. Fecha detectada por el planner (si aplica): {fecha}

Consulta del usuario: {consulta}
"""

async def llamar_endpoint(metodo: str, endpoint: str, params: dict) -> dict:
    """
    Llama a un endpoint del backend y retorna los datos crudos.
    """
    url = f"{settings.backend_url}{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            if metodo == "GET":
                response = await client.get(url, params=params, timeout=10.0)
            else:
                response = await client.post(url, json=params, timeout=10.0)

            response.raise_for_status()
            data = response.json()

            # Extrae la clave principal de la respuesta (brechas/regiones/programas)
            resultado = (
                data.get("brechas")
                or data.get("regiones")
                or data.get("programas")
                or data
            )

            fuentes = [{"nombre": "Backend AppBiT", "endpoint": endpoint}]
            return {"resultado": resultado, "fuentes": fuentes}

        except httpx.HTTPStatusError as e:
            logger.warning("Error HTTP %s llamando %s: %s", e.response.status_code, endpoint, e)
            return {"resultado": {}, "fuentes": []}
        except httpx.HTTPError as e:
            logger.warning("Error de red llamando %s: %s", endpoint, e)
            return {"resultado": {}, "fuentes": []}


async def ejecutar_sql(consulta: str, schema_minimo: str, model: ChatOpenAI, fecha: str | None = None) -> dict:
    """
    Genera SQL con el modelo primary y lo ejecuta contra MySQL (solo SELECT).
    """

    # 1. Genera el SQL
    prompt = TEXT_TO_SQL_PROMPT.format(
        schema=schema_minimo,
        consulta=consulta,
        fecha=fecha or "no especificada - usar el día más reciente (MAX(day_date))",
    )
    response = await model.ainvoke([
        SystemMessage(content=prompt),
        HumanMessage(content=consulta)
    ])

    sql = _limpiar_sql(response.content.strip())

    print("\n" + "-"*80, flush=True)
    print("SQL generado por el agente:", flush=True)
    print(sql, flush=True)
    print("-"*80, flush=True)

    # Validación mínima de seguridad
    sql_upper = sql.upper()
    if not sql_upper.startswith("SELECT"):
        logger.warning("SQL generado no es SELECT - abortando: %s", sql)
        print("Abortado: no es un SELECT.", flush=True)
        return {"resultado": {}, "fuentes": []}

    for keyword in ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"):
        if keyword in sql_upper:
            logger.warning("SQL contiene keyword peligroso '%s' - abortando.", keyword)
            print(f"Abortado: contiene keyword peligroso '{keyword}'.", flush=True)
            return {"resultado": {}, "fuentes": []}

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

        print(f"SQL ejecutado OK - {len(rows)} filas obtenidas.", flush=True)
        print("Resultado (hasta 10 filas):", flush=True)
        for row in rows[:10]:
            print(f"   {row}", flush=True)
        if len(rows) > 10:
            print(f"   ... y {len(rows) - 10} filas más", flush=True)
        print("-"*80 + "\n", flush=True)

        fuentes = [{"nombre": "Vísent CDRView v2", "codigo_origem": "text_to_sql"}]
        return {"resultado": list(rows), "fuentes": fuentes}

    except Exception as e:
        logger.exception("Error ejecutando SQL: %s", sql)
        print(f"Error ejecutando SQL: {e}", flush=True)
        print("-"*80 + "\n", flush=True)
        return {"resultado": {}, "fuentes": []}