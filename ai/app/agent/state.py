from typing import TypedDict


class AgentState(TypedDict):
    consulta: str
    filtros: dict
    idioma: str
    plan: dict
    schema_decision: dict
    tool_results: dict
    respuesta_ia: str
    visualizacion_sugerida: str
    fuentes: list
    fuera_de_dominio: bool 
