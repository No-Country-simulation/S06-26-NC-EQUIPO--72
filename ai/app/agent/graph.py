import asyncio
import json
import logging
import re
from typing import Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.exceptions import OutputParserException
from openai import RateLimitError
from pydantic import ValidationError
from app.agent.prompts import (
    PLANNER_PROMPT,
    FORMATTER_PROMPT,
    QUERY_CLASSIFIER_PROMPT,
    TASK_DECOMPOSER_PROMPT,
    REACT_REASONER_PROMPT,
    REFLECTOR_PROMPT,
)
from app.agent.schema_linker import schema_linker
from app.agent.tools import llamar_endpoint, ejecutar_sql
from app.agent.sub_agent import run_sub_agent, SubAgentResult
from app.agent.state import AgentState, get_plan, get_schema_decision, get_tool_results
from app.agent.retry import llm_retry
from app.agent.resumir import (
    resumir_para_formatter,
    _limpiar_para_formatter,
    _construir_contexto_formatter,
)
from app.agent.json_utils import json_default
from app.agent.merge import _merge_join
from app.agent.guardrails import input_guardrail, output_guardrail
from app.agent.output_schemas import (
    PlanOutput,
    QueryClassification,
    TaskDecomposition,
    ReflectionOutput,
    FormatterOutput,
)
from app.core.config import settings
from app.agent.normalizer import normalizar_plan


logger = logging.getLogger(__name__)


def _extraer_json_con_fallback(raw: str, request_id: str = "-") -> dict:
    """
    Intenta extraer JSON válido de la respuesta del LLM.
    Estrategia: parseo directo -> regex -> plan vacío seguro.
    El fallback nunca tira todo el pipeline (Fix Bug C).
    """
    # Intento 1: parseo limpio directo
    if not isinstance(raw, str) or not raw.strip():
        logger.warning("[%s] Planner devolvió respuesta vacía o inválida", request_id)
        return {
            "fuera_de_dominio": False,
            "servicio": None,
            "municipio": None,
            "periodo": None,
            "cluster": None,
            "income_cluster": None,
            "indicador": None,
            "fecha": None,
            "razon": "fallback por respuesta vacía",
        }
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Intento 2: extraer el primer objeto JSON con regex
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group())
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    # Intento 3: plan vacío seguro- nunca tirar todo el pipeline
    logger.warning("[%s] Planner no pudo producir JSON válido. Raw: %s",
                   request_id, raw[:300])
    return {
        "fuera_de_dominio": False,
        "servicio": None,
        "municipio": None,
        "periodo": None,
        "cluster": None,
        "income_cluster": None,
        "indicador": None,
        "fecha": None,
        "razon": "fallback por error de parseo",
    }


# Mensajes de respuesta para consultas fuera de dominio, por idioma.
_MENSAJE_FUERA_DE_DOMINIO = {
    "es": (
        "Este asistente responde consultas sobre inclusión social, formación, empleo, "
        "salud mental, conectividad y programas sociales en la Región Metropolitana de "
        "Florianópolis. ¿Querés reformular tu pregunta dentro de ese contexto?"
    ),
    "pt": (
        "Este assistente responde consultas sobre inclusão social, formação, emprego, "
        "saúde mental, conectividade e programas sociais na Região Metropolitana de "
        "Florianópolis. Você poderia reformular sua pergunta dentro desse contexto?"
    ),
    "en": (
        "This assistant answers questions about social inclusion, training, employment, "
        "mental health, connectivity, and social programs in the Florianópolis Metropolitan "
        "Region. Could you rephrase your question within that scope?"
    ),
}


# instancia modelo light (Planner y Formatter)
# max_retries=0: el cliente openai reintenta internamente con backoff que puede
# llegar a 54s en un 429 (rate limit de Groq), comiéndose el timeout global
# (max_retries=1 no acota la espera, solo el número de intentos). Con 0, el
# RateLimitError propaga a @llm_retry (tenacity, esperas acotadas 1-8s).
_light_model = ChatOpenAI(
    api_key=settings.groq_api_key_light.get_secret_value(),
    base_url=settings.groq_base_url,
    model=settings.groq_model_light,
    temperature=0,
    max_retries=0,
)

