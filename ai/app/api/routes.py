
from fastapi import APIRouter
from app.controllers.ai_controller import AIController
from app.models.schemas import ConsultaRequest, ConsultaResponse, ResumeRequest

router = APIRouter()
ai_controller = AIController()


@router.post("/consulta", response_model=ConsultaResponse)
async def consulta(request: ConsultaRequest) -> ConsultaResponse:
    """
    Endpoint para enviar consultas al agente de IA
    """
    return await ai_controller.handle_consulta(request)


@router.post("/consulta/respuesta", response_model=ConsultaResponse)
async def resume_consulta(request: ResumeRequest) -> ConsultaResponse:
    """
    Reanuda una consulta pausada con la respuesta del gestor.
    Requiere session_id devuelto por POST /consulta cuando
    requiere_clarificacion era true.
    """
    return await ai_controller.handle_resume(request)
