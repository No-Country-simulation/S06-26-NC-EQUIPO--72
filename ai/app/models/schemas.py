
from pydantic import BaseModel, Field


class ConsultaRequest(BaseModel):
    consulta: str
    filtros: dict = Field(default_factory=dict)
    idioma: str = "es"


class ConsultaResponse(BaseModel):
    respuesta_ia: str = ""
    datos: list = Field(default_factory=list)
    fuentes: list = Field(default_factory=list)
    visualizacion_sugerida: str = "tabla_datos"
    idioma: str = "es"
    # HITL: cuando el agente pausa para clarificar, se devuelven estos campos
    session_id: str | None = None
    requiere_clarificacion: bool = False
    pregunta_clarificacion: str | None = None
    opciones_clarificacion: list[str] | None = None


class ResumeRequest(BaseModel):
    session_id: str
    respuesta_gestor: str
