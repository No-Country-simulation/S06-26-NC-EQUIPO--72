import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage

from app.agent.prompts import REFLECTOR_PROMPT
from app.agent.state import AgentState, get_tool_results
from app.agent.retry import llm_retry
from app.agent.json_utils import json_default
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _reflector_models,
    _reflector_fallback_model,
)
from app.agent.security import envolver_consulta, envolver_datos
from app.core.config import settings

logger = logging.getLogger(__name__)


def _gate_reflexion(state: AgentState) -> bool:
    """
    Señales determinísticas de respuesta pobre (sin LLM):
    - datos vacíos, o hubo error de tool, o respuesta muy corta
    - ya se retryó antes (siempre re-evaluar tras un retry)
    Reflexionar el 100% de las consultas no justifica el costo del 70B.
    """
    datos = state.get("merged_results") or get_tool_results(state)
    respuesta_ia = state.get("respuesta_ia", "")
    return bool(
        not datos
        or state.get("tool_error")
        or len(respuesta_ia) < 80
        or state.get("reflection_retry_count", 0) > 0
    )


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def reflector(state: AgentState) -> AgentState:
    """
    Evalúa la calidad de la respuesta del formatter.
    Solo invoca el LLM si el gate determinístico detecta respuesta pobre.
    """
    request_id = state.get("request_id", "-")
    datos = state.get("merged_results") or get_tool_results(state)
    respuesta_ia = state.get("respuesta_ia", "")

    if not _gate_reflexion(state):
        logger.debug("[%s] REFLECTOR | omitido (respuesta aparenta ser buena)",
                     request_id)
        return {**state, "reflection_score": 1.0}

    context = (
        f"Consulta original: {envolver_consulta(state['consulta'])}\n"
        f"Idioma esperado: {state['idioma']}\n"
        f"Respuesta del formatter: {respuesta_ia}\n"
        f"Datos disponibles (muestra): "
        f"{envolver_datos(json.dumps(datos[:3], ensure_ascii=False, default=json_default))}\n"
        f"Total de registros: {len(datos)}\n"
        f"Hay datos: {'SÍ' if datos else 'NO'}"
    )

    try:
        result = await _llm_ainvoke_con_fallback(
            _reflector_models, _reflector_fallback_model,
            [
                SystemMessage(content=REFLECTOR_PROMPT),
                HumanMessage(content=context),
            ],
            request_id, "REFLECTOR",
        )

        logger.info(
            "[%s] REFLECTOR | score=%.2f | suficiente=%s | retry=%s",
            request_id, result.quality_score,
            result.es_suficiente, result.necesita_retry
        )

        reflection_retry_count = state.get("reflection_retry_count", 0)
        return {
            **state,
            "reflection_score": result.quality_score,
            "reflection_feedback": result.feedback_al_formatter,
            "reflection_retry_count": (
                reflection_retry_count + (1 if result.necesita_retry else 0)
            ),
        }
    except Exception as e:
        logger.warning("[%s] REFLECTOR | error: %s- omitiendo reflexión",
                       request_id, e)
        return {**state, "reflection_score": 1.0}
