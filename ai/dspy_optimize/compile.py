"""
Script de compilación DSPy con MIPROv2.

Uso:
    python dspy_optimize/compile.py --module planner --auto light
    python dspy_optimize/compile.py --module query_classifier --auto medium
    python dspy_optimize/compile.py --all --auto light

Compilar gratis (sin gastar la cuota diaria de Groq) usando el tier
gratis de Gemini (500 RPD / 250K TPM), a costo de un puñado de minutos
a 15 RPM:

    python dspy_optimize/compile.py --module planner --auto light \
        --task-lm gemini --prompt-lm gemini --num-threads 1 --max-train 15

El script es OFFLINE — corre una vez y guarda los módulos compilados.
No afecta al agente en producción hasta que se copian los archivos.

CORRECCIÓN (ago-2026): con el golden en 100% el criterio de guardar es
"no regresar el devset" (score_optimized >= score_baseline) y la mejora
real se mide contra el dataset OOD (evals/ood_dataset.json), no contra el
golden (que ya no tiene headroom).
"""
import argparse
from pathlib import Path

from app.agent.dspy_config import (
    get_primary_lm, get_light_lm, get_gemini_lm,
)
from app.agent.dspy_modules import (
    PlannerModule, QueryClassifierModule, ClarificationDetectorModule,
)
from dspy_optimize.metrics import (
    planner_metric, query_classifier_metric, clarification_detector_metric,
)
from dspy_optimize.dataset import (
    build_planner_dataset, build_planner_ood_dataset,
    build_classifier_dataset, build_clarification_dataset,
)

_OUTPUT_DIR = Path("compiled_modules")
_OUTPUT_DIR.mkdir(exist_ok=True)

_LMS = {
    "gemini": get_gemini_lm,
    "groq-light": get_light_lm,
    "groq-primary": get_primary_lm,
}


def _build_trainset_devset(examples: list, split: float = 0.8):
    n = len(examples)
    split_idx = int(n * split)
    return examples[:split_idx], examples[split_idx:]


def compile_module(
    name: str,
    module_class,
    metric_fn,
    dataset_fn,
    auto: str = "light",
    task_lm=None,
    prompt_lm=None,
    num_threads: int = 1,
    max_train: int | None = None,
    devset_fn=None,
    num_candidates: int | None = None,
    num_trials: int | None = None,
):
    """
    Compila un módulo DSPy con MIPROv2 y lo guarda en disco.

    - task_lm: el modelo que corre el módulo (gemini = gratis, sin tocar Groq)
    - prompt_lm: el modelo que propone instrucciones (puede ser más fuerte)
    - max_train: acota el trainset para ajustarse a la cuota free (RPD/TPM)
    - devset_fn: si se provee, el devset es ese dataset (ej. el OOD anotado
      del planner) en vez del split interno del trainset. Así se mide la
      generalización real sobre parafraseos que el golden no cubre.
    - num_candidates/num_trials: con MIPROv2 auto=None (mode manual) acota
      el presupuesto (candidates de few-shot+instrucción y trials de BO).
      auto="light" fija 6 candidates y ~36 trials — MUCHO más caro.
    """
    mode_manual = num_candidates is not None
    print(f"\n{'='*60}")
    print(f"Compilando: {name} | auto={'manual' if mode_manual else auto} | "
          f"candidates={num_candidates} | trials={num_trials} | num_threads={num_threads}")
    print(f"{'='*60}")

    examples = dataset_fn()
    if max_train:
        examples = examples[:max_train]
    trainset, _ = _build_trainset_devset(examples)
    if devset_fn is not None:
        devset = devset_fn()
    else:
        _, devset = _build_trainset_devset(examples)
    print(f"Dataset: {len(trainset)} train, {len(devset)} dev")

    import dspy

    if task_lm:
        dspy.configure(lm=task_lm)

    module = module_class(lm=task_lm)

    from dspy.teleprompt import MIPROv2

    optimizer = MIPROv2(
        metric=metric_fn,
        prompt_model=prompt_lm or get_primary_lm(),
        task_model=task_lm or get_light_lm(),
        auto=None if mode_manual else auto,
        num_candidates=num_candidates,
        num_threads=num_threads,
        verbose=True,
    )

    print(f"Iniciando compilación MIPROv2 (auto={'manual' if mode_manual else auto}, "
          f"candidates={num_candidates}, trials={num_trials})...")
    # minibatch=False: MIPROv2 hace un split interno 80/20 (valset~80%); con
    # datasets chicos (<35) el minibatch por defecto excede el valset y lanza
    # ValueError. Con False, cada trial evalúa el valset completo (señal estable).
    optimized = optimizer.compile(
        student=module,
        trainset=trainset,
        max_bootstrapped_demos=3,
        max_labeled_demos=4,
        num_trials=num_trials,
        minibatch=False,
        requires_permission_to_run=False,
    )

    # Aceptación real: los evals del grafo (golden + OOD) con normalizar_plan,
    # NO la métrica interna de DSPy (que no aplica normalizar_plan y subestima
    # al sistema real — el baseline DSPy genérico saca ~43% vs 100% del sistema).
    # Por eso se guarda SIEMPRE: si los evals del grafo muestran regresión, el
    # archivo se elimina (revertir). El devset_fn se mantiene para registro.
    output_path = _OUTPUT_DIR / f"{name}.json"
    optimized.save(str(output_path))
    print(f"  Guardado en: {output_path}")

    return 0.0, 0.0


