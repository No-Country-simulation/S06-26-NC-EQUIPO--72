import json
import logging
import re

logger = logging.getLogger(__name__)


def _extraer_json_con_fallback(raw: str, request_id: str = "-") -> dict:
    """
    Intenta extraer JSON válido de la respuesta del LLM.
    Estrategia: parseo directo -> regex -> plan vacío seguro.
    El fallback nunca tira todo el pipeline (Fix Bug C).
    """
    # Intento 1: parseo limpio directo
    if not isinstance(raw, str) or not raw.strip():
        logger.warning("[%s] Planner devolvió respuesta vacía o inválida", request_id)
        return {
            "fuera_de_dominio": False,
            "servicio": None,
            "municipio": None,
            "periodo": None,
            "cluster": None,
            "income_cluster": None,
            "indicador": None,
            "fecha": None,
            "razon": "fallback por respuesta vacía",
        }
    cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Intento 2: extraer el primer objeto JSON con regex
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group())
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    # Intento 3: plan vacío seguro- nunca tirar todo el pipeline
    logger.warning("[%s] Planner no pudo producir JSON válido. Raw: %s",
                   request_id, raw[:300])
    return {
        "fuera_de_dominio": False,
        "servicio": None,
        "municipio": None,
        "periodo": None,
        "cluster": None,
        "income_cluster": None,
        "indicador": None,
        "fecha": None,
        "razon": "fallback por error de parseo",
    }
