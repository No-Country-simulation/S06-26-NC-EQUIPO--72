import logging

from app.agent.state import AgentState

logger = logging.getLogger(__name__)


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
