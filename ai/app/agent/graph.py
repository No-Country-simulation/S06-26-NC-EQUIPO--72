
import json
import logging
from typing import Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import PLANNER_PROMPT, FORMATTER_PROMPT
from app.agent.schema_linker import schema_linker
from app.agent.tools import llamar_endpoint, ejecutar_sql
from app.agent.state import AgentState
from app.core.config import settings

logger = logging.getLogger(__name__)

# instancia modelo light (Planner y Formatter)
_light_model = ChatOpenAI(
    api_key=settings.groq_api_key_light.get_secret_value(),
    base_url=settings.groq_base_url,
    model=settings.groq_model_light,
    temperature=0,
)

# instancia modelo primary (Tool Calling y SQL)
_primary_model = ChatOpenAI(
    api_key=settings.groq_api_key_primary.get_secret_value(),
    base_url=settings.groq_base_url,
    model=settings.groq_model_primary,
    temperature=0,
)

# Nodo 1 - Planner (usa modelo light)
async def planner(state: AgentState) -> AgentState:
    response = await _light_model.ainvoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=state["consulta"])
    ])
    try:
        clean = response.content.strip().removeprefix("```json").removesuffix("```").strip()
        plan = json.loads(clean)
    except json.JSONDecodeError:
        plan = {"servicio": None, "razon": "fallback por error de parseo"}

    return {**state, "plan": plan}


# Nodo 2 - Tool Caller
async def tool_caller(state: AgentState) -> AgentState:
    """
    Ejecuta la decisión del schema_linker:
    - Si tipo == "endpoint": llama al backend via HTTP
    - Si tipo == "sql": genera SQL con el modelo primary y lo ejecuta
    """

    decision = state["schema_decision"]
    results = {}
    fuentes = []

    if decision["tipo"] == "endpoint":
        data = await llamar_endpoint(
            metodo=decision["metodo"],
            endpoint=decision["endpoint"],
            params=decision["params"],
        )
        results = data.get("resultado", {})
        fuentes = data.get("fuentes", [])

    elif decision["tipo"] == "sql":
        data = await ejecutar_sql(
            consulta=state["consulta"],
            schema_minimo=decision["schema_minimo"],
            model=_primary_model,
        )
        results = data.get("resultado", {})
        fuentes = data.get("fuentes", [])

    return {**state, "tool_results": results, "fuentes": fuentes}



# Nodo 3 - Formatter (usa modelo light)
async def formatter(state: AgentState) -> AgentState:
    context = f"""
Consulta original: {state["consulta"]}
Idioma: {state["idioma"]}
Datos retornados: {json.dumps(state["tool_results"], ensure_ascii=False)}
"""
    response = await _light_model.ainvoke([
        SystemMessage(content=FORMATTER_PROMPT),
        HumanMessage(content=context)
    ])
    try:
        clean = response.content.strip().removeprefix("```json").removesuffix("```").strip()
        result = json.loads(clean)
        respuesta_ia = result.get("respuesta_ia", "No se pudo generar una respuesta.")
        visualizacion = result.get("visualizacion_sugerida", "tabla_datos")
    except json.JSONDecodeError:
        respuesta_ia = "No se pudo procesar la consulta."
        visualizacion = "tabla_datos"

    return {**state, "respuesta_ia": respuesta_ia, "visualizacion_sugerida": visualizacion}




# Construcción del grafo
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("schema_linker", schema_linker)
    graph.add_node("tool_caller", tool_caller)
    graph.add_node("formatter", formatter)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "schema_linker")
    graph.add_edge("schema_linker", "tool_caller")
    graph.add_edge("tool_caller", "formatter")
    graph.add_edge("formatter", END)

    return graph.compile()

agent = build_graph()
