"""
 Evals. Ejecuta el golden dataset contra el agente real.

Uso (dentro del contenedor AI, desde /app):
    python -m evals.run_evals            # reporte consola
    python -m evals.run_evals --json evals/reporte.json

- Concurrencia acotada (semáforo) para no saturar el TPM de Groq.
- Reintenta consultas fallidas por rate-limit a nivel eval (la ventana de
  TPM es ~60s, los retries internos del grafo son de 1-8s).
- Compara municipios normalizando acentos/case ("Sao Jose" == "São José").
- Reporta métricas por nodo + score por categoría.
"""
import asyncio
import json
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import logging

logger = logging.getLogger("evals")

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Campos cuyo comparador normaliza acentos/case.
_NORM_CHECKS = ("plan.municipio", "schema_decision.params.municipio")

# El TPM free-tier de Groq (6000/min para el 8B) es chico: las consultas en
# paralelo chocan y re-exhaustan la ventana sin recuperarse. Secuencial con
# cooldown + backoff de 60s (duración de la ventana) es lo confiable.
CONCURRENCIA = 1
INTENTOS_POR_QUERY = 3
# Pacing para el 8B: cuando el fallback (Gemini 2.0 Flash Lite) no tiene cuota
# o el 70B agotó su TPD diario, todo el pipeline cae al 8B: ~5700 tokens por
# consulta simple sobre su TPM de 6000. Cooldown ~60s deja drenar la ventana
# de 60s para que la siguiente arranque limpia.
COOLDOWN_ENTRE_QUERIES = 60  # segundos entre consultas exitosas
BACKOFF_RATE_LIMIT = 90  # > ventana de TPM (60s): garantiza ventana limpia al reintentar
# Timeout por consulta: ai_service lo aplica (simple 30s / compuesta 60s) pero
# eval_consulta llamaba a agent.ainvoke sin timeout -> una llamada colgada
# bloqueaba todo el run para siempre (visto con eval_017). 90s cubre la peor
# compuesta nominal (~39s) con margen.
AGENT_TIMEOUT_EVAL = 90.0

# Errores transitorios de Groq que ameritan reintento a nivel eval.
_TRANSIENT = ("RateLimitError", "APIStatusError", "APITimeoutError",
              "APIConnectionError")


def _norm(s) -> str:
    if s is None:
        return ""
    return (
        unicodedata.normalize("NFKD", str(s))
        .encode("ascii", "ignore").decode().strip().lower()
    )


def _get_actual(state: dict, check_key: str):
    if check_key == "tool_results_not_empty":
        return bool(state.get("tool_results") or state.get("merged_results"))
    if check_key == "reflection_score_min":
        return state.get("reflection_score", 0.0)
    if check_key == "fuera_de_dominio":
        # El agente solo setea True; en consultas en-dominio queda ausente.
        return bool(state.get("fuera_de_dominio"))
    actual = state
    for part in check_key.split("."):
        if not isinstance(actual, dict):
            return None
        actual = actual.get(part)
    return actual


def _check_passed(check_key: str, actual, expected) -> bool:
    if check_key == "tool_results_not_empty":
        return bool(actual) == bool(expected)
    if check_key == "reflection_score_min":
        return actual >= expected
    if check_key in _NORM_CHECKS:
        return _norm(actual) == _norm(expected)
    return actual == expected


def _es_error_transitorio(err: str) -> bool:
    return any(t in err for t in _TRANSIENT)


