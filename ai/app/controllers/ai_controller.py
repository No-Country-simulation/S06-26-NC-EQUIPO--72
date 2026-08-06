
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse, ResumeRequest
from app.services.ai_service import AIService


class AIController:
    def __init__(self):
        self.ai_service = AIService()

    async def handle_consulta(self, request: ConsultaRequest) -> ConsultaResponse:
        return await self.ai_service.process_query(request)

    async def handle_resume(self, request: ResumeRequest) -> ConsultaResponse:
        return await self.ai_service.resume_query(request)
