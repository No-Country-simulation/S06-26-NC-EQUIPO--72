import asyncio
import logging
import time
import uuid
from fastapi import HTTPException
from langdetect import detect, LangDetectException
from langgraph.types import Command
from openai import APIStatusError, RateLimitError
from app.models.schemas import ConsultaRequest, ConsultaResponse, ResumeRequest
from app.agent.graph import agent, _checkpointer
from app.agent.state import get_tool_results
from app.core.config import settings

logger = logging.getLogger(__name__)


# Session store en memoria — mapea session_id → (thread_id, timestamp).
# Simple dict es suficiente para MVP de una sola instancia y pausas cortas.
_session_store: dict[str, tuple[str, float]] = {}


def _limpiar_sesiones_expiradas() -> list[str]:
    """Devuelve los session_ids expirados (los threads se limpian aparte)."""
    ahora = time.monotonic()
    return [
        sid for sid, (_, creada) in _session_store.items()
        if ahora - creada > settings.hitl_session_ttl_seconds
    ]


async def limpiar_sesiones_expiradas() -> list[str]:
    """Elimina sesiones HITL expiradas del store y sus threads del checkpointer.

    Llamado periódicamente por main.py (loop de background).
    """
    expirados = _limpiar_sesiones_expiradas()
    for sid in expirados:
        thread_id = _session_store.pop(sid, (None, 0))[0]
        if thread_id:
            await _checkpointer.adelete_thread(thread_id)
    return expirados


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
        Procesa una consulta del usuario.

        Si el agente pausa con interrupt() (HITL), devuelve un
        ConsultaResponse con requiere_clarificacion=True, session_id y la
        pregunta/opciones para que Spring Boot la reenvíe al frontend.
        """
        request_id = str(uuid.uuid4())[:8]
        # si no hay idioma explícito (o pidió es), detectar del texto
        idioma = _detectar_idioma(request.consulta, request.idioma or "es")
        logger.info("[%s] CONSULTA | idioma_solicitado=%s | idioma_efectivo=%s",
                    request_id, request.idioma, idioma)
        thread_id = str(uuid.uuid4())
        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": settings.agent_recursion_limit,
        }
        initial_state = {
            "consulta": request.consulta,
            "idioma": idioma,
            "request_id": request_id,
            "filtros": {},
        }
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
                result = await asyncio.wait_for(
                    agent.ainvoke(initial_state, config=config),
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

            # El agente pausó por interrupt(): devolver la pregunta al gestor.
            if "__interrupt__" in result:
                interrupt_data = result["__interrupt__"][0].value
                _session_store[interrupt_data["session_id"]] = (thread_id, time.monotonic())
                logger.info(
                    "[%s] HITL | pausa registrada | session_id=%s",
                    request_id, interrupt_data["session_id"],
                )
                return ConsultaResponse(
                    idioma=idioma,
                    session_id=interrupt_data["session_id"],
                    requiere_clarificacion=True,
                    pregunta_clarificacion=interrupt_data["pregunta_clarificacion"],
                    opciones_clarificacion=interrupt_data.get("opciones_clarificacion"),
                )

            # No pausó: limpiar el thread del checkpointer y seguir el flujo normal.
            await _checkpointer.adelete_thread(thread_id)
            return self._build_response(result)

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

    async def resume_query(self, request: ResumeRequest) -> ConsultaResponse:
        """Reanuda un grafo pausado con la respuesta del gestor."""
        thread_id = _session_store.get(request.session_id, (None, 0))[0]
        if not thread_id:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "SESION_NO_ENCONTRADA",
                    "mensaje": "La sesión expiró o no existe. Enviá la consulta de nuevo.",
                }
            )

        config = {
            "configurable": {"thread_id": thread_id},
            "recursion_limit": settings.agent_recursion_limit,
        }

        try:
            try:
                result = await asyncio.wait_for(
                    agent.ainvoke(Command(resume=request.respuesta_gestor), config=config),
                    timeout=settings.agent_timeout_compuesta,
                )
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=504,
                    detail={
                        "error": "TIMEOUT",
                        "mensaje": "La consulta tardó demasiado al reanudar.",
                    }
                )
            finally:
                # Limpiar el thread pase lo que pase (Corrección 4).
                _session_store.pop(request.session_id, None)
                await _checkpointer.adelete_thread(thread_id)

            return self._build_response(result)

        except HTTPException:
            raise

        except Exception as e:
            logger.exception("Error inesperado reanudando consulta: %s", request.session_id)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "ERROR_INTERNO",
                    "mensaje": "Ocurrió un error reanudando la consulta.",
                }
            )

    def _build_response(self, state: dict) -> ConsultaResponse:
        """Construye la respuesta final a partir del estado del grafo."""
        # Fuera de dominio sigue lanzando 422 (handler existente).
        if state.get("fuera_de_dominio"):
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "CONSULTA_FUERA_DE_DOMINIO",
                    "mensaje": state.get("respuesta_ia"),
                }
            )

        # idioma efectivo conservado en el estado para la reanudación
        idioma = state.get("idioma", "es")

        return ConsultaResponse(
            respuesta_ia=state.get("respuesta_ia", ""),
            datos=get_tool_results(state),  # getter real: garantiza list[dict]
            fuentes=state.get("fuentes", []),
            visualizacion_sugerida=state.get("visualizacion_sugerida", "tabla_datos"),
            idioma=idioma,
        )
