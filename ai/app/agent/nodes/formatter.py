import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.exceptions import OutputParserException
from pydantic import ValidationError

from app.agent.prompts import FORMATTER_PROMPT
from app.agent.state import AgentState, get_tool_results, get_schema_decision
from app.agent.retry import llm_retry
from app.agent.resumir import (
    resumir_para_formatter,
    _limpiar_para_formatter,
    _construir_contexto_formatter,
)
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _formatter_models,
    _formatter_fallback_model,
    _light_models,
    _fallback_model,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


def _corregir_visualizacion(state: AgentState, visualizacion: str) -> str:
    """Mapa determinístico endpoint -> visualización (solo consultas simples)."""
    sd = get_schema_decision(state)
    endpoint = sd.get("endpoint") if isinstance(sd, dict) else None
    if not endpoint:
        return visualizacion
    # Las consultas compuestas no fijan schema_decision a nivel tope ({}), así
    # que acá solo entran las simples con endpoint resuelto.
    fija = {
        "/brechas": "mapa_brechas",
        "/mapa": "mapa_indicadores",
        "/mapa/indicadores": "mapa_indicadores",
        "/indicadores/evolucion": "grafico_barras",
        "/programas": "tabla_datos",
    }
    return fija.get(endpoint, visualizacion)


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def formatter(state: AgentState) -> AgentState:
    request_id = state.get("request_id", "-")
    tool_results = get_tool_results(state)  # siempre list[dict]

    # filtrar campos técnicos internos antes de pasarlos al LLM
    # (solo afecta el contexto- el frontend sigue viendo los datos crudos).
    datos_limpios = _limpiar_para_formatter(tool_results)

    # Resumir datasets grandes por estimación de tokens,
    # no por cantidad de registros como antes (Problema 10).
    datos_resumidos, fue_resumido = resumir_para_formatter(datos_limpios)

    # contexto enriquecido con la decisión explícita (tipo de datos,
    # merge, total de registros) + feedback de reflexión.
    context = _construir_contexto_formatter(state, datos_resumidos, fue_resumido)

    try:
        # Structured output: Pydantic valida JSON y visualizacion_sugerida.
        result = await _llm_ainvoke_con_fallback(
            _formatter_models, _formatter_fallback_model,
            [
                SystemMessage(content=FORMATTER_PROMPT),
                HumanMessage(content=context)
            ],
            request_id, "FORMATTER",
        )
        respuesta_ia = result.respuesta_ia
        visualizacion = result.visualizacion_sugerida
    except (OutputParserException, ValidationError, json.JSONDecodeError) as e:
        # Fallback: reintentar con parseo manual del mismo modelo base.
        logger.error("[%s] FORMATTER | structured output falló: %s- fallback manual",
                     request_id, e)
        response = await _llm_ainvoke_con_fallback(
            _light_models, _fallback_model,
            [
                SystemMessage(content=FORMATTER_PROMPT),
                HumanMessage(content=context)
            ],
            request_id, "FORMATTER",
        )
        try:
            clean = response.content.strip().removeprefix("```json").removesuffix("```").strip()
            result_manual = json.loads(clean)
            respuesta_ia = result_manual.get("respuesta_ia", "No se pudo generar una respuesta.")
            visualizacion = result_manual.get("visualizacion_sugerida", "tabla_datos")
        except json.JSONDecodeError:
            logger.error("[%s] FORMATTER JSON ERROR. Raw response: %s",
                         request_id, response.content[:500])
            respuesta_ia = "No se pudo procesar la consulta."
            visualizacion = "tabla_datos"

    datos_validos = bool(tool_results)
    logger.info("[%s] FORMATTER | visualizacion=%s | datos_validos=%s | resumido=%s",
                request_id, visualizacion, datos_validos, fue_resumido)

    # Estabilidad: la visualización debe ser consistente con el endpoint resuelto.
    # El LLM a veces elige "tabla_datos" para consultas de indicadores/red/brechas.
    visualizacion = _corregir_visualizacion(state, visualizacion)

    return {**state, "respuesta_ia": respuesta_ia, "visualizacion_sugerida": visualizacion}