# instancia modelo primary (Tool Calling y SQL)
_primary_model = ChatOpenAI(
    api_key=settings.groq_api_key_primary.get_secret_value(),
    base_url=settings.groq_base_url,
    model=settings.groq_model_primary,
    temperature=0,
    max_retries=0,
)

# Modelo fallback (Gemini 2.0 Flash Lite vía el endpoint OpenAI-compatible de
# Google). Pool de límites independiente de Groq: cuando cualquier modelo de
# Groq rate-limita (429 TPM/TPD), los nodos pasan a este en vez de esperar.
_fallback_model = ChatOpenAI(
    api_key=settings.google_api_key.get_secret_value(),
    base_url=settings.gemini_base_url,
    model=settings.gemini_model_fallback,
    temperature=0,
    max_retries=0,
)

# Versiones con structured output (json_mode soportado por Groq).
# el upgrade a 70B es condicional a que los evals den < 85%.
_planner_model = _light_model.with_structured_output(PlanOutput, method="json_mode")
_classifier_model = _primary_model.with_structured_output(
    QueryClassification, method="json_mode"
)
_decomposer_model = _primary_model.with_structured_output(
    TaskDecomposition, method="json_mode"
)
_reflector_model = _primary_model.with_structured_output(
    ReflectionOutput, method="json_mode"
)
_formatter_model = _light_model.with_structured_output(
    FormatterOutput, method="json_mode"
)

# Fallback (Gemini) con structured output para cada nodo: se activa ante un
# 429 de Groq (TPM o TPD). Gemini 2.0 Flash Lite soporta response_format
# json_object en su endpoint OpenAI-compatible.
_planner_fallback_model = _fallback_model.with_structured_output(
    PlanOutput, method="json_mode"
)
_classifier_fallback_model = _fallback_model.with_structured_output(
    QueryClassification, method="json_mode"
)
_decomposer_fallback_model = _fallback_model.with_structured_output(
    TaskDecomposition, method="json_mode"
)
_reflector_fallback_model = _fallback_model.with_structured_output(
    ReflectionOutput, method="json_mode"
)
_formatter_fallback_model = _fallback_model.with_structured_output(
    FormatterOutput, method="json_mode"
)


async def _llm_ainvoke_con_fallback(modelo, modelo_fallback, mensajes,
                                    request_id: str, nodo: str):
    """Invoca el modelo; ante rate-limit usa el fallback (pool de TPM separado).

    Si el fallback también falla, la excepción propaga a @llm_retry (tenacity),
    que reintenta todo el nodo con esperas acotadas 1-8s.
    """
    try:
        return await modelo.ainvoke(mensajes)
    except RateLimitError:
        logger.warning("[%s] %s | rate limit en %s- fallback a %s",
                       request_id, nodo,
                       _nombre_modelo(modelo), _nombre_modelo(modelo_fallback))
        return await modelo_fallback.ainvoke(mensajes)


def _nombre_modelo(modelo) -> str:
    """Nombre del modelo base, incluso dentro del wrapper de structured output."""
    nombre = getattr(modelo, "model_name", None)
    if nombre:
        return nombre
    for paso in getattr(modelo, "steps", []) or []:
        bound = getattr(paso, "bound", None)
        nombre = getattr(bound, "model_name", None)
        if nombre:
            return nombre
    return "?"

def _route_after_input_guardrail(state: AgentState) -> str:
    """
    si la consulta no pasó la validación de input (vacía/corta),
    corta a END con el mensaje del guardrail (evita que el nodo
    fuera_de_dominio sobrescriba ese mensaje); si no, sigue al planner.
    """
    if state.get("fuera_de_dominio"):
        return END
    return "planner"


