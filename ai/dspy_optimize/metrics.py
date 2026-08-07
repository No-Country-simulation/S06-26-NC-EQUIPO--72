"""
Metric functions para MIPROv2.
Cada metric mide la accuracy de un nodo específico del agente.
Todas devuelven float entre 0.0 y 1.0.
"""
import unicodedata
from typing import Any


def _normalizar_str(s: str | None) -> str:
    if s is None:
        return ""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", str(s))
        if unicodedata.category(c) != "Mn"
    )
    return sin_acentos.strip().lower()


def planner_metric(example: Any, prediction: Any, trace=None) -> float:
    """
    Mide la accuracy del planner sobre múltiples campos.
    Peso por importancia: servicio > municipio > fuera_de_dominio > resto.
    """
    score = 0.0
    max_score = 0.0

    # fuera_de_dominio (peso 2)
    max_score += 2
    pred_fod = getattr(prediction, "fuera_de_dominio", None)
    expected_fod = example.get("fuera_de_dominio", False)
    if str(pred_fod).lower() == str(expected_fod).lower():
        score += 2

    # servicio (peso 3 — el campo más importante)
    max_score += 3
    if _normalizar_str(getattr(prediction, "servicio", None)) == _normalizar_str(
        example.get("servicio")
    ):
        score += 3

    # municipio (peso 2)
    max_score += 2
    if _normalizar_str(getattr(prediction, "municipio", None)) == _normalizar_str(
        example.get("municipio")
    ):
        score += 2

    # indicador (peso 2)
    max_score += 2
    if _normalizar_str(getattr(prediction, "indicador", None)) == _normalizar_str(
        example.get("indicador")
    ):
        score += 2

    # cluster (peso 1)
    max_score += 1
    if _normalizar_str(getattr(prediction, "cluster", None)) == _normalizar_str(
        example.get("cluster")
    ):
        score += 1

    # periodo (peso 1)
    max_score += 1
    if _normalizar_str(getattr(prediction, "periodo", None)) == _normalizar_str(
        example.get("periodo")
    ):
        score += 1

    # income_cluster (peso 1)
    max_score += 1
    if _normalizar_str(getattr(prediction, "income_cluster", None)) == _normalizar_str(
        example.get("income_cluster")
    ):
        score += 1

    return score / max_score if max_score > 0 else 0.0


def query_classifier_metric(example: Any, prediction: Any, trace=None) -> float:
    """
    Mide la accuracy del query_classifier.
    query_type tiene más peso que merge_strategy (que es secundario).
    """
    score = 0.0

    # query_type (peso 3)
    pred_qt = _normalizar_str(getattr(prediction, "query_type", None))
    exp_qt = _normalizar_str(example.get("query_type"))
    if pred_qt == exp_qt:
        score += 3

    # merge_strategy (peso 1 — solo si query_type es compuesta)
    if exp_qt == "compuesta":
        pred_ms = _normalizar_str(getattr(prediction, "merge_strategy", None))
        exp_ms = _normalizar_str(example.get("merge_strategy"))
        if pred_ms == exp_ms:
            score += 1
        return score / 4

    return score / 3


def clarification_detector_metric(
    example: Any, prediction: Any, trace=None
) -> float:
    """
    Mide la accuracy del clarification_detector.
    Penaliza fuertemente los falsos positivos (pausa innecesaria)
    porque son peor UX que no pausar.
    """
    pred_nc = str(getattr(prediction, "necesita_clarificacion", "false")).lower()
    exp_nc = str(example.get("necesita_clarificacion", False)).lower()

    if pred_nc == exp_nc:
        return 1.0

    # Falso positivo (pausó cuando no debía) → penalización máxima
    if pred_nc == "true" and exp_nc == "false":
        return 0.0

    # Falso negativo (no pausó cuando debía) → penalización media.
    # Es mejor que pausar innecesariamente, así que no es 0.
    return 0.4
