from typing import Literal

from pydantic import BaseModel, Field


class PlanOutput(BaseModel):
    fuera_de_dominio: bool = False
    # EDUCACION es válida como categoria en /mapa/indicadores (schema_linker)
    servicio: Literal[
        "FORMACION", "MENTORIA", "EXPERIENCIA", "EMPLEO", "SALUD_MENTAL", "EDUCACION"
    ] | None = None
    municipio: str | None = None
    periodo: Literal["MADRUGADA", "MANHA", "TARDE", "NOITE"] | None = None
    cluster: str | None = None
    income_cluster: Literal["A", "B", "C", "D"] | None = None
    indicador: str | None = None
    fecha: str | None = None
    razon: str = ""


class QueryClassification(BaseModel):
    query_type: Literal["simple", "compuesta"]
    fuentes_necesarias: list[str]
    merge_strategy: Literal["join", "relacional"]
    razon: str


class SubTaskDefinition(BaseModel):
    sub_agent_id: str  # "agent_red", "agent_social", etc.
    endpoint: str
    params: dict
    descripcion: str  # qué se espera obtener


class TaskDecomposition(BaseModel):
    sub_tasks: list[SubTaskDefinition]
    merge_strategy: Literal["join", "relacional"]
    join_key: str | None = None  # "cluster" para joins exactos


class ReflectionOutput(BaseModel):
    quality_score: float = Field(ge=0.0, le=1.0)
    es_suficiente: bool
    problemas: list[str]
    feedback_al_formatter: str
    necesita_retry: bool


class FormatterOutput(BaseModel):
    respuesta_ia: str = Field(min_length=10)
    visualizacion_sugerida: Literal[
        "mapa_brechas", "mapa_indicadores", "tabla_datos", "grafico_barras"
    ]


class ClarificationDecision(BaseModel):
    necesita_clarificacion: bool
    pregunta: str | None = None
    opciones: list[str] | None = None
    razon: str = ""
