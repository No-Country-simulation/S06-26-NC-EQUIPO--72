
from pydantic import BaseModel, Field


class ConsultaRequest(BaseModel):
    consulta: str
    filtros: dict = Field(default_factory=dict)
    idioma: str = "es"


class ConsultaResponse(BaseModel):
    respuesta_ia: str
    datos: list
    fuentes: list
    visualizacion_sugerida: str
    idioma: str

