import logging

from langchain_openai import ChatOpenAI
from openai import RateLimitError

from app.agent.output_schemas import (
    PlanOutput,
    QueryClassification,
    TaskDecomposition,
    ReflectionOutput,
    FormatterOutput,
    ClarificationDecision,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


# Pool de cuentas Groq (rotación). Cada clave del pool es una cuenta con su
# propia cuota diaria de TPM/TPD: ante un 429 (limite de requests o de tokens
# por dia agotado), los nodos rotan a la siguiente clave antes de degradar al
# fallback Gemini. El pool lo arma settings.claves_groq() a partir de las
# claves primary/light/extra del .env + GROQ_API_KEYS_ROTACION.
_claves_groq = settings.claves_groq()


def _construir_chain(modelo: str) -> list[ChatOpenAI]:
    """Una instancia ChatOpenAI por cuenta Groq (mismo modelo, key distinta).

    max_retries=0: el cliente openai reintenta internamente con backoff que
    puede llegar a 54s en un 429 (rate limit de Groq), comiéndose el timeout
    global. Con 0, el RateLimitError propaga a _llm_ainvoke_con_fallback
    (rotación de cuentas) y luego a @llm_retry (tenacity, 1-8s).
    """
    return [
        ChatOpenAI(api_key=k, base_url=settings.groq_base_url, model=modelo,
                   temperature=0, max_retries=0)
        for k in _claves_groq
    ]


_light_models = _construir_chain(settings.groq_model_light)
_primary_models = _construir_chain(settings.groq_model_primary)

# Modelo fallback (Gemini 2.0 Flash Lite vía el endpoint OpenAI-compatible de
# Google). Pool de límites independiente de Groq: cuando cualquier modelo de
# Groq rate-limita (429 TPM/TPD), los nodos pasan a este en vez de esperar.
_fallback_model = ChatOpenAI(
    api_key=settings.google_api_key.get_secret_value(),
    base_url=settings.gemini_base_url,
    model=settings.gemini_model_fallback,
    temperature=0,
    max_retries=0,
)

# Versiones con structured output (json_mode soportado por Groq).
# Una por cada cuenta del pool: la cadena rota la consulta a la siguiente
# cuenta ante un 429.
def _structured_chain(modelos: list, schema) -> list:
    return [m.with_structured_output(schema, method="json_mode")
            for m in modelos]


_planner_models = _structured_chain(_light_models, PlanOutput)
_classifier_models = _structured_chain(_primary_models, QueryClassification)
_decomposer_models = _structured_chain(_primary_models, TaskDecomposition)
_reflector_models = _structured_chain(_primary_models, ReflectionOutput)
_formatter_models = _structured_chain(_light_models, FormatterOutput)
_clarification_models = _structured_chain(_light_models, ClarificationDecision)

# Fallback (Gemini) con structured output para cada nodo: se activa ante un
# 429 de Groq (TPM o TPD). Gemini 2.0 Flash Lite soporta response_format
# json_object en su endpoint OpenAI-compatible.
_planner_fallback_model = _fallback_model.with_structured_output(
    PlanOutput, method="json_mode"
)
_classifier_fallback_model = _fallback_model.with_structured_output(
    QueryClassification, method="json_mode"
)
_decomposer_fallback_model = _fallback_model.with_structured_output(
    TaskDecomposition, method="json_mode"
)
_reflector_fallback_model = _fallback_model.with_structured_output(
    ReflectionOutput, method="json_mode"
)
_formatter_fallback_model = _fallback_model.with_structured_output(
    FormatterOutput, method="json_mode"
)
_clarification_fallback_model = _fallback_model.with_structured_output(
    ClarificationDecision, method="json_mode"
)


async def _llm_ainvoke_con_fallback(modelos, modelo_fallback, mensajes,
                                    request_id: str, nodo: str):
    """Invoca el modelo con rotación de cuentas Groq: ante un 429 (limite de
    requests o de tokens por dia agotado) usa la siguiente cuenta del pool;
    si todas agotan, usa el fallback (pool de límites separado, Gemini).

    Si el fallback también falla, la excepción propaga a @llm_retry (tenacity),
    que reintenta todo el nodo con esperas acotadas 1-8s.
    """
    if not isinstance(modelos, (list, tuple)):
        modelos = [modelos]
    ultimo_error = None
    for modelo in modelos:
        if modelo is None:
            continue
        try:
            return await modelo.ainvoke(mensajes)
        except RateLimitError as e:
            ultimo_error = e
            logger.warning("[%s] %s | rate limit en %s- probando siguiente cuenta Groq",
                           request_id, nodo, _nombre_modelo(modelo))
    if not ultimo_error:
        raise RuntimeError("sin modelos válidos para invocar")
    logger.warning("[%s] %s | todas las cuentas Groq rate-limit - fallback a %s",
                   request_id, nodo, _nombre_modelo(modelo_fallback))
    return await modelo_fallback.ainvoke(mensajes)


def _nombre_modelo(modelo) -> str:
    """Nombre del modelo base, incluso dentro del wrapper de structured output."""
    nombre = getattr(modelo, "model_name", None)
    if nombre:
        return nombre
    for paso in getattr(modelo, "steps", []) or []:
        bound = getattr(paso, "bound", None)
        nombre = getattr(bound, "model_name", None)
        if nombre:
            return nombre
    return "?"
