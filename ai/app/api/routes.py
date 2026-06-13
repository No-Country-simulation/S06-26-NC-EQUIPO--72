
from fastapi import APIRouter
from app.controllers.ai_controller import AIController
from app.models.schemas import ConsultaRequest, ConsultaResponse

router = APIRouter()
ai_controller = AIController()


@router.post("/consulta", response_model=ConsultaResponse)
async def consulta(request: ConsultaRequest) -> ConsultaResponse:
    """
    Endpoint para enviar consultas al agente de IA
    """
    return await ai_controller.handle_consulta(request)

