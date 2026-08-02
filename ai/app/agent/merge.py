import logging

logger = logging.getLogger(__name__)


def _merge_join(
    results_a: list[dict],
    results_b: list[dict],
    join_key: str,
) -> list[dict]:
    """
    Join exacto por join_key (típicamente "cluster").
    Python puro, sin LLM, determinístico.
    Incluye todos los registros de A, enriquecidos con datos de B.
    Registros de A sin match en B se incluyen con campos de B ausentes.

    Validación en runtime: si join_key no existe en alguna de las fuentes,
    se loguea un ERROR y se devuelve A sin merge (fallback explícito).
    Nunca un join vacío silencioso.
    """
    if results_a and join_key not in results_a[0]:
        logger.error("join_key '%s' no existe en fuente A. Campos: %s",
                     join_key, list(results_a[0].keys()))
        return results_a

    if results_b and join_key not in results_b[0]:
        logger.error("join_key '%s' no existe en fuente B. Campos: %s",
                     join_key, list(results_b[0].keys()))
        return results_a

    index_b = {r.get(join_key): r for r in results_b}
    merged = []
    for record_a in results_a:
        key_val = record_a.get(join_key)
        record_b = index_b.get(key_val, {})
        # Merge: A tiene prioridad sobre B en caso de campo con mismo nombre.
        # Campos de B que A no tiene se agregan al registro merged.
        merged_record = {**record_b, **record_a}
        merged.append(merged_record)
    return merged
