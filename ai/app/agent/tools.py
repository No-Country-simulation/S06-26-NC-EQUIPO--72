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
        

async def ejecutar_sql(consulta: str, schema_minimo: str, model: ChatOpenAI) -> dict:
    """
    Genera SQL con el modelo primary y lo ejecuta contra MySQL (solo SELECT).
    """

    # 1. Genera el SQL
    prompt = TEXT_TO_SQL_PROMPT.format(schema=schema_minimo, consulta=consulta)
    response = await model.ainvoke([
        SystemMessage(content=prompt),
        HumanMessage(content=consulta)
    ])

    sql = _limpiar_sql(response.content.strip())

    # Validación mínima de seguridad
    sql_upper = sql.upper()
    if not sql_upper.startswith("SELECT"):
        logger.warning("SQL generado no es SELECT — abortando: %s", sql)
        return {"resultado": {}, "fuentes": []}

    for keyword in ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"):
        if keyword in sql_upper:
            logger.warning("SQL contiene keyword peligroso '%s' — abortando.", keyword)
            return {"resultado": {}, "fuentes": []}

    # 2. Ejecuta el SQL
    try:
        conn = await aiomysql.connect(
            host=settings.db_host,
            port=settings.db_port,
            db=settings.db_name,
            user=settings.db_user,
            password=settings.db_password.get_secret_value(),
        )
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql)
            rows = await cur.fetchall()
        conn.close()

        fuentes = [{"nombre": "Vísent CDRView v2", "codigo_origem": "text_to_sql"}]
        return {"resultado": list(rows), "fuentes": fuentes}

    except Exception as e:
        logger.exception("Error ejecutando SQL: %s", sql)
        return {"resultado": {}, "fuentes": []}