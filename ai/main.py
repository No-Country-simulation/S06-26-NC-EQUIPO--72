import threading
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middlewares.logging_middleware import LoggingMiddleware
from app.etl.pipeline import run_pipeline

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
    """Ejecuta el ETL en background y actualiza el estado"""
    global etl_status
    etl_status["running"] = True
    etl_status["completed"] = False
    etl_status["error"] = None
    
    try:
        run_pipeline(use_fast_load=True)
        etl_status["completed"] = True
    except Exception as e:
        etl_status["error"] = str(e)
    finally:
        etl_status["running"] = False

@app.on_event("startup")
async def startup_event():
    """Evento de inicio: inicia el ETL en background"""
    thread = threading.Thread(target=run_etl_background, daemon=True)
    thread.start()
    print("ETL iniciado en background - el servicio está listo para recibir peticiones!")

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