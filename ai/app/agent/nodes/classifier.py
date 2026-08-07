import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.exceptions import OutputParserException
from pydantic import ValidationError

from app.agent.prompts import QUERY_CLASSIFIER_PROMPT
from app.agent.state import AgentState
from app.agent.retry import llm_retry
from app.agent.parsing import _extraer_json_con_fallback
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _classifier_models,
    _classifier_fallback_model,
    _primary_models,
    _fallback_model,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def query_classifier(state: AgentState) -> AgentState:
    """
    Clasifica la consulta como simple o compuesta y determina
    qué fuentes de datos se necesitan (merge_strategy).
    """
    request_id = state.get("request_id", "-")
    try:
        result = await _llm_ainvoke_con_fallback(
            _classifier_models, _classifier_fallback_model,
            [
                SystemMessage(content=QUERY_CLASSIFIER_PROMPT),
                HumanMessage(content=(
                    f"Consulta: {state['consulta']}\n"
                    f"Plan del planner: {json.dumps(state.get('plan', {}), ensure_ascii=False)}"
                ))
            ],
            request_id, "QUERY_CLASSIFIER",
        )
        logger.info(
            "[%s] QUERY_CLASSIFIER | tipo=%s | fuentes=%s | merge=%s",
            request_id, result.query_type,
            result.fuentes_necesarias, result.merge_strategy
        )
        return {
            **state,
            "query_type": result.query_type,
            "merge_strategy": result.merge_strategy,
        }
    except (OutputParserException, ValidationError, json.JSONDecodeError) as e:
        # Fallback manual: el 70B a veces omite merge_strategy (lo deja en
        # null) y Pydantic rechaza el JSON completo, tirando la clasificación.
        # En vez de degradar a "simple" a ciegas, reintentamos el parseo con
        # el mismo modelo base y defaults seguros.
        logger.warning("[%s] QUERY_CLASSIFIER | structured output falló: %s- fallback manual",
                       request_id, e)
        try:
            response = await _llm_ainvoke_con_fallback(
                _primary_models, _fallback_model,
                [
                    SystemMessage(content=QUERY_CLASSIFIER_PROMPT),
                    HumanMessage(content=(
                        f"Consulta: {state['consulta']}\n"
                        f"Plan del planner: {json.dumps(state.get('plan', {}), ensure_ascii=False)}"
                    ))
                ],
                request_id, "QUERY_CLASSIFIER",
            )
            raw = _extraer_json_con_fallback(response.content, request_id)
            query_type = raw.get("query_type", "simple")
            if query_type not in ("simple", "compuesta"):
                query_type = "simple"
            merge = raw.get("merge_strategy", "join")
            if merge not in ("join", "relacional"):
                merge = "join"
            logger.info("[%s] QUERY_CLASSIFIER | fallback manual: tipo=%s | merge=%s",
                        request_id, query_type, merge)
            return {
                **state,
                "query_type": query_type,
                "merge_strategy": merge,
            }
        except Exception:
            # Último recurso: default simple- nunca bloquear el pipeline.
            logger.warning("[%s] QUERY_CLASSIFIER | fallback manual falló- default simple",
                           request_id)
            return {**state, "query_type": "simple", "merge_strategy": "join"}
