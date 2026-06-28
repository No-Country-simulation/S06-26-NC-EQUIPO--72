import asyncio
import threading
import traceback
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middlewares.logging_middleware import LoggingMiddleware
from app.etl.pipeline import run_pipeline
from app.vectorstore.indexer import init_vectorstore


app = FastAPI(
    title="App BiT — AI Service",
    description="Agente de IA para consultas en lenguaje natural sobre datos de inclusión social.",
    version="1.0.0"
)

# Agregar middlewares
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
        print(f"[ETL] Error en background: {e}", flush=True)
        traceback.print_exc()
    finally:
        etl_status["running"] = False

async def _init_vectorstore_con_retry(reintentos: int = 5, espera: float = 3.0) -> None:
    for intento in range(1, reintentos + 1):
        try:
            init_vectorstore()
            print("[VectorStore] Inicializado correctamente.", flush=True)
            return
        except Exception as e:
            print(f"[VectorStore] Intento {intento}/{reintentos} fallido: {e}", flush=True)
            if intento < reintentos:
                await asyncio.sleep(espera)
    print("[VectorStore] No se pudo inicializar después de todos los intentos.", flush=True)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio: inicia el ETL en background y vectorstore con reintentos"""
    thread = threading.Thread(target=run_etl_background, daemon=True)
    thread.start()
    print("ETL iniciado en background - el servicio está listo para recibir peticiones", flush=True)

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