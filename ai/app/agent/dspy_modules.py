"""
Módulos DSPy (Fase B del plan).

Cada módulo envuelve un nodo LLM del agente con una Signature DSPy.
Instancias de producción al final del archivo: compiladas si existen
en compiled_modules/, baseline si no. Nunca fallan.
"""
from pathlib import Path

import dspy

from app.agent.dspy_config import get_primary_lm, get_light_lm


class PlannerSignature(dspy.Signature):
    """
    Clasificás la intención de una consulta sobre inclusión social
    en la Región Metropolitana de Florianópolis, Brasil.
    Extraés filtros geográficos, temporales y de servicio.
    Detectás si la consulta está fuera del dominio del sistema.

    Sistema cubre: formación técnica, mentoría, empleo,
    salud mental, conectividad de red móvil, programas sociales.
    Municipios válidos: Florianópolis, São José, Palhoça, Biguaçu.
    """
    consulta: str = dspy.InputField(
        desc="Consulta del gestor público en lenguaje natural (es/pt/en)"
    )

    fuera_de_dominio: bool = dspy.OutputField(
        desc=(
            "True si la consulta no tiene relación con inclusión social, "
            "conectividad o programas en la RM de Florianópolis. "
            "False si pertenece al dominio aunque sea parcialmente."
        )
    )
    servicio: str = dspy.OutputField(
        desc=(
            "Servicio social detectado: FORMACION, MENTORIA, EXPERIENCIA, "
            "EMPLEO, SALUD_MENTAL, EDUCACION. "
            "null si no aplica o la consulta es de red/conectividad."
        )
    )
    municipio: str = dspy.OutputField(
        desc=(
            "Municipio oficial: Florianópolis, São José, Palhoça, Biguaçu. "
            "null si no se menciona."
        )
    )
    cluster: str = dspy.OutputField(
        desc=(
            "Cluster exacto de los 23 válidos (ej: TRINDADE, SAO_JOSE_KOBRASOL). "
            "null si no aplica."
        )
    )
    indicador: str = dspy.OutputField(
        desc=(
            "Indicador específico SOLO si el usuario lo nombra puntualmente: "
            "taxa_emprego_formal, taxa_desemprego, evasao_escolar, "
            "taxa_conclusao_ensino_medio, taxa_internacao_psiquiatrica, "
            "cobertura_atencao_basica. "
            "null para preguntas genéricas como 'nivel de empleo'."
        )
    )
    periodo: str = dspy.OutputField(
        desc="MADRUGADA, MANHA, TARDE o NOITE. null si no aplica."
    )
    income_cluster: str = dspy.OutputField(
        desc="A, B, C o D. null si no se menciona nivel de ingresos."
    )
    fecha: str = dspy.OutputField(
        desc="Fecha en formato YYYY-MM-DD. null si no se menciona."
    )
    razon: str = dspy.OutputField(
        desc="Una línea explicando la clasificación."
    )


class PlannerModule(dspy.Module):
    def __init__(self, lm=None):
        super().__init__()
        self.lm = lm
        self.predict = dspy.Predict(PlannerSignature)

    def forward(self, consulta: str):
        with dspy.context(lm=self.lm or get_light_lm()):
            return self.predict(consulta=consulta)


class QueryClassifierSignature(dspy.Signature):
    """
    Determinás si una consulta sobre inclusión social en la RM de
    Florianópolis requiere UNA o MÚLTIPLES fuentes de datos.
    SIMPLE: una fuente. COMPUESTA: dos o más fuentes combinadas.
    """
    consulta: str = dspy.InputField(
        desc="Consulta original del gestor"
    )
    plan_serializado: str = dspy.InputField(
        desc="JSON con los filtros extraídos por el planner"
    )

    query_type: str = dspy.OutputField(
        desc=(
            "'simple' si una sola fuente responde la consulta. "
            "'compuesta' si necesita combinar datos de dos o más fuentes. "
            "Ejemplos simples: brechas de un servicio, indicador de una zona, "
            "programas disponibles. "
            "Ejemplos compuestos: desempleo Y conectividad, "
            "internaciones + programas activos, relación entre dos fenómenos."
        )
    )
    merge_strategy: str = dspy.OutputField(
        desc=(
            "'join' si combina métricas por zona (clave cluster). "
            "'relacional' si analiza correlación entre fenómenos."
        )
    )
    razon: str = dspy.OutputField(
        desc="Una línea explicando la decisión."
    )


