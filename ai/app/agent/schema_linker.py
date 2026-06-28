import logging
from app.agent.state import AgentState
from app.vectorstore.searcher import search

logger = logging.getLogger(__name__)


def _build_endpoint_decision(payload: dict, plan: dict) -> dict:
    """
    Construye los parámetros del endpoint a partir del payload de Qdrant
    y el plan del planner (que ya clasificó servicio/categoría).
    """
    endpoint = payload["endpoint"]
    servicio = plan.get("servicio")
    params: dict = {}

    if endpoint == "/brechas":
        params = {
            "servicio": servicio,
            "municipio": plan.get("municipio"),
            "periodo": plan.get("periodo", "TARDE"),
            "income_cluster": plan.get("income_cluster"),
        }
    elif endpoint == "/mapa":
        params = {
            "periodo": plan.get("periodo", "TARDE"),
            "municipio": plan.get("municipio"),
            "fecha": plan.get("fecha"),
        }
    elif endpoint == "/mapa/indicadores":
        # categoria usa los mismos valores que servicio para SALUD_MENTAL/EMPLEO/EDUCACION
        params = {
            "categoria": servicio,
            "indicador": plan.get("indicador"),
            "municipio": plan.get("municipio"),
        }
    elif endpoint == "/programas":
        params = {
            "tipo": servicio,
            "municipio": plan.get("municipio"),
            "cluster": plan.get("cluster"),
            "activo": True,
        }

    # Elimina params None para no mandarlos en la query
    params = {k: v for k, v in params.items() if v is not None}

    return {
        "tipo": "endpoint",
        "metodo": payload.get("metodo", "GET"),
        "endpoint": endpoint,
        "params": params,
        "score": payload["score"],
    }


def _build_sql_decision(payload: dict | None) -> dict:
    """
    Construye la decisión de fallback SQL.
    Si hay payload (tabla con score bajo pero existente), usa su schema.
    Si no hay nada, usa schema mínimo genérico.
    """
    if payload:
        return {
            "tipo": "sql",
            "tablas": payload.get("tablas", []),
            "schema_minimo": payload.get("schema_minimo", ""),
            "score": payload.get("score", 0.0),
        }
    return {
        "tipo": "sql",
        "tablas": ["concentracao"],
        "schema_minimo": (
            "concentracao(ecgi, cluster, municipio, day_date, periodo, "
            "n_usuarios, download_gb, congestionamento_medio, rat_type_predominante)"
        ),
        "score": 0.0,
    }


async def schema_linker(state: AgentState) -> AgentState:
    """
    Busca en Qdrant el endpoint o tabla más similar a la consulta.
    Decide si el tool_caller debe llamar a un endpoint o generar SQL.
    No consume tokens LLM.
    """
    consulta = state["consulta"]
    plan = state.get("plan", {})

    result = search(consulta, top_k=1)

    if result and result["tipo"] == "endpoint":
        decision = _build_endpoint_decision(result, plan)
    else:
        decision = _build_sql_decision(result)

    logger.info("Schema linker decision: %s", decision)
    return {**state, "schema_decision": decision}