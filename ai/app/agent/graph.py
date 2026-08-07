"""
Ensamblador del grafo multi-agente.

Este módulo ORQUESTA los nodos (que viven en `app.agent.nodes`) y la capa de
LLMs (`app.agent.llm_layer`) / parsing (`app.agent.parsing`), construye el
grafo con langgraph y expone el agente compilado.

Re-exporta los símbolos públicos y privados que consumen el resto del sistema
(ai_service, conftest, evals, tests) para no romper imports existentes:
  - agent, _checkpointer      -> app/services/ai_service.py
  - build_graph               -> conftest.py, evals/run_evals.py
  - _route_*                  -> tests/test_routing.py, test_guardrails.py
  - _aplicar_correccion_react -> tests/test_routing.py
  - _gate_reflexion           -> tests/test_routing.py
  - _evaluar_señales_*        -> tests/test_clarification_detector.py
  - _extraer_json_con_fallback-> tests/test_extraer_json.py
  - _llm_ainvoke_con_fallback -> tests/test_llm_fallback.py
"""
import logging

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

from app.agent.state import AgentState
from app.agent.guardrails import input_guardrail, output_guardrail
from app.agent.schema_linker import schema_linker

# Nodos individuales
from app.agent.nodes.planner import (
    planner,
    _parse_bool,
    _parse_nullable,
    _run_dspy_async,
    _plan_via_dspy,
    _plan_desde_prediccion,
)
from app.agent.nodes.fuera_de_dominio import fuera_de_dominio_node, _MENSAJE_FUERA_DE_DOMINIO
from app.agent.nodes.clarification import (
    clarification_detector,
    _PALABRAS_SERVICIO,
    _evaluar_señales_deterministicas,
    _merece_evaluacion_llm,
    _integrar_respuesta_al_plan,
)
from app.agent.nodes.classifier import query_classifier
from app.agent.nodes.decomposer import task_decomposer
from app.agent.nodes.executor import parallel_executor, result_merger
from app.agent.nodes.tool_caller import tool_caller, react_reasoner, _aplicar_correccion_react
from app.agent.nodes.formatter import formatter, _corregir_visualizacion
from app.agent.nodes.reflector import reflector, _gate_reflexion
from app.agent.nodes.routing import (
    _route_after_input_guardrail,
    _route_after_planner,
    _route_after_classifier,
    _route_after_task_decomposer,
    _route_after_tool_caller,
    _route_after_reflector,
)

# Capas de soporte
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _nombre_modelo,
    _construir_chain,
    _structured_chain,
)
from app.agent.parsing import _extraer_json_con_fallback

logger = logging.getLogger(__name__)


# Checkpointer global de producción — una sola instancia que vive mientras
# el proceso FastAPI corre. Es REQUERIDO para que interrupt() funcione
# (HITL). Evals y tests pasan su propia instancia via build_graph(checkpointer=...).
_checkpointer = InMemorySaver()


# Construcción del grafo
def build_graph(checkpointer=None):
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("fuera_de_dominio", fuera_de_dominio_node)
    graph.add_node("input_guardrail", input_guardrail)
    graph.add_node("output_guardrail", output_guardrail)
    graph.add_node("clarification_detector", clarification_detector)
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
    # Si no, pasa por el clarification_detector (que evalúa ambigüedad y
    # puede pausar con interrupt() para pedir clarificación al gestor).
    graph.add_conditional_edges(
        "planner",
        _route_after_planner,
        {
            "query_classifier": "clarification_detector",
            "fuera_de_dominio": "fuera_de_dominio",
        },
    )

    graph.add_edge("clarification_detector", "query_classifier")

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

    return graph.compile(checkpointer=checkpointer or _checkpointer)


agent = build_graph()