class QueryClassifierModule(dspy.Module):
    def __init__(self, lm=None):
        super().__init__()
        self.lm = lm
        self.classify = dspy.ChainOfThought(QueryClassifierSignature)

    def forward(self, consulta: str, plan_serializado: str):
        with dspy.context(lm=self.lm or get_primary_lm()):
            return self.classify(
                consulta=consulta,
                plan_serializado=plan_serializado,
            )


class ClarificationDetectorSignature(dspy.Signature):
    """
    Detectás si una consulta sobre la RM de Florianópolis necesita
    clarificación del gestor antes de continuar. Preferís NO pausar
    cuando hay duda — una pausa innecesaria es peor UX que continuar.
    """
    consulta: str = dspy.InputField(
        desc="Consulta original del gestor"
    )
    plan_serializado: str = dspy.InputField(
        desc="JSON con los filtros extraídos por el planner"
    )

    necesita_clarificacion: bool = dspy.OutputField(
        desc=(
            "True SOLO si hay ambigüedad real que cambia el resultado: "
            "múltiples servicios sin especificar, zona inter-municipal, "
            "período temporal ambiguo con impacto en los datos. "
            "False si la consulta es genérica pero resoluble."
        )
    )
    pregunta: str = dspy.OutputField(
        desc="Pregunta específica al gestor. null si no necesita clarificación."
    )
    opciones: str = dspy.OutputField(
        desc=(
            "Opciones separadas por '|' para el gestor. "
            "Ej: 'Mentoría|Formación técnica|Ambas'. "
            "null si no aplica."
        )
    )
    razon: str = dspy.OutputField(
        desc="Por qué necesita o no necesita clarificación."
    )


class ClarificationDetectorModule(dspy.Module):
    def __init__(self, lm=None):
        super().__init__()
        self.lm = lm
        self.detect = dspy.Predict(ClarificationDetectorSignature)

    def forward(self, consulta: str, plan_serializado: str):
        with dspy.context(lm=self.lm or get_light_lm()):
            return self.detect(
                consulta=consulta,
                plan_serializado=plan_serializado,
            )


_COMPILED_DIR = Path("compiled_modules")


def load_compiled_module(name: str, module_class):
    """
    Carga un módulo compilado desde disco si existe.
    Si no existe, devuelve el módulo sin compilar (baseline).
    Nunca falla — el baseline sin compilar ya es funcional.
    """
    path = _COMPILED_DIR / f"{name}.json"
    if path.exists():
        module = module_class()
        module.load(str(path))
        return module
    return module_class()


# Instancias de producción — compiladas si existen, baseline si no.
# NO se instancian los módulos aquí para no forzar la importación de DSPy
# en el arranque del agente (es dependencia opcional hasta el Bloque 2).
planner_module = None
query_classifier_module = None
clarification_detector_module = None


def init_modules(use_compiled: bool = True):
    """Instancia los módulos (baseline o compilados). Llamada explícita
    por quien quiera usar DSPy en runtime, nunca en import."""
    global planner_module, query_classifier_module, clarification_detector_module
    if use_compiled:
        planner_module = load_compiled_module("planner", PlannerModule)
        query_classifier_module = load_compiled_module(
            "query_classifier", QueryClassifierModule
        )
        clarification_detector_module = load_compiled_module(
            "clarification_detector", ClarificationDetectorModule
        )
    else:
        planner_module = PlannerModule()
        query_classifier_module = QueryClassifierModule()
        clarification_detector_module = ClarificationDetectorModule()
