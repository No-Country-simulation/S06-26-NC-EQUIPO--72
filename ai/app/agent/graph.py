import json
import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import PLANNER_PROMPT, FORMATTER_PROMPT
from app.agent.schema_linker import schema_linker
from app.agent.tools import llamar_endpoint, ejecutar_sql
from app.agent.state import AgentState
from app.core.config import settings
from app.agent.normalizer import normalizar_plan


logger = logging.getLogger(__name__)


def _json_default(obj: Any) -> Any:
    """
    Convierte tipos que json.dumps no soporta nativamente pero que
    MySQL/aiomysql devuelven con frecuencia: TIME -> timedelta,
    DATE/DATETIME -> date/datetime, DECIMAL -> Decimal.
    """
    if isinstance(obj, timedelta):
        # timedelta representa TIME en MySQL - lo pasamos a "HH:MM:SS"
        total_seconds = int(obj.total_seconds())
        horas, resto = divmod(total_seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


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
        plan = normalizar_plan(plan)  # <-- corrección determinística post-LLM
    except json.JSONDecodeError:
        plan = {"servicio": None, "fuera_de_dominio": False, "razon": "fallback por error de parseo"}

    return {**state, "plan": plan}


def _route_after_planner(state: AgentState) -> str:
    """
    Decide si la consulta sigue el flujo normal (schema_linker -> tool_caller)
    o corta directo a una respuesta de fuera de dominio, sin gastar llamadas
    de más a Qdrant, al backend o al modelo de text-to-SQL.
    """
    if state.get("plan", {}).get("fuera_de_dominio"):
        return "fuera_de_dominio"
    return "schema_linker"


# Nodo - Fuera de dominio (corta el flujo temprano, sin tools ni SQL)
async def fuera_de_dominio_node(state: AgentState) -> AgentState:
    idioma = state.get("idioma", "es")
    mensaje = _MENSAJE_FUERA_DE_DOMINIO.get(idioma, _MENSAJE_FUERA_DE_DOMINIO["es"])
    razon = state.get("plan", {}).get("razon", "")
    logger.info("Consulta fuera de dominio detectada. Razón: %s", razon)

    return {
        **state,
        "fuera_de_dominio": True,
        "respuesta_ia": mensaje,
    }

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
        if decision["endpoint"] == "/brechas":
            print(
                f"\nENDPOINT '/brechas' NO DISPONIBLE (todavía no está implementado).\n",
                flush=True,
            )
            logger.warning(
                "Endpoint /brechas solicitado pero no está disponible.",
            )
            results = {
                "error": "El endpoint /brechas todavía no está disponible. El equipo está trabajando en él.",
                "endpoint_solicitado": decision["endpoint"],
            }
            fuentes = []
        else:
            # Todos los demás endpoints están activados
            data = await llamar_endpoint(
                metodo=decision["metodo"],
                endpoint=decision["endpoint"],
                params=decision["params"],
            )
            results = data.get("resultado", {})
            fuentes = data.get("fuentes", [])

    elif decision["tipo"] == "sql":
        plan = state.get("plan", {})
        data = await ejecutar_sql(
            consulta=state["consulta"],
            schema_minimo=decision["schema_minimo"],
            model=_primary_model,
            fecha=plan.get("fecha"),
            filtros={
                "municipio": plan.get("municipio"),
                "cluster": plan.get("cluster"),
                "periodo": plan.get("periodo"),
                "income_cluster": plan.get("income_cluster"),
                "servicio": plan.get("servicio"),
            },
        )
        results = data.get("resultado", {})
        fuentes = data.get("fuentes", [])

    return {**state, "tool_results": results, "fuentes": fuentes}



# Nodo 3 - Formatter (usa modelo light)
async def formatter(state: AgentState) -> AgentState:
    context = f"""
Consulta original: {state["consulta"]}
Idioma: {state["idioma"]}
Datos retornados: {json.dumps(state["tool_results"], ensure_ascii=False, default=_json_default)}
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
    graph.add_node("fuera_de_dominio", fuera_de_dominio_node)
    graph.add_node("schema_linker", schema_linker)
    graph.add_node("tool_caller", tool_caller)
    graph.add_node("formatter", formatter)

    graph.set_entry_point("planner")

    # Routing condicional: si es fuera de dominio, corta directo a END
    # sin pasar por schema_linker/tool_caller/formatter.
    graph.add_conditional_edges(
        "planner",
        _route_after_planner,
        {
            "schema_linker": "schema_linker",
            "fuera_de_dominio": "fuera_de_dominio",
        },
    )

    graph.add_edge("schema_linker", "tool_caller")
    graph.add_edge("tool_caller", "formatter")
    graph.add_edge("formatter", END)
    graph.add_edge("fuera_de_dominio", END)

    return graph.compile()

agent = build_graph()