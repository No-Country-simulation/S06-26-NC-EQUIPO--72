import json
import logging
import uuid

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt

from app.agent.prompts import CLARIFICATION_DETECTOR_PROMPT
from app.agent.state import AgentState
from app.agent.retry import llm_retry
from app.agent.output_schemas import ClarificationDecision
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _clarification_models,
    _clarification_fallback_model,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


_PALABRAS_SERVICIO = {
    "MENTORIA": ("mentoría", "mentor", "mentores"),
    "FORMACION": ("formación", "capacitación", "cursos"),
    "EMPLEO": ("empleo", "trabajo", "desempleo"),
    "SALUD_MENTAL": ("salud mental", "psiquiátrica", "internación"),
    "EXPERIENCIA": ("experiencia", "comunitaria", "estructural"),
}


def _evaluar_señales_deterministicas(
    plan: dict,
    consulta: str,
    state: AgentState,
) -> ClarificationDecision | None:
    """
    Evalúa señales de ambigüedad sin LLM.
    Devuelve ClarificationDecision si hay señal clara,
    None si no hay señal (→ evaluar con LLM).
    """
    consulta_lower = consulta.lower()

    # Señal 1: múltiples servicios mencionados, independiente de lo que
    # eligió el planner (Corrección 3). _integrar_respuesta_al_plan
    # sobrescribe con la respuesta del gestor.
    servicios_detectados = [
        s for s, palabras in _PALABRAS_SERVICIO.items()
        if any(p in consulta_lower for p in palabras)
    ]
    if len(servicios_detectados) >= 2:
        opciones = [s.capitalize() for s in servicios_detectados]
        opciones.append("Todos por separado")
        return ClarificationDecision(
            necesita_clarificacion=True,
            pregunta=(
                f"Tu consulta menciona {len(servicios_detectados)} tipos de "
                f"servicio. ¿Cuál querés analizar primero?"
            ),
            opciones=opciones,
            razon="múltiples servicios detectados, planner no resolvió",
        )

    # Señal 2: cluster inter-municipal sin municipio
    if plan.get("cluster") == "ESTREITO_CAPOEIRAS" and not plan.get("municipio"):
        return ClarificationDecision(
            necesita_clarificacion=True,
            pregunta=(
                "ESTREITO_CAPOEIRAS cubre zonas de Florianópolis y São José. "
                "¿Querés ver solo uno de los dos municipios?"
            ),
            opciones=["Florianópolis", "São José", "Ambos"],
            razon="cluster inter-municipal sin municipio especificado",
        )

    # Señal 3: consulta muy corta sin ningún filtro extraído
    tiene_filtro = any([
        plan.get("servicio"), plan.get("municipio"),
        plan.get("cluster"), plan.get("indicador"),
    ])
    if not tiene_filtro and len(consulta.split()) <= 3:
        return ClarificationDecision(
            necesita_clarificacion=True,
            pregunta="¿Sobre qué aspecto de la RM de Florianópolis querés información?",
            opciones=[
                "Brechas de programas sociales",
                "Indicadores de empleo",
                "Salud mental",
                "Conectividad y red",
                "Programas disponibles",
            ],
            razon="consulta demasiado corta sin filtros extraídos",
        )

    return None  # sin señal determinística → evaluar con LLM


def _merece_evaluacion_llm(plan: dict, consulta: str) -> bool:
    """
    Heurística para decidir si vale la pena gastar un LLM call
    en evaluar clarificación. Solo en casos donde hay señales
    de posible ambigüedad no capturada por las reglas determinísticas.
    """
    palabras = consulta.lower().split()
    # Consulta corta sin servicio claro
    if len(palabras) <= 6 and not plan.get("servicio"):
        return True
    # Contiene palabras que sugieren ambigüedad temporal
    _TEMPORAL = ("reciente", "último", "últimos", "nueva", "actual", "hoy")
    if any(p in palabras for p in _TEMPORAL) and not plan.get("fecha"):
        return True
    return False


