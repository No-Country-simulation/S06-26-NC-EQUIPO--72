import logging

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Errores transitorios típicos de la API (Groq): rate limit, 5xx y red.
# NO se reintenta sobre errores determinísticos (pydantic, programming errors)
# porque reintentar ahí no ayuda y desperdicia llamadas.
_LLM_RETRYABLE = (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)


def llm_retry(max_attempts: int = 3):
    """Decorator de retry para llamadas LLM (errores transitorios de API)."""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(_LLM_RETRYABLE),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


def http_retry(max_attempts: int = 2):
    """Decorator de retry para llamadas HTTP al backend (errores de red/5xx)."""
    import httpx

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type(httpx.HTTPError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
