from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.middlewares.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="App BiT — AI Service",
    description="Agente de IA para consultas en lenguaje natural sobre datos de inclusión social.",
    version="1.0.0"
)

# Agregar middlewares
app.add_middleware(LoggingMiddleware)

app.include_router(router)

@app.get("/health")
def health():
    return { "status": "ok", "backend_url": settings.backend_url }