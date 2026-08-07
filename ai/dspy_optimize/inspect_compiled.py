"""
Inspecciona un módulo DSPy compilado: instrucciones y demos que MIPROv2
encontró. Útil para documentar las mejoras de prompts post-compilación.

Uso (dentro del contenedor AI, desde /app):
    python dspy_optimize/inspect_compiled.py planner
"""
import argparse
import json
from pathlib import Path


def inspect(nombre: str):
    ruta = Path("compiled_modules") / f"{nombre}.json"
    if not ruta.exists():
        print(f"No existe módulo compilado: {ruta}")
        return

    data = json.loads(ruta.read_text(encoding="utf-8"))
    print(f"\n=== {nombre}.json ===")

    # Estructura típica de un Predict/PredictWithTakenSignatures guardado.
    for key in ("predict", "classify", "detect"):
        predictor = data.get(key) or (data.get("forward", {}) or {}).get(key)
        if not predictor:
            continue
        print(f"\n--- {key} ---")
        for step in predictor.get("predictions", []):
            instructions = step.get("instructions") or step.get("signature", {}).get("instructions")
            if instructions:
                print(f"Instrucciones: {str(instructions)[:600]}")
        demos = predictor.get("demos", [])
        print(f"Demos few-shot: {len(demos)}")
        for i, demo in enumerate(demos[:2]):
            print(f"  Demo {i+1}: {str(demo)[:300]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("module", choices=["planner", "query_classifier",
                                           "clarification_detector"])
    args = parser.parse_args()
    inspect(args.module)