def _integrar_respuesta_al_plan(
    plan: dict,
    respuesta: str,
    state: AgentState,
) -> dict:
    """
    Integra la respuesta del gestor al plan del planner.
    Mapea respuestas en lenguaje natural a valores canónicos del dominio.
    Si la respuesta no matchea ningún valor conocido, la deja como
    contexto libre en 'razon' para que el schema_linker la use.

    NOTA MVP: una sola oportunidad de clarificación por consulta.
    Si la respuesta del gestor no desambigua completamente, el agente
    continúa con lo que pudo inferir. Una segunda pausa requeriría
    estado adicional en el grafo y está fuera del scope actual.
    """
    plan = dict(plan)
    respuesta_lower = respuesta.lower().strip()

    # La respuesta del gestor es AUTORITATIVA: sobrescribe lo que el planner
    # pudo inferir (Corrección 3). Por eso no hay guard "if not plan.get(...)".
    # Mapeo de servicios (respuestas del gestor → valor canónico)
    _MAPA_SERVICIO = {
        "mentoría": "MENTORIA",
        "mentoria": "MENTORIA",
        "formación": "FORMACION",
        "formacion": "FORMACION",
        "formación técnica": "FORMACION",
        "empleo": "EMPLEO",
        "salud mental": "SALUD_MENTAL",
        "experiencia": "EXPERIENCIA",
        "experiencias": "EXPERIENCIA",
    }
    for texto, valor in _MAPA_SERVICIO.items():
        if texto in respuesta_lower:
            plan["servicio"] = valor
            break

    # Mapeo de municipios
    _MAPA_MUNICIPIO = {
        "florianópolis": "Florianópolis",
        "florianopolis": "Florianópolis",
        "são josé": "São José",
        "sao jose": "São José",
        "palhoça": "Palhoça",
        "palhoca": "Palhoça",
        "biguaçu": "Biguaçu",
        "biguacu": "Biguaçu",
        "ambos": None,  # no filtrar por municipio
    }
    for texto, valor in _MAPA_MUNICIPIO.items():
        if texto in respuesta_lower:
            plan["municipio"] = valor
            break

    # Períodos temporales
    _MAPA_PERIODO = {
        "última semana": None,   # sin filtro de periodo (granularidad diaria)
        "mañana": "MANHA",
        "tarde": "TARDE",
        "noche": "NOITE",
        "madrugada": "MADRUGADA",
    }
    for texto, valor in _MAPA_PERIODO.items():
        if texto in respuesta_lower:
            plan["periodo"] = valor
            break

    # Si "ambas" o "todos" → no filtrar por servicio (análisis general)
    if "ambas" in respuesta_lower or "todos" in respuesta_lower:
        plan["servicio"] = None

    # Siempre agregar la respuesta como contexto adicional
    plan["razon"] = (
        f"{plan.get('razon', '')} | respuesta_gestor: {respuesta}"
    ).strip(" |")

    return plan


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def clarification_detector(state: AgentState) -> AgentState:
    """
    Detecta si la consulta necesita clarificación del gestor.

    Flujo:
    1. Evaluar señales determinísticas (sin LLM, barato)
    2. Si no hay señal: evaluar con LLM light (solo en casos ambiguos)
    3. Si necesita clarificación: interrupt() pausa el grafo
    4. Cuando el gestor responde: el grafo reanuda con respuesta_gestor
       y este nodo integra la respuesta al plan antes de continuar

    Usa su propio session_id — el checkpointer persiste el estado
    completo entre la pausa y la reanudación.
    """
    request_id = state["request_id"]
    consulta = state["consulta"]
    plan = state.get("plan", {})
    respuesta_gestor = state.get("respuesta_gestor")

    # Si ya hay respuesta del gestor (segunda pasada tras reanudación):
    # integrar la respuesta al plan y continuar sin pausar
    if respuesta_gestor:
        logger.info(
            "[%s] CLARIFICATION_DETECTOR | reanudando con respuesta='%s'",
            request_id, str(respuesta_gestor)[:50],
        )
        plan_enriquecido = _integrar_respuesta_al_plan(
            plan, respuesta_gestor, state
        )
        return {
            **state,
            "plan": plan_enriquecido,
            "necesita_clarificacion": False,
            "respuesta_gestor": None,  # limpiar para no re-procesar
        }

    # Primera pasada: evaluar si necesita clarificación

    # Paso 1: señales determinísticas
    decision = _evaluar_señales_deterministicas(plan, consulta, state)

    # Paso 2: si no hay señal determinística, evaluar con LLM
    # Solo si la consulta parece potencialmente ambigua
    if decision is None and _merece_evaluacion_llm(plan, consulta):
        try:
            decision = await _llm_ainvoke_con_fallback(
                _clarification_models, _clarification_fallback_model,
                [
                    SystemMessage(content=CLARIFICATION_DETECTOR_PROMPT),
                    HumanMessage(content=(
                        f"Consulta: {consulta}\n"
                        f"Plan extraído: {json.dumps(plan, ensure_ascii=False)}"
                    ))
                ],
                request_id, "CLARIFICATION_DETECTOR",
            )
            logger.info(
                "[%s] CLARIFICATION_DETECTOR LLM | necesita=%s | razon='%s'",
                request_id,
                decision.necesita_clarificacion,
                decision.razon,
            )
        except Exception as e:
            logger.warning(
                "[%s] CLARIFICATION_DETECTOR LLM error: %s — omitiendo",
                request_id, e,
            )
            decision = ClarificationDecision(
                necesita_clarificacion=False,
                razon="error en detector LLM — continúa sin clarificación",
            )

    # Si no disparó ninguna señal: continuar normal
    if decision is None or not decision.necesita_clarificacion:
        logger.debug(
            "[%s] CLARIFICATION_DETECTOR | sin ambigüedad — continúa",
            request_id,
        )
        return {**state, "necesita_clarificacion": False}

    # Necesita clarificación: pausar con interrupt()
    session_id = str(uuid.uuid4())[:8]
    logger.info(
        "[%s] CLARIFICATION_DETECTOR | pausando | session_id=%s | pregunta='%s'",
        request_id, session_id, decision.pregunta,
    )

    # interrupt() pausa el grafo aquí y persiste el estado completo
    # en el checkpointer. El valor que se pasa es lo que el AI Service
    # devuelve al llamador (Spring Boot) para que lo reenvíe al frontend.
    # Cuando el gestor responde, interrupt() retorna la respuesta_gestor.
    respuesta_del_gestor = interrupt({
        "session_id": session_id,
        "requiere_clarificacion": True,
        "pregunta_clarificacion": decision.pregunta,
        "opciones_clarificacion": decision.opciones,
    })

    # --- El grafo pausa aquí ---
    # Cuando Spring Boot llama a POST /consulta/respuesta con session_id
    # y respuesta_gestor, el grafo reanuda desde esta línea.

    # Integrar la respuesta del gestor al plan
    plan_enriquecido = _integrar_respuesta_al_plan(
        plan, respuesta_del_gestor, state
    )

    logger.info(
        "[%s] CLARIFICATION_DETECTOR | reanudado | respuesta='%s'",
        request_id, str(respuesta_del_gestor)[:50],
    )

    return {
        **state,
        "plan": plan_enriquecido,
        "session_id": session_id,
        "necesita_clarificacion": False,
        "hitl_activado": True,
        "respuesta_gestor": None,
    }
