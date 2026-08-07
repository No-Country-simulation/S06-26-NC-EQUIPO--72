"""
Construye los datasets DSPy desde el golden_dataset.json existente.
Reutiliza exactamente las mismas consultas y expected values que
ya usás en run_evals.py — no hay que crear nuevos ejemplos.
"""
import json
from pathlib import Path

import dspy

_GOLDEN_PATH = Path(__file__).resolve().parent.parent / "evals" / "golden_dataset.json"
_OOD_PLANNER_PATH = (Path(__file__).resolve().parent.parent
                     / "evals" / "ood_planner_dataset.json")


def _load_golden() -> list[dict]:
    return json.loads(_GOLDEN_PATH.read_text(encoding="utf-8"))


def _serializar_plan(expected: dict) -> str:
    """
    CORRECCIÓN: el golden_dataset usa claves planas con puntos en el expected
    (ej. "plan.servicio": "EDUCACION"), NO dicts anidados. Acá se construye el
    plan real tal como lo produce el planner en runtime, para evitar el
    train/serve skew de mandar un plan vacío ("{}") al dataset.
    """
    plan_datos = {
        "fuera_de_dominio": expected.get("fuera_de_dominio", False),
        "servicio": expected.get("plan.servicio"),
        "municipio": expected.get("plan.municipio"),
        "cluster": expected.get("plan.cluster"),
        "indicador": expected.get("plan.indicador"),
        "periodo": expected.get("plan.periodo"),
        "income_cluster": expected.get("plan.income_cluster"),
    }
    return json.dumps(plan_datos, ensure_ascii=False)


def build_planner_dataset() -> list[dspy.Example]:
    """
    Dataset para el planner: consulta → filtros extraídos.
    Excluye consultas de evals HITL (distinto dominio de evaluación).
    """
    golden = _load_golden()
    examples = []
    for entry in golden:
        if entry["categoria"].startswith("hitl_"):
            continue

        expected = entry.get("expected", {})
        # CORRECCIÓN: acceso directo a las claves planas del expected.
        example = dspy.Example(
            consulta=entry["consulta"],
            fuera_de_dominio=expected.get("fuera_de_dominio", False),
            servicio=expected.get("plan.servicio"),
            municipio=expected.get("plan.municipio"),
            cluster=expected.get("plan.cluster"),
            indicador=expected.get("plan.indicador"),
            periodo=expected.get("plan.periodo"),
            income_cluster=expected.get("plan.income_cluster"),
            fecha=None,
        ).with_inputs("consulta")
        examples.append(example)

    return examples


def build_planner_ood_dataset() -> list[dspy.Example]:
    """
    Dataset OOD ANOTADO para el planner (evals/ood_planner_dataset.json):
    consultas parafraseadas que NO están en el golden, con los campos de
    planner anotados (servicio/municipio/indicador/cluster/periodo/
    income_cluster). Se usa como DEVSET de la compilación para medir la
    generalización real (el golden ya está en 100% y no deja headroom).
    """
    data = json.loads(_OOD_PLANNER_PATH.read_text(encoding="utf-8"))
    examples = []
    for entry in data:
        expected = entry.get("expected", {})
        example = dspy.Example(
            consulta=entry["consulta"],
            fuera_de_dominio=expected.get("fuera_de_dominio", False),
            servicio=expected.get("plan.servicio"),
            municipio=expected.get("plan.municipio"),
            cluster=expected.get("plan.cluster"),
            indicador=expected.get("plan.indicador"),
            periodo=expected.get("plan.periodo"),
            income_cluster=expected.get("plan.income_cluster"),
            fecha=None,
        ).with_inputs("consulta")
        examples.append(example)

    return examples


def build_classifier_dataset() -> list[dspy.Example]:
    """
    Dataset para el query_classifier: consulta + plan → simple/compuesta.
    """
    golden = _load_golden()
    examples = []
    for entry in golden:
        if entry["categoria"].startswith("hitl_"):
            continue

        expected = entry.get("expected", {})
        query_type = expected.get("query_type")
        if not query_type:
            continue  # omitir entradas sin expected query_type

        example = dspy.Example(
            consulta=entry["consulta"],
            # CORRECCIÓN: plan real (mismo JSON que recibe en runtime),
            # no un plan vacío.
            plan_serializado=_serializar_plan(expected),
            query_type=query_type,
            merge_strategy=expected.get("merge_strategy", "join"),
        ).with_inputs("consulta", "plan_serializado")
        examples.append(example)

    return examples


def build_clarification_dataset() -> list[dspy.Example]:
    """
    Dataset para el clarification_detector.
    Usa los 5 casos HITL + casos del golden donde la consulta
    es claramente no ambigua (necesita_clarificacion: false).
    """
    golden = _load_golden()
    examples = []

    for entry in golden:
        expected = entry.get("expected", {})

        if entry["categoria"].startswith("hitl_"):
            nc = expected.get("necesita_clarificacion")
            if nc is None:
                continue
            example = dspy.Example(
                consulta=entry["consulta"],
                plan_serializado=_serializar_plan(expected),
                necesita_clarificacion=nc,
                pregunta=None,
                opciones=None,
            ).with_inputs("consulta", "plan_serializado")
            examples.append(example)
        else:
            # Casos normales: no necesitan clarificación
            example = dspy.Example(
                consulta=entry["consulta"],
                plan_serializado=_serializar_plan(expected),
                necesita_clarificacion=False,
                pregunta=None,
                opciones=None,
            ).with_inputs("consulta", "plan_serializado")
            examples.append(example)

    return examples
