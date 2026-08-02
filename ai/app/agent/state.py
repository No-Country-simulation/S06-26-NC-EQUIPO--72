from typing import TypedDict, NotRequired


class AgentState(TypedDict):
    # Campos requeridos (siempre presentes desde el inicio)
    consulta: str
    idioma: str
    request_id: str

    # Campos opcionales- NotRequired evita KeyError en accesos tempranos
    filtros: NotRequired[dict]
    plan: NotRequired[dict]
    query_type: NotRequired[str]          # "simple" | "compuesta"
    task_decomposition: NotRequired[list] # lista de sub-tareas para agentes
    schema_decision: NotRequired[dict]
    routing_reason: NotRequired[str]
    sub_agent_results: NotRequired[list]  # resultados de cada sub-agente
    tool_results: NotRequired[list]       # siempre list[dict]
    tool_results_meta: NotRequired[dict]
    tool_error: NotRequired[str | None]
    merged_results: NotRequired[list]     # resultado del merge entre sub-agentes
    merge_strategy: NotRequired[str]      # "join" | "relacional"
    join_key: NotRequired[str]            # clave del join exacto (default "cluster")
    datos_validos: NotRequired[bool]
    reflection_score: NotRequired[float]  # score de calidad del reflector
    reflection_feedback: NotRequired[str] # feedback del reflector al formatter
    react_retry_count: NotRequired[int]       # ReAct loop
    reflection_retry_count: NotRequired[int]  # Reflexion
    respuesta_ia: NotRequired[str]
    visualizacion_sugerida: NotRequired[str]
    fuentes: NotRequired[list]
    fuera_de_dominio: NotRequired[bool]


# --- Getters seguros  ---
# El contrato entre nodos: cada getter garantiza un tipo válido,
# evitando `.get()` repetidos con defaults incorrectos en cada nodo.


def get_tool_results(state: AgentState) -> list[dict]:
    """Siempre devuelve lista, nunca None ni dict."""
    results = state.get("tool_results", [])
    if isinstance(results, dict):
        return [results] if results else []
    return results if isinstance(results, list) else []


def get_plan(state: AgentState) -> dict:
    return state.get("plan", {})


def get_schema_decision(state: AgentState) -> dict:
    return state.get("schema_decision", {})


def is_compuesta(state: AgentState) -> bool:
    return state.get("query_type") == "compuesta"


def hay_datos(state: AgentState) -> bool:
    results = get_tool_results(state)
    merged = state.get("merged_results", [])
    return bool(results) or bool(merged)
