import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.exceptions import OutputParserException
from pydantic import ValidationError

from app.agent.prompts import TASK_DECOMPOSER_PROMPT
from app.agent.state import AgentState, get_plan
from app.agent.retry import llm_retry
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _decomposer_models,
    _decomposer_fallback_model,
)
from app.agent.security import envolver_consulta
from app.core.config import settings

logger = logging.getLogger(__name__)


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def task_decomposer(state: AgentState) -> AgentState:
    """
    Descompone una consulta compuesta en sub-tareas paralelas.
    """
    request_id = state.get("request_id", "-")
    plan = get_plan(state)
    try:
        result = await _llm_ainvoke_con_fallback(
            _decomposer_models, _decomposer_fallback_model,
            [
                SystemMessage(content=TASK_DECOMPOSER_PROMPT),
                HumanMessage(content=(
                    f"Consulta: {envolver_consulta(state['consulta'])}\n"
                    f"Plan del planner: {json.dumps(plan, ensure_ascii=False)}\n"
                    f"Merge strategy: {state.get('merge_strategy', 'join')}"
                ))
            ],
            request_id, "TASK_DECOMPOSER",
        )
        logger.info(
            "[%s] TASK_DECOMPOSER | sub_tasks=%d | join_key=%s",
            request_id, len(result.sub_tasks), result.join_key
        )
        return {
            **state,
            "task_decomposition": [t.model_dump() for t in result.sub_tasks],
            "merge_strategy": result.merge_strategy,
            "join_key": result.join_key or "cluster",
        }
    except (OutputParserException, ValidationError, json.JSONDecodeError) as e:
        logger.error("[%s] TASK_DECOMPOSER | error: %s- tratando como simple",
                     request_id, e)
        return {**state, "query_type": "simple"}
