import logging
import os

from app.core.config import settings


logger = logging.getLogger(__name__)


def setup_observability() -> None:
    """
    Activa el tracing de LangSmith si está configurado.

    Debe ejecutarse ANTES de construir el grafo: las variables de entorno
    se leen al inicializar el tracer, así que si esto corre después del
    import de graph.py, los spans no se van a emitir.
    """
    if settings.langsmith_tracing and settings.langsmith_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = (
            settings.langsmith_api_key.get_secret_value()
        )
        os.environ["LANGCHAIN_PROJECT"] = settings.langsmith_project
        logger.info("LangSmith tracing activado- proyecto: %s",
                    settings.langsmith_project)
    else:
        logger.info("LangSmith tracing desactivado")
