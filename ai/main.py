import asyncio
import logging
import threading
import traceback
from fastapi import FastAPI
from app.core.config import settings
from app.core.observability import setup_observability


logger = logging.getLogger(__name__)


# Configura logging ANTES de setup_observability para que sus INFO se vean.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

# Activa LangSmith ANTES de importar el grafo - el tracer lee las env vars
# al construirse, así que esto tiene que correr antes de graph.py.
setup_observability()


from app.api.routes import router
from app.middlewares.logging_middleware import LoggingMiddleware
from app.etl.pipeline import run_pipeline
from app.vectorstore.indexer import init_vectorstore
from app.services.ai_service import limpiar_sesiones_expiradas
from app.core.config import settings


app = FastAPI(
    title="App BiT - AI Service",
    description="Agente de IA para consultas en lenguaje natural sobre datos de inclusión social.",
    version="1.0.0"
)

app.add_middleware(LoggingMiddleware)

app.include_router(router)

# Estado del ETL
etl_status = {
    "running": False,
    "completed": False,
    "error": None
}

def run_etl_background():
    global etl_status
    etl_status["running"] = True
    etl_status["completed"] = False
    etl_status["error"] = None
    
    try:
        run_pipeline()
        etl_status["completed"] = True
    except Exception as e:
        etl_status["error"] = str(e)
        logger.error("[ETL] Error en background: %s", e)
        traceback.print_exc()
    finally:
        etl_status["running"] = False

async def _init_vectorstore_con_retry(reintentos: int = 5, espera: float = 3.0) -> None:
    for intento in range(1, reintentos + 1):
        try:
            init_vectorstore()
            logger.info("[VectorStore] Inicializado correctamente.")
            return
        except Exception as e:
            logger.warning("[VectorStore] Intento %d/%d fallido: %s", intento, reintentos, e)
            if intento < reintentos:
                await asyncio.sleep(espera)
    logger.error("[VectorStore] No se pudo inicializar después de todos los intentos.")


_cleanup_task: asyncio.Task | None = None


async def _session_cleanup_loop() -> None:
    """Loop en background: elimina sesiones HITL expiradas y sus threads."""
    while True:
        await asyncio.sleep(settings.hitl_cleanup_interval_seconds)
        try:
            limpiadas = await limpiar_sesiones_expiradas()
            if limpiadas:
                logger.info("Sesiones HITL expiradas limpiadas: %s", limpiadas)
        except Exception as e:  # noqa: BLE001
            logger.warning("Error en limpieza de sesiones HITL: %s", e)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio: inicia el ETL en background y vectorstore con reintentos"""
    thread = threading.Thread(target=run_etl_background, daemon=True)
    thread.start()
    logger.info("ETL iniciado en background - el servicio está listo para recibir peticiones")

    await _init_vectorstore_con_retry()

    # Limpieza periódica de sesiones HITL expiradas (Corrección 4).
    global _cleanup_task
    _cleanup_task = asyncio.create_task(_session_cleanup_loop())
    logger.info("Limpieza de sesiones HITL iniciada (cada %ds, TTL %ds)",
                settings.hitl_cleanup_interval_seconds,
                settings.hitl_session_ttl_seconds)


@app.on_event("shutdown")
async def shutdown_event():
    if _cleanup_task is not None:
        _cleanup_task.cancel()


@app.get("/health")
def health():
    return { 
        "status": "ok", 
        "backend_url": settings.backend_url,
        "etl": etl_status 
    }

@app.get("/etl/status")
def get_etl_status():
    """Obtiene el estado actual del ETL"""
    return {
        "status": etl_status
    }