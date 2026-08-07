import logging

from langgraph.graph import END

from app.agent.state import (
    AgentState,
    get_plan,
    get_tool_results,
    es_consulta_corta_ambigua,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


def _route_after_input_guardrail(state: AgentState) -> str:
    """
    Si la consulta no pasó la validación de input (vacía/corta),
    corta a END con el mensaje del guardrail (evita que el nodo
    fuera_de_dominio sobrescriba ese mensaje); si no, sigue al planner.
    """
    if state.get("fuera_de_dominio"):
        return END
    return "planner"


def _route_after_planner(state: AgentState) -> str:
    """
    Decide si la consulta sigue el flujo normal (query_classifier ->
    schema_linker/tool_caller) o corta directo a una respuesta de fuera de
    dominio, sin gastar llamadas de más a Qdrant, al backend o al modelo LLM.
    """
    if get_plan(state).get("fuera_de_dominio"):
        # Corrección 2: consultas ultra-cortas ambiguas ("qué hay") NO son
        # fuera de dominio — son candidatas a clarificación. Pasan por el
        # clarification_detector en vez de cortar a FOD.
        if es_consulta_corta_ambigua(state):
            return "query_classifier"
        return "fuera_de_dominio"
    return "query_classifier"


def _route_after_classifier(state: AgentState) -> str:
    if state.get("query_type") == "compuesta":
        return "task_decomposer"
    return "schema_linker"


def _route_after_task_decomposer(state: AgentState) -> str:
    # Si el decomposer falló y revirtió a simple
    if state.get("query_type") == "simple":
        return "schema_linker"
    return "parallel_executor"


def _route_after_tool_caller(state: AgentState) -> str:
    """
    Decide si hacer ReAct retry o continuar al output_guardrail.
    Solo aplica para consultas simples- las compuestas tienen su propio
    manejo de errores en parallel_executor.
    """
    tool_results = get_tool_results(state)
    react_retry_count = state.get("react_retry_count", 0)
    query_type = state.get("query_type", "simple")

    datos_vacios = not tool_results
    puede_reintentar = react_retry_count < settings.max_retries_llm
    es_simple = query_type == "simple"

    if datos_vacios and puede_reintentar and es_simple:
        logger.info(
            "[%s] REACT | datos vacíos- razonando ajuste (retry %d/%d)",
            state.get("request_id", "-"),
            react_retry_count + 1, settings.max_retries_llm,
        )
        return "react_reasoner"

    return "output_guardrail"


def _route_after_reflector(state: AgentState) -> str:
    """
    Si la reflexión indica respuesta pobre y hay reintentos disponibles,
    vuelve al formatter con feedback. Regla única: count < max (nunca <=).
    """
    score = state.get("reflection_score", 1.0)
    retry_count = state.get("reflection_retry_count", 0)
    max_retries = settings.reflector_max_retries

    if score < settings.reflector_min_quality_score and retry_count < max_retries:
        logger.info(
            "[%s] REFLECTOR | score %.2f < %.2f- formatter retry %d/%d",
            state.get("request_id", "-"), score,
            settings.reflector_min_quality_score, retry_count, max_retries
        )
        return "formatter"

    return END
