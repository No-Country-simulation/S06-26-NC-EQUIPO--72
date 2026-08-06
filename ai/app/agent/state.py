import re
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

    # HITL — clarificación con el gestor
    session_id: NotRequired[str]
    necesita_clarificacion: NotRequired[bool]
    pregunta_clarificacion: NotRequired[str | None]
    opciones_clarificacion: NotRequired[list[str] | None]
    respuesta_gestor: NotRequired[str | None]
    hitl_activado: NotRequired[bool]  # True si alguna vez pausó


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


def necesita_hitl(state: AgentState) -> bool:
    return bool(state.get("necesita_clarificacion"))


def get_respuesta_gestor(state: AgentState) -> str | None:
    return state.get("respuesta_gestor")


def es_consulta_corta_ambigua(state: AgentState) -> bool:
    """Consulta ultra-corta sin ruido → candidata a clarificación (no FOD).

    Usada por _route_after_planner para NO rechazar como fuera de dominio
    consultas cortas ambiguas como "qué hay".

    Corrección al plan (evita falsos positivos del detector): el planner
    sigue siendo la primera línea de defensa FOD (clima, matemática, chistes).
    Una consulta corta con señales FOD obvias NO pide clarificación.
    """
    consulta = state.get("consulta", "").lower().strip()
    if not consulta:
        return False
    palabras = consulta.split()
    if len(palabras) >= 4:
        return False
    _RUIDO = ("hola", "buenos", "gracias", "adios", "chau", "ok", "si", "no")
    if any(p in consulta for p in _RUIDO):
        return False
    # Señales FOD obvias en consultas cortas: van a fuera_de_dominio, NO a
    # clarificación (casos eval_023 "2+2", eval_027 "contame un chiste").
    if _es_fuera_de_dominio_obvio(consulta):
        return False
    return True


_FOD_OBVIO = (
    "clima", "pronóstico", "pronostico", "lluvia", "temperatura", "hora",
    "chiste", "chistes", "broma", "bromas", "cuento", "joke", "musica",
    "música", "matemática", "matematica", "suma", "resta", "multiplic",
    "divid", "cuánto es", "cuanto es",
)


def _es_fuera_de_dominio_obvio(consulta: str) -> bool:
    """Detecta FOD inconfundible en consultas cortas (matemática, chistes, clima)."""
    if any(p in consulta for p in _FOD_OBVIO):
        return True
    # Aritmética explícita: "2+2", "cuánto es 5*3" (dígitos u operadores).
    return bool(re.search(r"\d", consulta))
