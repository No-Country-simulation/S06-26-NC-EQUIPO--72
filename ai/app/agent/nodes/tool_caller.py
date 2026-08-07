import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage

from app.agent.prompts import REACT_REASONER_PROMPT
from app.agent.state import (
    AgentState,
    get_plan,
    get_schema_decision,
    get_tool_results,
)
from app.agent.retry import llm_retry
from app.agent.parsing import _extraer_json_con_fallback
from app.agent.tools import llamar_endpoint, ejecutar_sql
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _primary_models,
    _fallback_model,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


async def tool_caller(state: AgentState) -> AgentState:
    """
    Ejecuta la decisión del schema_linker:
    - Si tipo == "endpoint": llama al backend via HTTP
    - Si tipo == "sql": genera SQL con el modelo primary y lo ejecuta
    """
    request_id = state.get("request_id", "-")
    decision = get_schema_decision(state)
    results: list[dict] = []

    if not decision:
        # Contrato de estado violado: schema_linker debería haber seteado
        # schema_decision. Fallback explícito en vez de KeyError silencioso.
        logger.error("[%s] TOOL_CALLER | sin schema_decision", request_id)
        return {
            **state,
            "tool_results": [],
            "tool_error": "sin schema_decision",
        }

    if decision["tipo"] == "endpoint":

        data = await llamar_endpoint(
            metodo=decision.get("metodo", "GET"),
            endpoint=decision["endpoint"],
            params=decision["params"],
            request_id=request_id,
        )
        results = data.get("resultado", [])
        fuentes = data.get("fuentes", [])

    elif decision["tipo"] == "sql":
        plan = get_plan(state)
        data = await ejecutar_sql(
            consulta=state["consulta"],
            schema_minimo=decision["schema_minimo"],
            modelos=_primary_models,
            model_fallback=_fallback_model,
            fecha=plan.get("fecha"),
            filtros={
                "municipio": plan.get("municipio"),
                "cluster": plan.get("cluster"),
                "periodo": plan.get("periodo"),
                "income_cluster": plan.get("income_cluster"),
                "servicio": plan.get("servicio"),
            },
            request_id=request_id,
        )
        results = data.get("resultado", [])
        fuentes = data.get("fuentes", [])

    # Contrato de estado: tool_results siempre es list[dict]
    if isinstance(results, dict):
        results = [results] if results else []
    elif not isinstance(results, list):
        results = []

    n_results = len(results)
    logger.info("[%s] TOOL_CALLER | records=%d | fuente=%s",
                request_id, n_results, decision.get("endpoint", "sql"))

    return {**state, "tool_results": results, "fuentes": fuentes}


def _aplicar_correccion_react(decision: dict, reasoning: dict) -> dict:
    """
    Aplica la corrección del reasoner sobre schema_decision (función pura).
    - Si propone un endpoint HTTP (empieza con "/"), el tipo pasa a
      "endpoint" y se actualizan endpoint/params.
    - Si propone solo params, se actualizan params.
    - Se eliminan params None: httpx no los omite (envía "clave=" vacío)
      y el backend lo interpreta como filtro activo -> 0 records.
      Mismo criterio que _build_endpoint_decision (schema_linker).
    """
    nueva_decision = {**decision}
    nuevo_endpoint = reasoning.get("nuevo_endpoint")
    nuevos_params = reasoning.get("nuevos_params", {})

    if isinstance(nuevo_endpoint, str) and nuevo_endpoint.startswith("/"):
        nueva_decision["tipo"] = "endpoint"
        nueva_decision["endpoint"] = nuevo_endpoint
        # Si la decisión venía de SQL (sin metodo), el re-toolcall por HTTP
        # crasheaba con KeyError: 'metodo' en tool_caller (eval_007/028).
        nueva_decision.setdefault("metodo", "GET")
        if isinstance(nuevos_params, dict) and nuevos_params:
            nueva_decision["params"] = nuevos_params
    elif isinstance(nuevos_params, dict) and nuevos_params:
        nueva_decision["params"] = nuevos_params

    nueva_decision["params"] = {
        k: v for k, v in nueva_decision.get("params", {}).items()
        if v is not None
    }
    return nueva_decision


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def react_reasoner(state: AgentState) -> AgentState:
    """
    Razona sobre por qué el tool call anterior falló y propone un ajuste.
    Solo se ejecuta si react_retry_count < max_retries_llm (garantiza que
    el loop siempre termina). Actualiza schema_decision para el re-intento.
    """
    request_id = state.get("request_id", "-")
    react_retry_count = state.get("react_retry_count", 0)
    if react_retry_count >= settings.max_retries_llm:
        logger.info("[%s] REACT | máximo de reintentos alcanzado", request_id)
        return state

    decision = get_schema_decision(state)
    tool_results = get_tool_results(state)
    plan = get_plan(state)

    context = (
        f"Consulta: {state['consulta']}\n"
        f"Endpoint llamado: {decision.get('endpoint', 'sql')}\n"
        f"Parámetros usados: {json.dumps(decision.get('params', {}), ensure_ascii=False)}\n"
        f"Resultado: {'vacío' if not tool_results else f'{len(tool_results)} registros'}\n"
        f"Plan del planner: {json.dumps(plan, ensure_ascii=False)}\n"
        f"Reintento actual: {react_retry_count + 1}/{settings.max_retries_llm}"
    )

    try:
        response = await _llm_ainvoke_con_fallback(
            _primary_models, _fallback_model,
            [
                SystemMessage(content=REACT_REASONER_PROMPT),
                HumanMessage(content=context),
            ],
            request_id, "REACT_REASONER",
        )
        reasoning = _extraer_json_con_fallback(response.content, request_id)
        logger.info(
            "[%s] REACT_REASONER | razon='%s' | accion='%s' | nuevo_endpoint=%s",
            request_id,
            reasoning.get("razon_datos_vacios", ""),
            reasoning.get("accion", ""),
            reasoning.get("nuevo_endpoint"),
        )

        nueva_decision = _aplicar_correccion_react(decision, reasoning)

        return {
            **state,
            "schema_decision": nueva_decision,
            "react_retry_count": react_retry_count + 1,
        }
    except Exception as e:
        logger.warning("[%s] REACT_REASONER | error: %s", request_id, e)
        return {**state, "react_retry_count": react_retry_count + 1}