# Nodo 1 - Planner (usa modelo light con structured output)
@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def planner(state: AgentState) -> AgentState:
    request_id = state.get("request_id", "-")
    try:
        # Structured output: Pydantic valida el JSON y elimina el parsing manual.
        result: PlanOutput = await _llm_ainvoke_con_fallback(
            _planner_model, _planner_fallback_model,
            [
                SystemMessage(content=PLANNER_PROMPT),
                HumanMessage(content=state["consulta"])
            ],
            request_id, "PLANNER",
        )
        plan = result.model_dump()
    except (OutputParserException, ValidationError, json.JSONDecodeError) as e:
        # Fallback: el modelo no produjo JSON válido- reintentar parseo manual.
        # Los errores transitorios de API los reintenta el decorador @llm_retry.
        logger.warning("[%s] PLANNER | structured output falló: %s- fallback manual",
                       request_id, e)
        response = await _llm_ainvoke_con_fallback(
            _light_model, _fallback_model,
            [
                SystemMessage(content=PLANNER_PROMPT),
                HumanMessage(content=state["consulta"])
            ],
            request_id, "PLANNER",
        )
        plan = _extraer_json_con_fallback(response.content, request_id)
    plan = normalizar_plan(plan)  # <-- corrección determinística post-LLM

    logger.info("[%s] PLANNER | servicio=%s | municipio=%s | fuera_dominio=%s",
                request_id, plan.get("servicio"), plan.get("municipio"),
                plan.get("fuera_de_dominio"))
    logger.debug("[%s] PLANNER | plan=%s", request_id,
                 json.dumps(plan, ensure_ascii=False, default=json_default))

    return {**state, "plan": plan}


def _route_after_planner(state: AgentState) -> str:
    """
    Decide si la consulta sigue el flujo normal (query_classifier ->
    schema_linker/tool_caller) o corta directo a una respuesta de fuera de
    dominio, sin gastar llamadas de más a Qdrant, al backend o al modelo LLM.
    """
    if get_plan(state).get("fuera_de_dominio"):
        return "fuera_de_dominio"
    return "query_classifier"


# Nodo - Fuera de dominio (corta el flujo temprano, sin tools ni SQL)
async def fuera_de_dominio_node(state: AgentState) -> AgentState:
    request_id = state.get("request_id", "-")
    idioma = state.get("idioma", "es")
    mensaje = _MENSAJE_FUERA_DE_DOMINIO.get(idioma, _MENSAJE_FUERA_DE_DOMINIO["es"])
    razon = state.get("plan", {}).get("razon", "")
    logger.info("[%s] FUERA_DE_DOMINIO | razon=%s", request_id, razon)

    return {
        **state,
        "fuera_de_dominio": True,
        "respuesta_ia": mensaje,
    }


