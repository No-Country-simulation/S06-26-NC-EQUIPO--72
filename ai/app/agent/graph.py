import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import PLANNER_PROMPT, FORMATTER_PROMPT
from app.agent.tools import consultar_datos, consultar_brechas
from app.core.config import settings

# Estado del grafo
class AgentState(TypedDict):
    consulta: str
    filtros: dict
    idioma: str
    plan: dict
    tool_results: dict
    respuesta_ia: str
    visualizacion_sugerida: str
    fuentes: list

# Modelo
def get_model():
    return ChatOpenAI(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
        temperature=0
    )

# Nodo 1 — Planner
async def planner(state: AgentState) -> AgentState:
    model = get_model()
    response = await model.ainvoke([
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=state["consulta"])
    ])

    try:
        clean = response.content.strip().replace("```json", "").replace("```", "")
        plan = json.loads(clean)
    except Exception:
        plan = {
            "herramientas": ["consultar_datos"],
            "servicio": None,
            "razon": "fallback por error de parseo"
        }

    return { **state, "plan": plan }


# Nodo 2 — Tool Caller
async def tool_caller(state: AgentState) -> AgentState:
    herramientas = state["plan"].get("herramientas", [])
    servicio = state["plan"].get("servicio")
    filtros = state.get("filtros", {})
    results = {}
    fuentes = []

    if "consultar_datos" in herramientas:
        data = await consultar_datos(
            filtros=filtros,
            indicadores=["n_usuarios", "congestionamento_medio"],
            idioma=state["idioma"]
        )
        results["datos"] = data.get("datos", [])
        fuentes.extend(data.get("fuentes", []))

    if "consultar_brechas" in herramientas and servicio:
        brechas = await consultar_brechas(
            servicio=servicio,
            municipio=filtros.get("municipio"),
            periodo=filtros.get("periodo", "TARDE")
        )
        results["brechas"] = brechas.get("brechas", [])

    return { **state, "tool_results": results, "fuentes": fuentes }


# Nodo 3 — Formatter
async def formatter(state: AgentState) -> AgentState:
    model = get_model()

    context = f"""
Consulta original: {state["consulta"]}
Idioma: {state["idioma"]}
Datos retornados: {json.dumps(state["tool_results"], ensure_ascii=False)}
"""

    response = await model.ainvoke([
        SystemMessage(content=FORMATTER_PROMPT),
        HumanMessage(content=context)
    ])

    try:
        clean = response.content.strip().replace("```json", "").replace("```", "")
        result = json.loads(clean)
        respuesta_ia = result.get("respuesta_ia", "No se pudo generar una respuesta.")
        visualizacion = result.get("visualizacion_sugerida", "tabla_datos")
    except Exception:
        respuesta_ia = "No se pudo procesar la consulta."
        visualizacion = "tabla_datos"

    return {
        **state,
        "respuesta_ia": respuesta_ia,
        "visualizacion_sugerida": visualizacion
    }


# Construcción del grafo
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("tool_caller", tool_caller)
    graph.add_node("formatter", formatter)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "tool_caller")
    graph.add_edge("tool_caller", "formatter")
    graph.add_edge("formatter", END)

    return graph.compile()

agent = build_graph()