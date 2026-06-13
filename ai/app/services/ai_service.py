
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.agent.graph import agent


class AIService:
    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Procesa una consulta del usuario usando el agente LangGraph
        """
        result = await agent.ainvoke({
            "consulta": request.consulta,
            "filtros": request.filtros,
            "idioma": request.idioma,
            "plan": {},
            "tool_results": {},
            "respuesta_ia": "",
            "visualizacion_sugerida": "",
            "fuentes": []
        })

        datos = []
        if "datos" in result.get("tool_results", {}):
            datos = result["tool_results"]["datos"]
        elif "brechas" in result.get("tool_results", {}):
            datos = result["tool_results"]["brechas"]

        return ConsultaResponse(
            respuesta_ia=result["respuesta_ia"],
            datos=datos,
            fuentes=result["fuentes"],
            visualizacion_sugerida=result["visualizacion_sugerida"],
            idioma=request.idioma
        )