async def eval_consulta(entry: dict, agent, sem: asyncio.Semaphore) -> dict:
    async with sem:
        error = None
        state: dict = {}
        latencia = 0.0

        for intento in range(INTENTOS_POR_QUERY):
            t0 = time.perf_counter()
            try:
                state = await asyncio.wait_for(
                    agent.ainvoke({
                        "consulta": entry["consulta"],
                        "idioma": entry["idioma"],
                        "request_id": f"eval_{entry['id']}",
                        "filtros": {},
                    }),
                    timeout=AGENT_TIMEOUT_EVAL,
                )
                error = None
                latencia = time.perf_counter() - t0
                break
            except Exception as e:  # noqa: BLE001
                latencia = time.perf_counter() - t0
                error = f"{type(e).__name__}: {str(e)[:200]}"
                if _es_error_transitorio(error) and intento < INTENTOS_POR_QUERY - 1:
                    logger.warning(
                        "[%s] transitorio (%s)- esperando %ds (%d/%d)",
                        entry["id"], type(e).__name__, BACKOFF_RATE_LIMIT,
                        intento + 1, INTENTOS_POR_QUERY,
                    )
                    await asyncio.sleep(BACKOFF_RATE_LIMIT)
                else:
                    break

        if not error:
            # Espacia el uso de TPM entre consultas exitosas.
            await asyncio.sleep(COOLDOWN_ENTRE_QUERIES)

        checks = {}
        for check_key, expected in entry["expected"].items():
            actual = _get_actual(state, check_key)
            checks[check_key] = {
                "pass": _check_passed(check_key, actual, expected),
                "actual": actual,
                "expected": expected,
            }

        passed = sum(1 for c in checks.values() if c["pass"])
        total = len(checks)
        return {
            "id": entry["id"],
            "categoria": entry["categoria"],
            "consulta": entry["consulta"][:70],
            "score": passed / total if total else 0,
            "passed": passed,
            "total": total,
            "latencia": round(latencia, 2),
            "error": error,
            "checks": checks,
            "state": state,
        }


# ---------- Métricas por nodo ----------

def _metricas_por_nodo(results: list[dict]) -> dict:
    def _score(key):
        tot = pas = 0
        for r in results:
            if key in r["checks"]:
                tot += 1
                pas += int(r["checks"][key]["pass"])
        return (pas / tot if tot else None, pas, tot)

    servicio, s_p, s_t = _score("plan.servicio")
    municipio, m_p, m_t = _score("plan.municipio")
    endpoint, e_p, e_t = _score("schema_decision.endpoint")
    qtype, q_p, q_t = _score("query_type")
    merge, mg_p, mg_t = _score("merge_strategy")
    visual, v_p, v_t = _score("visualizacion_sugerida")

    # Fuera de dominio: precision y recall
    fd = [(r["state"].get("fuera_de_dominio") is True,
           r["checks"]["fuera_de_dominio"]["expected"] is True)
          for r in results if "fuera_de_dominio" in r["checks"]]
    vp = sum(1 for a, e in fd if a and e)
    fp = sum(1 for a, e in fd if a and not e)
    fn = sum(1 for a, e in fd if not a and e)
    precision = vp / (vp + fp) if (vp + fp) else None
    recall = vp / (vp + fn) if (vp + fn) else None

    # Tool caller: empty rate y sub-agent errors
    not_empty, ne_p, ne_t = _score("tool_results_not_empty")
    empty_rate = (1 - ne_p / ne_t) if ne_t else None
    react = sum(1 for r in results if r["state"].get("react_retry_count", 0) > 0)
    sub_err = sum(
        1 for r in results
        for sr in r["state"].get("sub_agent_results", []) if sr.get("error")
    )

    # Reflector
    scores_ref = [
        r["state"].get("reflection_score")
        for r in results
        if r["state"].get("reflection_score") is not None
    ]
    retry_ref = sum(1 for r in results
                    if r["state"].get("reflection_retry_count", 0) > 0)

    lat = sorted(r["latencia"] for r in results if r["latencia"] > 0)
    errores_http = sum(1 for r in results if r["error"])

    return {
        "PLANNER": {
            "accuracy_servicio": _fmt(servicio, s_p, s_t),
            "accuracy_municipio": _fmt(municipio, m_p, m_t),
            "fuera_dominio_precision": _fmt(precision, vp, vp + fp),
            "fuera_dominio_recall": _fmt(recall, vp, vp + fn),
        },
        "QUERY_CLASSIFIER": {
            "accuracy_query_type": _fmt(qtype, q_p, q_t),
            "accuracy_merge_strategy": _fmt(merge, mg_p, mg_t),
        },
        "SCHEMA_LINKER": {
            "endpoint_accuracy": _fmt(endpoint, e_p, e_t),
        },
        "FORMATTER": {
            "visualizacion_accuracy": _fmt(visual, v_p, v_t),
        },
        "TOOL_CALLER": {
            "empty_rate": _fmt(empty_rate, ne_t - ne_p, ne_t),
            "react_retry_count": react,
            "sub_agent_errors": sub_err,
        },
        "REFLECTOR": {
            "mean_quality_score": (round(sum(scores_ref) / len(scores_ref), 3)
                                   if scores_ref else None),
            "retry_rate": (retry_ref / len(scores_ref) if scores_ref else None),
            "con_llm": len(scores_ref),
        },
        "END_TO_END": {
            "latencia_p50": _percentil(lat, 0.50),
            "latencia_p95": _percentil(lat, 0.95),
            "errores_por_rate_limit": errores_http,
            "queries": len(results),
        },
    }