# Nodo 2 - Query Classifier
@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def query_classifier(state: AgentState) -> AgentState:
    """
    Clasifica la consulta como simple o compuesta y determina
    qué fuentes de datos se necesitan (merge_strategy).
    """
    request_id = state.get("request_id", "-")
    try:
        result: QueryClassification = await _llm_ainvoke_con_fallback(
            _classifier_model, _classifier_fallback_model,
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
                _primary_model, _fallback_model,
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


def _route_after_classifier(state: AgentState) -> str:
    if state.get("query_type") == "compuesta":
        return "task_decomposer"
    return "schema_linker"


# Nodo 3 - Task Decomposer
@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def task_decomposer(state: AgentState) -> AgentState:
    """
    Descompone una consulta compuesta en sub-tareas paralelas.
    """
    request_id = state.get("request_id", "-")
    plan = get_plan(state)
    try:
        result: TaskDecomposition = await _llm_ainvoke_con_fallback(
            _decomposer_model, _decomposer_fallback_model,
            [
                SystemMessage(content=TASK_DECOMPOSER_PROMPT),
                HumanMessage(content=(
                    f"Consulta: {state['consulta']}\n"
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


def _route_after_task_decomposer(state: AgentState) -> str:
    # Si el decomposer falló y revirtió a simple
    if state.get("query_type") == "simple":
        return "schema_linker"
    return "parallel_executor"


# Nodo 4 - Parallel Executor
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


# Nodo 5 - Result Merger
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

# Nodo 2 - Tool Caller
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
            model=_primary_model,
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


# Nodo 5 - React Reasoner
# ReAct = loop opcional DENTRO del flujo simple: si el tool call devolvió
# datos vacíos, el reasoner razona POR QUÉ y propone un ajuste (nuevo
# endpoint/params). tool_caller re-intenta con la decisión corregida.
# Usa su propio contador (react_retry_count)- no interfiere con el
# presupuesto de retries del reflector (reflection_retry_count).
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
            _primary_model, _fallback_model,
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



# Nodo 3 - Formatter (usa modelo light con structured output)
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
        result: FormatterOutput = await _llm_ainvoke_con_fallback(
            _formatter_model, _formatter_fallback_model,
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
            _light_model, _fallback_model,
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

    return {**state, "respuesta_ia": respuesta_ia, "visualizacion_sugerida": visualizacion}


# Nodo 6 - Reflector
# Reflexion pattern: evalúa la calidad de la respuesta del formatter antes
# de devolverla. Si es pobre, el formatter recibe feedback y reintenta.
# Contador propio (reflection_retry_count)- no interfiere con ReAct.
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
        f"Consulta original: {state['consulta']}\n"
        f"Idioma esperado: {state['idioma']}\n"
        f"Respuesta del formatter: {respuesta_ia}\n"
        f"Datos disponibles (muestra): "
        f"{json.dumps(datos[:3], ensure_ascii=False, default=json_default)}\n"
        f"Total de registros: {len(datos)}\n"
        f"Hay datos: {'SÍ' if datos else 'NO'}"
    )

    try:
        result: ReflectionOutput = await _llm_ainvoke_con_fallback(
            _reflector_model, _reflector_fallback_model,
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



# Construcción del grafo
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("fuera_de_dominio", fuera_de_dominio_node)
    graph.add_node("input_guardrail", input_guardrail)
    graph.add_node("output_guardrail", output_guardrail)
    graph.add_node("query_classifier", query_classifier)
    graph.add_node("task_decomposer", task_decomposer)
    graph.add_node("parallel_executor", parallel_executor)
    graph.add_node("result_merger", result_merger)
    graph.add_node("schema_linker", schema_linker)
    graph.add_node("tool_caller", tool_caller)
    graph.add_node("react_reasoner", react_reasoner)
    graph.add_node("formatter", formatter)
    graph.add_node("reflector", reflector)

    graph.set_entry_point("input_guardrail")

    # validación de input primero- si es inválida corta a END.
    graph.add_conditional_edges(
        "input_guardrail",
        _route_after_input_guardrail,
        {
            "planner": "planner",
            END: END,
        },
    )

    # Routing condicional: si es fuera de dominio, corta directo a END
    # sin pasar por query_classifier/schema_linker/tool_caller/formatter.
    graph.add_conditional_edges(
        "planner",
        _route_after_planner,
        {
            "query_classifier": "query_classifier",
            "fuera_de_dominio": "fuera_de_dominio",
        },
    )

    # Consulta simple -> schema_linker; compuesta -> task_decomposer.
    graph.add_conditional_edges(
        "query_classifier",
        _route_after_classifier,
        {
            "task_decomposer": "task_decomposer",
            "schema_linker": "schema_linker",
        },
    )

    # Si el decomposer falló y revirtió a simple, va a schema_linker.
    graph.add_conditional_edges(
        "task_decomposer",
        _route_after_task_decomposer,
        {
            "parallel_executor": "parallel_executor",
            "schema_linker": "schema_linker",
        },
    )

    # Flujo simple- con ReAct loop: si el tool call devuelve datos
    # vacíos, tool_caller -> react_reasoner -> tool_caller (hasta max retries);
    # luego pasa por output_guardrail -> formatter.
    graph.add_edge("schema_linker", "tool_caller")
    graph.add_conditional_edges(
        "tool_caller",
        _route_after_tool_caller,
        {
            "react_reasoner": "react_reasoner",
            "output_guardrail": "output_guardrail",
        },
    )
    graph.add_edge("react_reasoner", "tool_caller")
    graph.add_edge("output_guardrail", "formatter")

    # Flujo compuesto
    graph.add_edge("parallel_executor", "result_merger")
    graph.add_edge("result_merger", "output_guardrail")

    # Reflexion pattern: tras el formatter, el reflector evalúa la
    # respuesta; si es pobre y hay presupuesto de retries, vuelve al formatter
    # con feedback, si no, termina.
    graph.add_edge("formatter", "reflector")
    graph.add_conditional_edges(
        "reflector",
        _route_after_reflector,
        {
            "formatter": "formatter",
            END: END,
        },
    )

    graph.add_edge("fuera_de_dominio", END)

    return graph.compile()

agent = build_graph()