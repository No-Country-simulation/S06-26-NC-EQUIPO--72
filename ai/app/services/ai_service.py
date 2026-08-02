import asyncio
import logging
import uuid
from fastapi import HTTPException
from langdetect import detect, LangDetectException
from openai import APIStatusError, RateLimitError
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.agent.graph import agent
from app.agent.state import get_tool_results
from app.core.config import settings

logger = logging.getLogger(__name__)


# pre-clasificación determinística SIN LLM para elegir el timeout
# antes del ainvoke (el query_classifier corre dentro del grafo).
_PALABRAS_COMPUESTA = (
    " y ", " and ", "además", "también", "relación", "correlación",
    "junto", "combinado", "al mismo tiempo", "tanto",
)


def _es_probablemente_compuesta(consulta: str) -> bool:
    lower = consulta.lower()
    return any(p in lower for p in _PALABRAS_COMPUESTA)


def _detectar_idioma(consulta: str, idioma_solicitado: str) -> str:
    """
    Auto-detección de idioma.
    - Si el usuario pidió explícitamente pt o en, se respeta.
    - Si pidió es (o no especificó), se detecta del texto: si el texto real
      está en pt/en, se usa ese. Default: es.
    """
    if idioma_solicitado in ("pt", "en"):
        return idioma_solicitado  # explícito no español -> respetar
    try:
        detectado = detect(consulta)
        if detectado in ("es", "pt", "en"):
            return detectado
    except LangDetectException:
        pass
    return "es"  # default



class AIService:
    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Procesa una consulta del usuario
        """
        request_id = str(uuid.uuid4())[:8]
        # si no hay idioma explícito (o pidió es), detectar del texto
        idioma = _detectar_idioma(request.consulta, request.idioma)
        logger.info("[%s] CONSULTA | idioma_solicitado=%s | idioma_efectivo=%s",
                    request_id, request.idioma, idioma)
        try:
            # timeout global por pre-clasificación (sin LLM).
            # simple = agent_timeout_simple (falla rápido bajo rate limiting);
            # compuesta = agent_timeout_compuesta (sub-agentes paralelos).
            timeout = (
                settings.agent_timeout_compuesta
                if _es_probablemente_compuesta(request.consulta)
                else settings.agent_timeout_simple
            )
            try:
                state = await asyncio.wait_for(
                    agent.ainvoke(
                        {
                            "consulta": request.consulta,
                            "idioma": idioma,
                            "request_id": request_id,
                            "filtros": {},
                        },
                        config={"recursion_limit": settings.agent_recursion_limit},
                    ),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                logger.error("[%s] Timeout global (%.0fs)", request_id, timeout)
                raise HTTPException(
                    status_code=504,
                    detail={
                        "error": "TIMEOUT",
                        "mensaje": (
                            "La consulta tardó demasiado. "
                            "Intentá con una consulta más específica."
                        ),
                    }
                )

            if state.get("fuera_de_dominio"):
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "CONSULTA_FUERA_DE_DOMINIO",
                        "mensaje": state.get("respuesta_ia"),
                    }
                )
            
            # Extrae los datos de la respuesta
            # get_tool_results garantiza list[dict]
            datos = get_tool_results(state)

            return ConsultaResponse(
                respuesta_ia=state.get("respuesta_ia", ""),
                datos=datos,
                fuentes=state.get("fuentes", []),
                visualizacion_sugerida=state.get("visualizacion_sugerida", "tabla_datos"),
                idioma=idioma,
            )

        except HTTPException:
            raise  # re-lanza HTTPExceptions sin modificar

        except RateLimitError as e:
            # Groq (free tier) limita por TPM (ventana ~60s). Los retries
            # de tenacity (1-8s) no alcanzan a esperar la ventana, así que
            # tras agotarlos degradamos a 503 con mensaje de reintento.
            logger.warning(
                "Rate limit de Groq tras retries: %s", request.consulta
            )
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "IA_SATURADA",
                    "mensaje": (
                        "El servicio de IA está momentáneamente saturado "
                        "por límites de uso. Por favor, reintentá en unos "
                        "segundos."
                    ),
                },
            )

        except APIStatusError as e:
            # Defensa extra: un 413 (request demasiado grande para el TPM
            # del modelo) no se resuelve con retries. Degradar con 503 en
            # vez de 500.
            logger.warning(
                "Groq rechazó la llamada (status=%s): %s",
                e.status_code, request.consulta,
            )
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "IA_SATURADA",
                    "mensaje": (
                        "El servicio de IA no pudo procesar la consulta por "
                        "límites de uso. Probá reformularla en términos más "
                        "acotados."
                    ),
                },
            )

        except Exception as e:
            logger.exception("Error inesperado procesando consulta: %s", request.consulta)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "ERROR_INTERNO",
                    "mensaje": "Ocurrió un error procesando la consulta.",
                }
            )
