import asyncio
import logging

from app.agent.state import AgentState
from app.agent.sub_agent import run_sub_agent, SubAgentResult
from app.agent.merge import _merge_join

logger = logging.getLogger(__name__)


async def parallel_executor(state: AgentState) -> AgentState:
    """
    Ejecuta todos los sub-agentes en paralelo con asyncio.gather.
    """
    sub_tasks = state.get("task_decomposition", [])
    request_id = state.get("request_id", "-")

    if not sub_tasks:
        logger.error("[%s] PARALLEL_EXECUTOR | sin sub_tasks", request_id)
        return {**state, "sub_agent_results": [], "tool_error": "sin sub-tareas"}

    logger.info(
        "[%s] PARALLEL_EXECUTOR | lanzando %d sub-agentes en paralelo",
        request_id, len(sub_tasks)
    )

    # asyncio.gather ejecuta todos en paralelo- si uno falla,
    # return_exceptions=True evita que cancele los demás.
    raw_results = await asyncio.gather(
        *[run_sub_agent(task, request_id) for task in sub_tasks],
        return_exceptions=True,
    )

    sub_agent_results = []
    all_fuentes = []
    for result in raw_results:
        if isinstance(result, Exception):
            logger.error("[%s] Sub-agente lanzó excepción: %s", request_id, result)
            sub_agent_results.append(SubAgentResult(
                sub_agent_id="unknown", endpoint="unknown",
                results=[], fuentes=[], error=str(result)
            ))
        else:
            sub_agent_results.append(result)
            all_fuentes.extend(result.fuentes)

    # Deduplicar fuentes
    fuentes_unicas = list({
        f["nombre"]: f for f in all_fuentes
    }.values())

    logger.info(
        "[%s] PARALLEL_EXECUTOR | completado | results=%s",
        request_id,
        [(r.sub_agent_id, r.records_count) for r in sub_agent_results]
    )

    return {
        **state,
        "sub_agent_results": [vars(r) for r in sub_agent_results],
        "fuentes": fuentes_unicas,
    }


async def result_merger(state: AgentState) -> AgentState:
    """
    Combina resultados de sub-agentes según merge_strategy.
    JOIN -> Python puro por join_key (_merge_join)
    RELACIONAL -> pasa ambos datasets por separado al formatter
    """
    sub_results = state.get("sub_agent_results", [])
    merge_strategy = state.get("merge_strategy", "join")
    join_key = state.get("join_key", "cluster")
    request_id = state.get("request_id", "-")

    if not sub_results:
        return {**state, "merged_results": [], "tool_results": []}

    # Extraer listas de resultados de cada sub-agente
    result_lists = [r["results"] for r in sub_results if r.get("results")]

    if merge_strategy == "join" and len(result_lists) >= 2:
        merged = _merge_join(result_lists[0], result_lists[1], join_key)
        # Si hay más de 2 sub-agentes, hacer joins adicionales
        for extra_list in result_lists[2:]:
            merged = _merge_join(merged, extra_list, join_key)

        logger.info(
            "[%s] RESULT_MERGER | join por '%s' | %d registros merged",
            request_id, join_key, len(merged)
        )
        return {**state, "merged_results": merged, "tool_results": merged}

    elif merge_strategy == "relacional":
        # Para análisis relacional, el formatter recibe ambos datasets
        # por separado con metadata que le indica cómo interpretarlos
        tool_results_meta = {
            "merge_strategy": "relacional",
            "datasets": [
                {
                    "sub_agent_id": r["sub_agent_id"],
                    "endpoint": r["endpoint"],
                    "descripcion": next(
                        (t["descripcion"] for t in state.get("task_decomposition", [])
                         if t["sub_agent_id"] == r["sub_agent_id"]),
                        r["endpoint"]
                    ),
                    "records": r["results"],
                }
                for r in sub_results
            ],
        }
        # tool_results = concatenación de todos (para guardrail)
        all_records = [rec for r in sub_results for rec in r.get("results", [])]
        return {
            **state,
            "merged_results": all_records,
            "tool_results": all_records,
            "tool_results_meta": {
                **state.get("tool_results_meta", {}),
                **tool_results_meta,
            },
        }

    else:
        # Fallback: usar el primer resultado disponible
        fallback = result_lists[0] if result_lists else []
        logger.warning(
            "[%s] RESULT_MERGER | fallback a primer resultado (%d records)",
            request_id, len(fallback)
        )
        return {**state, "merged_results": fallback, "tool_results": fallback}
