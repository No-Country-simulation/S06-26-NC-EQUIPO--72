"""
Configuración central de DSPy para App BiT.

Regla: DSPy se configura una vez al importar este módulo.
Todos los módulos DSPy importan desde acá — nunca llaman
dspy.configure() en sus propios archivos.
"""
import logging
import threading
import time

import dspy
from app.core.config import settings

logger = logging.getLogger(__name__)

# LMs configurados por tier.
# CORRECCIÓN: dspy 3.x enruta por litellm. Para Groq, el proveedor es
# "groq/" + el id COMPLETO del modelo ("openai/gpt-oss-120b"). Sin el
# prefijo "groq/", litellm va a api.openai.com y falla; sin el namespace
# "openai/" dentro del id, Groq responde model_not_found.


class _RotatingLM(dspy.LM):
    """dspy.LM que rota la api_key entre cuentas Groq ante un
    `LMRateLimitError` (429 — limite de requests o de tokens por dia
    agotado). Suma la cuota TPM/TPD de cada cuenta del pool
    (`settings.claves_groq()`). Solo para la compilación offline (MIPROv2);
    el runtime usa la rotación de graph.py.
    """

    def __init__(self, model: str, api_keys: list[str], **kwargs):
        if not api_keys:
            raise ValueError("_RotatingLM requiere al menos una api_key")
        self._api_keys = list(api_keys)
        self._idx = 0
        self._lock = threading.Lock()
        super().__init__(model=model, api_key=self._api_keys[0], **kwargs)

    def _usar_siguiente(self) -> bool:
        with self._lock:
            if len(self._api_keys) <= 1:
                return False
            self._idx = (self._idx + 1) % len(self._api_keys)
            self.kwargs["api_key"] = self._api_keys[self._idx]
            self.api_key = self._api_keys[self._idx]
            return True

    def _rotar_si_rate_limit(self, e, intento: int) -> bool:
        if not isinstance(e, dspy.LMRateLimitError):
            return False
        if intento >= len(self._api_keys) - 1:
            return False
        self._usar_siguiente()
        logger.warning("dspy | rate limit - rotando a cuenta %d/%d",
                       self._idx + 1, len(self._api_keys))
        return True

    def forward(self, prompt=None, messages=None, **kwargs):
        for intento in range(len(self._api_keys)):
            try:
                return super().forward(prompt=prompt, messages=messages, **kwargs)
            except Exception as e:  # noqa: BLE001
                if not self._rotar_si_rate_limit(e, intento):
                    raise
        raise RuntimeError("agotadas las cuentas")  # pragma: no cover

    async def aforward(self, prompt=None, messages=None, **kwargs):
        for intento in range(len(self._api_keys)):
            try:
                return await super().aforward(prompt=prompt, messages=messages, **kwargs)
            except Exception as e:  # noqa: BLE001
                if not self._rotar_si_rate_limit(e, intento):
                    raise
        raise RuntimeError("agotadas las cuentas")  # pragma: no cover


_primary_lm = _RotatingLM(
    model=f"groq/{settings.groq_model_primary}",
    api_keys=settings.claves_groq(),
    temperature=0,
    cache=False,
    num_retries=1,
)

_light_lm = _RotatingLM(
    model=f"groq/{settings.groq_model_light}",
    api_keys=settings.claves_groq(),
    temperature=0,
    cache=False,
    num_retries=1,
)

# NOTA: el fallback real Groq→Gemini no pasa por DSPy — vive en
# _llm_ainvoke_con_fallback() (graph.py). Este LM existe para la
# compilación offline (MIPROv2) usando el tier gratis de Gemini
# (gemini-3.1-flash-lite: 500 RPD / 250K TPM) sin gastar la cuota
# diaria de Groq. No se usa en producción.
_gemini_lm = dspy.LM(
    model=f"gemini/{settings.gemini_model_fallback}",
    api_key=settings.google_api_key.get_secret_value(),
    temperature=0,
    cache=False,
    num_retries=30,
)

# Gemini free tier: 15 RPM duro (hard platform limit). dspy 3.3.0 NO
# implementa max_requests_per_minute (se ignora). MIPROv2 dispara llamadas
# en ráfaga (proposals en threads propios) → se envuelve forward con
# spacing global estricto de 4.5s (13.3 RPM) para no tocar el 429 de cuota.
_GEMINI_MIN_INTERVAL = 4.5
_gemini_lock = threading.Lock()
_gemini_last = [0.0]


def _gemini_paced(*args, **kwargs):
    with _gemini_lock:
        now = time.time()
        wait = _GEMINI_MIN_INTERVAL - (now - _gemini_last[0])
        if wait > 0:
            time.sleep(wait)
        _gemini_last[0] = time.time()
    return _gemini_orig_forward(*args, **kwargs)


_gemini_orig_forward = _gemini_lm.forward
_gemini_lm.forward = _gemini_paced

_fallback_lm = _gemini_lm

# Configuración global — usa el light como default.
# Los módulos que necesitan primary lo setean explícitamente.
dspy.configure(lm=_light_lm)


def get_primary_lm() -> dspy.LM:
    return _primary_lm


def get_light_lm() -> dspy.LM:
    return _light_lm


def get_fallback_lm() -> dspy.LM:
    return _fallback_lm


def get_gemini_lm() -> dspy.LM:
    """Gemini free tier (gemini-3.1-flash-lite). Uso offline (compilación
    MIPROv2) para no gastar la cuota diaria de Groq. 500 RPD / 250K TPM."""
    return _gemini_lm
