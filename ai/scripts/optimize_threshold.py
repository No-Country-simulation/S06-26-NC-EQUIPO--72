"""
Análisis adaptativo del schema_linker_threshold.

Metodología:
1. Correr el schema linker sobre el dataset (golden u OOD) registrando
   por consulta: routing (determinístico vs embeddings), score real de
   embeddings y endpoint elegido.
2. Construir la curva Precision-Recall para cada valor de threshold.
   Solo las consultas que usan embeddings participan de la curva (las
   determinísticas aciertan con score=1.0 independientemente del threshold).
3. Encontrar el threshold óptimo según la métrica elegida.
4. Generar reporte en consola y JSON (evals/threshold_analysis.json).

Uso (dentro del contenedor AI, desde /app):
    python scripts/optimize_threshold.py                              # golden
    python scripts/optimize_threshold.py --dataset evals/ood_dataset.json
    python scripts/optimize_threshold.py --metric precision_at_recall 0.9
    python scripts/optimize_threshold.py --plan-mode empty   # plan vacío (pure embeddings)

CORRECCIÓN (ago-2026): el golden resuelve 17/17 endpoints por routing
determinístico y CERO usan embeddings → el script avisa "threshold
irrelevante". Correr contra el dataset OOD (evals/ood_dataset.json), cuyas
consultas están parafraseadas para no disparar las reglas determinísticas.
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent.schema_linker import _route_por_plan  # noqa: E402
from app.agent.normalizer import normalizar_plan  # noqa: E402
from app.vectorstore.searcher import search as qdrant_search  # noqa: E402

_DEFAULT_DATASET = Path("evals/golden_dataset.json")
_THRESHOLD_ACTUAL = 0.67


def _cargar_dataset(ruta: Path) -> list[dict]:
    if not ruta.exists():
        sys.exit(f"No existe el dataset: {ruta}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _plan_para_query(entry: dict, plan_mode: str) -> dict:
    """Construye el plan que alimenta al router determinístico.

    - plan_mode="expected": usa los valores del golden (sin llamada LLM).
    - plan_mode="empty": plan vacío — simula el peor caso donde el planner
      no extrajo nada y la decisión depende 100% de embeddings.
    """
    expected = entry.get("expected", {})
    if plan_mode == "expected":
        return normalizar_plan({
            "fuera_de_dominio": expected.get("fuera_de_dominio", False),
            "servicio": expected.get("plan.servicio"),
            "municipio": expected.get("plan.municipio"),
            "indicador": expected.get("plan.indicador"),
            "periodo": expected.get("plan.periodo"),
            "cluster": None,
            "income_cluster": None,
            "fecha": None,
        })
    return normalizar_plan({
        "fuera_de_dominio": False,
        "servicio": None, "municipio": None, "indicador": None,
        "periodo": None, "cluster": None, "income_cluster": None, "fecha": None,
    })


def _esperado(entry: dict) -> str | None:
    """Devuelve lo que se espera resolver: un endpoint o 'sql'."""
    exp = entry.get("expected", {})
    endpoint = exp.get("schema_decision.endpoint")
    if endpoint:
        return endpoint
    tipo = exp.get("schema_decision.tipo")
    if tipo == "sql":
        return "sql"
    return None


def _obtener_score_real(consulta: str, plan: dict) -> dict:
    """Corre el schema linker con threshold=0 (acepta todo) y registra
    el score real del mejor match de embeddings."""
    consulta_lower = consulta.lower()

    # Paso 1: routing determinístico (no usa threshold)
    resultado_det = _route_por_plan(plan, consulta_lower)
    if resultado_det:
        return {
            "routing": "deterministico",
            "score": 1.0,
            "endpoint_elegido": resultado_det["endpoint"],
            "usa_embeddings": False,
        }

    # Paso 2: embeddings search con debug=True (ignora el threshold)
    partes = [consulta]
    if plan.get("servicio"):
        partes.append(f"servicio: {plan['servicio']}")
    if plan.get("indicador"):
        partes.append(f"indicador: {plan['indicador']}")
    query_enriquecida = " | ".join(partes)

    resultado = qdrant_search(query_enriquecida, top_k=1, tipo="endpoint",
                              debug=True)

    if not resultado:
        return {
            "routing": "embeddings",
            "score": 0.0,
            "endpoint_elegido": None,
            "usa_embeddings": True,
        }

    return {
        "routing": "embeddings",
        "score": resultado["score"],
        "endpoint_elegido": resultado.get("endpoint"),
        "usa_embeddings": True,
    }


def _recolectar_scores(dataset: list[dict], plan_mode: str) -> list[dict]:
    registros = []
    for entry in dataset:
        if entry["categoria"].startswith("hitl_"):
            continue

        esperado = _esperado(entry)
        if not esperado:
            continue

        plan = _plan_para_query(entry, plan_mode)
        score_data = _obtener_score_real(entry["consulta"], plan)

        elegido = score_data["endpoint_elegido"]
        match_correcto = (
            elegido == esperado if esperado != "sql"
            else elegido is None  # si era sql, "acertar" = no matchear endpoint
        )

        registros.append({
            "id": entry["id"],
            "consulta": entry["consulta"][:60],
            "esperado": esperado,
            "endpoint_elegido": elegido,
            "score": score_data["score"],
            "routing": score_data["routing"],
            "usa_embeddings": score_data["usa_embeddings"],
            "match_correcto": match_correcto,
        })
    return registros


def _calcular_curva_pr(registros: list[dict],
                       thresholds: np.ndarray) -> list[dict]:
    solo_embeddings = [r for r in registros if r["usa_embeddings"]]
    if not solo_embeddings:
        print("ADVERTENCIA: ninguna consulta usa embeddings — threshold irrelevante")
        return []

    resultados = []
    for threshold in thresholds:
        tp = fp = fn = tn = 0
        for r in solo_embeddings:
            supera = r["score"] >= threshold
            es_correcto = r["match_correcto"]
            if supera and es_correcto:
                tp += 1
            elif supera and not es_correcto:
                fp += 1
            elif not supera and es_correcto:
                fn += 1
            else:
                tn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0.0)
        fallback_rate = (fn + tn) / len(solo_embeddings)

        resultados.append({
            "threshold": round(float(threshold), 3),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "fallback_rate": round(fallback_rate, 4),
        })
    return resultados


def _optimo(curva: list[dict], metrica: str, min_precision: float) -> dict:
    if metrica == "f1":
        return max(curva, key=lambda r: r["f1"])
    if metrica == "precision":
        return max(curva, key=lambda r: r["precision"])
    if metrica == "precision_at_recall":
        candidatos = [r for r in curva if r["recall"] >= min_precision]
        if not candidatos:
            return max(curva, key=lambda r: r["precision"])
        return max(candidatos, key=lambda r: r["precision"])
    raise ValueError(f"Métrica desconocida: {metrica}")


def _imprimir_reporte(registros, curva, optimo, threshold_actual):
    print("\n" + "=" * 70)
    print("ANÁLISIS ADAPTATIVO DEL SCHEMA LINKER THRESHOLD")
    print("=" * 70)

    solo_emb = [r for r in registros if r["usa_embeddings"]]
    deterministicos = [r for r in registros if not r["usa_embeddings"]]

    print(f"\nDataset analizado:")
    print(f"  Total consultas:         {len(registros)}")
    print(f"  Routing determinístico:  {len(deterministicos)} "
          f"({len(deterministicos)/len(registros)*100:.0f}%)")
    print(f"  Routing por embeddings:  {len(solo_emb)} "
          f"({len(solo_emb)/len(registros)*100:.0f}%)")

    for r in registros:
        print(f"  [{r['id']}] {r['consulta']:<50} "
              f"esperado={r['esperado']:<20} score={r['score']:.3f} "
              f"elegido={r['endpoint_elegido'] or 'sql'} "
              f"{'OK' if r['match_correcto'] else 'MAL'} ({r['routing']})")

    if not curva:
        return

    actual_row = next((r for r in curva
                       if abs(r["threshold"] - threshold_actual) < 0.01), None)
    if actual_row:
        print(f"\n  Threshold ACTUAL ({threshold_actual}):")
        print(f"    Precision: {actual_row['precision']:.4f} | "
              f"Recall: {actual_row['recall']:.4f} | "
              f"F1: {actual_row['f1']:.4f} | "
              f"FP: {actual_row['fp']} | FN: {actual_row['fn']} | "
              f"Fallback: {actual_row['fallback_rate']:.2%}")

    print(f"\n  Threshold OPTIMO ({optimo['threshold']}):")
    print(f"    Precision: {optimo['precision']:.4f} | "
          f"Recall: {optimo['recall']:.4f} | "
          f"F1: {optimo['f1']:.4f} | "
          f"FP: {optimo['fp']} | FN: {optimo['fn']} | "
          f"Fallback: {optimo['fallback_rate']:.2%}")

    print(f"\n  Curva (threshold 0.50 a 0.95):")
    print(f"    {'Thresh':>7} {'Prec':>7} {'Recall':>7} {'F1':>7} "
          f"{'FP':>4} {'FN':>4} {'Fallback':>9}")
    for row in curva:
        mark = ""
        if abs(row["threshold"] - threshold_actual) < 0.01:
            mark = " <- actual"
        if abs(row["threshold"] - optimo["threshold"]) < 0.01:
            mark += " <- optimo"
        print(f"    {row['threshold']:>7.3f} {row['precision']:>7.4f} "
              f"{row['recall']:>7.4f} {row['f1']:>7.4f} "
              f"{row['fp']:>4} {row['fn']:>4} "
              f"{row['fallback_rate']:>9.2%}{mark}")

    print(f"\n  Recomendación:")
    if optimo["threshold"] != threshold_actual:
        print(f"    Actualizar schema_linker_threshold: "
              f"{threshold_actual} -> {optimo['threshold']}")
        print(f"    En config.py: "
              f"schema_linker_threshold: float = {optimo['threshold']}")
    else:
        print(f"    El threshold actual ({threshold_actual}) ya es óptimo.")


def main(dataset: Path, plan_mode: str, metrica: str, min_precision: float):
    dataset_data = _cargar_dataset(dataset)
    print(f"Cargadas {len(dataset_data)} consultas de {dataset}")
    print(f"plan_mode={plan_mode} metrica={metrica}")

    registros = _recolectar_scores(dataset_data, plan_mode)
    thresholds = np.arange(0.50, 0.96, 0.01)
    curva = _calcular_curva_pr(registros, thresholds)

    optimo = (_optimo(curva, metrica, min_precision) if curva
              else {"threshold": _THRESHOLD_ACTUAL, "precision": 1.0,
                    "recall": 1.0, "f1": 1.0, "fp": 0, "fn": 0,
                    "fallback_rate": 0.0})

    _imprimir_reporte(registros, curva, optimo, _THRESHOLD_ACTUAL)

    reporte = {
        "dataset": str(dataset),
        "plan_mode": plan_mode,
        "threshold_actual": _THRESHOLD_ACTUAL,
        "threshold_optimo": optimo["threshold"],
        "metricas": {k: optimo[k] for k in
                     ("precision", "recall", "f1", "fp", "fn",
                      "fallback_rate")},
        "registros": registros,
        "curva": curva,
    }
    salida = Path("evals/threshold_analysis.json")
    salida.write_text(json.dumps(reporte, ensure_ascii=False, indent=2))
    print(f"\nReporte guardado en {salida}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adaptive schema linker threshold")
    parser.add_argument("--dataset", type=Path, default=_DEFAULT_DATASET,
                        help="Dataset a analizar (default: golden)")
    parser.add_argument("--plan-mode", choices=["expected", "empty"],
                        default="expected",
                        help="Como construir el plan (expected=golden, empty=vacio)")
    parser.add_argument("--metric", choices=["f1", "precision",
                                             "precision_at_recall"],
                        default="f1")
    parser.add_argument("--min-precision", type=float, default=0.85,
                        help="Precision minima para precision_at_recall")
    args = parser.parse_args()

    main(args.dataset, args.plan_mode, args.metric, args.min_precision)
