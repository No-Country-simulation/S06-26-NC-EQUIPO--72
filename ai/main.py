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


@app.on_event("startup")
async def startup_event():
    """Evento de inicio: inicia el ETL en background y vectorstore con reintentos"""
    thread = threading.Thread(target=run_etl_background, daemon=True)
    thread.start()
    logger.info("ETL iniciado en background - el servicio está listo para recibir peticiones")

    await _init_vectorstore_con_retry()

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