def _fmt(val, p=None, t=None):
    if val is None:
        return None
    return {"valor": round(val, 4), "pass": p, "total": t}


def _percentil(lat: list[float], q: float):
    if not lat:
        return None
    lat = sorted(lat)
    idx = min(len(lat) - 1, int(q * len(lat)))
    return round(lat[idx], 2)


def _imprimir_reporte(results: list[dict]) -> None:
    print("\n=== EVAL RESULTS ===")
    por_categoria = defaultdict(list)
    for r in results:
        por_categoria[r["categoria"]].append(r)

    total = len(results)
    score_all = sum(r["score"] for r in results) / total

    print(f"Score total: {score_all:.2%} ({total} consultas)\n")

    for cat, items in sorted(por_categoria.items()):
        avg = sum(r["score"] for r in items) / len(items)
        print(f"  {cat}: {avg:.2%} ({len(items)} consultas)")

    fallos = [r for r in results if r["score"] < 1.0]
    if fallos:
        print(f"\nFallos ({len(fallos)}):")
        for r in fallos:
            print(f"  [{r['id']}] {r['consulta']} (score {r['score']:.0%}, {r['latencia']}s)")
            if r["error"]:
                print(f"      error: {r['error'][:120]}")
            for check, detail in r["checks"].items():
                if not detail["pass"]:
                    print(f"      ✗ {check}: esperado={detail['expected']!r} "
                          f"actual={detail['actual']!r}")

    print("\n=== MÉTRICAS POR NODO ===")
    for nodo, metricas in _metricas_por_nodo(results).items():
        print(f"\n{nodo}:")
        for k, v in metricas.items():
            print(f"  {k}: {v}")


async def run_all_evals(ruta_dataset: str | None = None) -> None:
    from app.agent.graph import agent

    # CLI: [dataset_path] [--json salida.json] (orden indistinto)
    if ruta_dataset is None or "--json" in sys.argv:
        positional, ruta_json = [], None
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == "--json":
                ruta_json = args[i + 1]
                i += 2
            else:
                positional.append(args[i])
                i += 1
        ruta_dataset = ruta_dataset or positional[0] if positional else "evals/golden_dataset.json"
    else:
        ruta_json = None

    dataset = json.loads(Path(ruta_dataset).read_text())
    print(f"Cargadas {len(dataset)} consultas de {ruta_dataset}")

    # Reanudar: si existe un parcial, se saltea lo ya completado (no se pierde
    # el trabajo si un run se cuelga o se corta).
    parcial = Path(ruta_json + ".partial") if ruta_json else None
    results: list[dict] = []
    if parcial and parcial.exists():
        try:
            prev = json.loads(parcial.read_text())
            results = list(prev.get("detalle", []))
            if results:
                print(f"Reanudando: {len(results)} consultas ya completadas")
        except Exception:
            results = []
    hechos = {r["id"] for r in results}
    pendientes = [e for e in dataset if e["id"] not in hechos]
    print(f"Pendientes: {len(pendientes)} de {len(dataset)}")

    sem = asyncio.Semaphore(CONCURRENCIA)
    tasks = [eval_consulta(e, agent, sem) for e in pendientes]
    for coro in asyncio.as_completed(tasks):
        r = await coro
        results.append(r)
        estado = "OK " if r["score"] == 1.0 else "FALLO"
        print(f"[{r['id']}] {estado} score={r['score']:.0%} ({r['latencia']}s) "
              f"{r['consulta'][:45]}", flush=True)
        if parcial:
            parcial.write_text(json.dumps(
                {"detalle": results}, ensure_ascii=False, indent=2))

    # /indicadores/evolucion ya implementado (backend + router + prompt).
    _imprimir_reporte(results)

    if ruta_json:
        Path(ruta_json).write_text(json.dumps({
            "resumen": {
                "score_total": round(sum(r["score"] for r in results) / len(results), 4),
                "consultas": len(results),
            },
            "metricas_por_nodo": _metricas_por_nodo(results),
            "detalle": [
                {k: v for k, v in r.items() if k != "state"}
                for r in results
            ],
        }, ensure_ascii=False, indent=2))
        print(f"\nReporte JSON guardado en {ruta_json}")


if __name__ == "__main__":
    asyncio.run(run_all_evals())
