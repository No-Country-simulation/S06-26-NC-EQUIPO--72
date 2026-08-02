import json
from typing import Any

from app.agent.json_utils import json_default
from app.agent.state import AgentState
from app.core.config import settings


# Calibrado a 0.5 (≈2 chars/token) en vez de 0.25: con 0.25 el estimador
# subestimaba a la mitad los tokens reales del JSON (11.839 chars ≈ 6.000
# tokens, no ~2.960), dejando pasar a la compuesta relacional un contexto que
# superaba el TPM de 6000 del modelo 8B y Groq rechazaba con 413.
_TOKENS_POR_CARACTER = 0.5

# Campos técnicos internos que el formatter nunca necesita mencionar
_CAMPOS_INTERNOS = {"ecgi", "id", "created_at", "updated_at", "codigo_origem"}


def _limpiar_para_formatter(results: list[dict]) -> list[dict]:
    """
    Filtra campos técnicos internos antes de pasarlos al formatter.
    Solo afecta el contexto del LLM- no el resultado que ve el frontend.
    """
    return [
        {k: v for k, v in r.items() if k not in _CAMPOS_INTERNOS}
        for r in results
    ]


def _detectar_tipo_datos(results: list[dict]) -> str:
    """
    Auto-detección del tipo de datos para guiar al formatter.
    """
    if not results:
        return "sin_datos"
    campos = set().union(*[r.keys() for r in results[:3]])
    if "severidad_brecha" in campos:
        return "brechas_sociales"
    if "indicadores" in campos:
        return "indicadores_territoriales"
    if "rat_type_predominante" in campos and "indicadores" not in campos:
        return "datos_red_pura"
    if "tipo" in campos and "organizacion" in campos:
        return "programas_sociales"
    if "evolucion" in campos or "valor_promedio" in campos:
        return "evolucion_temporal"
    return "datos_generales"


def _construir_contexto_formatter(
    state: AgentState,
    datos_para_llm,
    fue_resumido: bool,
) -> str:
    """
    Construye el contexto enriquecido para el formatter con toda la
    información relevante explícita- el modelo no debe inferir nada del JSON.
    """
    decision = state.get("schema_decision", {})
    meta = state.get("tool_results_meta", {})
    tool_results = state.get("tool_results", [])
    merged = state.get("merged_results", [])
    datos_finales = merged or tool_results
    tipo = _detectar_tipo_datos(datos_finales)
    merge_strategy = state.get("merge_strategy", "")
    reflection_feedback = state.get("reflection_feedback", "")

    return f"""
Consulta original: {state['consulta']}
Idioma de respuesta: {state['idioma']}

# Contexto de la decisión
Tipo de consulta: {state.get('query_type', 'simple')}
Fuente de datos: {decision.get('endpoint', 'múltiples endpoints')}
Tipo de datos: {tipo}
Merge realizado: {merge_strategy if merge_strategy else 'ninguno (consulta simple)'}
Datos resumidos: {'SÍ (el dataset completo era muy grande)' if fue_resumido else 'NO (datos completos)'}
Hay datos disponibles: {'SÍ' if datos_finales else 'NO- los filtros no matchearon ningún resultado'}
Total de registros: {len(datos_finales)}
Error en ejecución: {state.get('tool_error') or 'ninguno'}

# Feedback de la reflexión anterior (si aplica)
{f'ATENCIÓN- mejorar estos aspectos: {reflection_feedback}' if reflection_feedback else 'Primera generación- sin feedback previo'}

# Datos
{json.dumps(datos_para_llm, ensure_ascii=False, default=json_default)}
""".strip()


def _necesita_resumen(results: list[dict], max_tokens: int) -> bool:
    sample_json = json.dumps(results, ensure_ascii=False, default=json_default)
    tokens_estimados = len(sample_json) * _TOKENS_POR_CARACTER
    return tokens_estimados > max_tokens


def resumir_para_formatter(results: list[dict]) -> tuple[list[Any] | dict, bool]:
    """
    Devuelve (datos_resumidos, fue_resumido).
    Criterio: estimación de tokens, no cantidad de registros.
    """
    if not _necesita_resumen(results, settings.formatter_max_tokens_estimate):
        return results, False

    tiene_brecha = any("severidad_brecha" in r for r in results)
    if tiene_brecha:
        alta = [r for r in results if r.get("severidad_brecha") == "ALTA"]
        return {
            "total_zonas": len(results),
            "zonas_alta_prioridad": alta[:10],
            "media_count": sum(1 for r in results if r.get("severidad_brecha") == "MEDIA"),
            "baja_count": sum(1 for r in results if r.get("severidad_brecha") == "BAJA"),
            "nota": "resumen- datos completos disponibles",
        }, True
    else:
        # Muestra DISTRIBUIDA a lo largo del dataset, no los primeros N:
        # cuando el merge concatenó varias fuentes (estrategia relacional),
        # tomar solo el inicio perdería los datos de las fuentes siguientes.
        total = len(results)
        n = settings.formatter_max_records
        if total <= n:
            muestra = results
        else:
            step = total / n
            indices = sorted({min(int(i * step), total - 1) for i in range(n)})
            muestra = [results[i] for i in indices]
        return {
            "total_zonas": total,
            "muestra": muestra,
            "nota": f"mostrando {len(muestra)} de {total} registros",
        }, True
