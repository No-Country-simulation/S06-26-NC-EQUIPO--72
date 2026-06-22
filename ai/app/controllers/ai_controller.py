
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.services.ai_service import AIService


class AIController:
    def __init__(self):
        self.ai_service = AIService()

    async def handle_consulta(self, request: ConsultaRequest) -> ConsultaResponse:
        return await self.ai_service.process_query(request)