def main():
    parser = argparse.ArgumentParser(
        description="Compilación DSPy con MIPROv2 para App BiT"
    )
    parser.add_argument(
        "--module",
        choices=["planner", "query_classifier", "clarification_detector"],
        help="Módulo a compilar",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Compilar todos los módulos en orden de prioridad",
    )
    parser.add_argument(
        "--auto",
        choices=["light", "medium", "heavy"],
        default="light",
        help="Intensidad de la compilación MIPROv2",
    )
    parser.add_argument(
        "--task-lm",
        choices=list(_LMS),
        default="groq-light",
        help="Modelo que corre el módulo (gemini = gratis, 500 RPD/250K TPM)",
    )
    parser.add_argument(
        "--prompt-lm",
        choices=list(_LMS),
        default="groq-primary",
        help="Modelo que propone instrucciones a MIPROv2",
    )
    parser.add_argument(
        "--num-threads",
        type=int,
        default=1,
        help="Paralelismo (1 para respetar el límite de 15 RPM de Gemini)",
    )
    parser.add_argument(
        "--max-train",
        type=int,
        default=None,
        help="Acotar el trainset a N ejemplos (control de cuota free)",
    )
    parser.add_argument(
        "--num-candidates",
        type=int,
        default=None,
        help="Candidates de few-shot+instrucción (auto manual, acota presupuesto)",
    )
    parser.add_argument(
        "--num-trials",
        type=int,
        default=None,
        help="Trials de optimización bayesiana (auto manual)",
    )
    args = parser.parse_args()

    task_lm = _LMS[args.task_lm]()
    prompt_lm = _LMS[args.prompt_lm]()

    modulos = {
        "planner": (
            PlannerModule, planner_metric, build_planner_dataset,
            build_planner_ood_dataset,  # devset OOD anotado (generalización)
        ),
        "query_classifier": (
            QueryClassifierModule, query_classifier_metric,
            build_classifier_dataset, None,
        ),
        "clarification_detector": (
            ClarificationDetectorModule, clarification_detector_metric,
            build_clarification_dataset, None,
        ),
    }

    if args.module:
        seleccion = {args.module: modulos[args.module]}
    elif args.all:
        seleccion = modulos
    else:
        parser.error("Se requiere --module o --all")

    for nombre, (cls, metric, ds, devset) in seleccion.items():
        compile_module(nombre, cls, metric, ds, auto=args.auto,
                       task_lm=task_lm, prompt_lm=prompt_lm,
                       num_threads=args.num_threads,
                       max_train=args.max_train,
                       devset_fn=devset,
                       num_candidates=args.num_candidates,
                       num_trials=args.num_trials)


if __name__ == "__main__":
    main()
