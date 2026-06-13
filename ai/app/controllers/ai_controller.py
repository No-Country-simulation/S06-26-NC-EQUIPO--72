
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.services.ai_service import AIService


class AIController:
    def __init__(self):
        self.ai_service = AIService()

    async def handle_consulta(self, request: ConsultaRequest) -> ConsultaResponse:
        try:
            return await self.ai_service.process_query(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

