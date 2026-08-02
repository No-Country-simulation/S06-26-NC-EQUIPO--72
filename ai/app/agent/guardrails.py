import logging

from app.agent.state import AgentState, get_tool_results

logger = logging.getLogger(__name__)


def _sanitizar_consulta(consulta: str) -> str:
    """
    Sanitización de input: limita a 500 chars y elimina
    caracteres de control (salvo \n y \t). Sin LLM- rápido y barato.
    """
    MAX_CHARS = 500
    if len(consulta) > MAX_CHARS:
        logger.warning("Consulta truncada de %d a %d chars", len(consulta), MAX_CHARS)
        consulta = consulta[:MAX_CHARS]
    # Eliminar caracteres de control excepto salto de línea y tab
    consulta = "".join(c for c in consulta if c.isprintable() or c in ("\n", "\t"))
    return consulta.strip()


async def input_guardrail(state: AgentState) -> AgentState:
    """
    Validación determinística de la consulta antes de procesarla.
    Sin LLM- rápido y barato. Si la consulta es inválida, corta el flujo
    (el router _route_after_input_guardrail lo lleva a END).
    """
    consulta = state.get("consulta", "")

    # Consulta vacía o demasiado corta
    if len(consulta.strip()) < 3:
        return {
            **state,
            "fuera_de_dominio": True,
            "respuesta_ia": "La consulta está vacía o es demasiado corta.",
        }

    # Sanitización
    consulta_sanitizada = _sanitizar_consulta(consulta)

    return {**state, "consulta": consulta_sanitizada}


async def output_guardrail(state: AgentState) -> AgentState:
    """
    Validación de coherencia entre consulta y datos obtenidos.
    Sin LLM- determinístico. Registra advertencias en tool_results_meta
    y calcula datos_validos (True si no hay advertencias salvo "resultado vacío").
    """
    tool_results = get_tool_results(state)
    merged = state.get("merged_results", [])
    datos = merged or tool_results
    decision = state.get("schema_decision", {})
    advertencias = []

    # Check 1: datos vacíos
    if not datos:
        advertencias.append("resultado vacío")

    # Check 2: error en tool caller
    if state.get("tool_error"):
        advertencias.append(f"tool_error: {state['tool_error']}")

    # Check 3: /brechas sin severidad_brecha
    if decision.get("endpoint") == "/brechas" and datos:
        if not any("severidad_brecha" in r for r in datos):
            advertencias.append("/brechas sin campo severidad_brecha")

    # Check 4: sub-agentes con error en consulta compuesta
    for sr in state.get("sub_agent_results", []):
        if sr.get("error"):
            advertencias.append(f"sub_agent {sr['sub_agent_id']}: {sr['error']}")

    if advertencias:
        logger.warning(
            "[%s] OUTPUT_GUARDRAIL | advertencias: %s",
            state.get("request_id", "-"), "; ".join(advertencias)
        )

    return {
        **state,
        "datos_validos": not bool([a for a in advertencias if "vacío" not in a]),
        "tool_results_meta": {
            **state.get("tool_results_meta", {}),
            "advertencias": advertencias,
        },
    }
