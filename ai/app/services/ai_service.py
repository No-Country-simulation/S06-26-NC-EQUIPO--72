
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.agent.graph import agent


class AIService:
    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Procesa una consulta del usuario
        """
        # Verifica si la consulta está vacía o solo tiene espacios
        if not request.consulta or request.consulta.strip() == "":
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "CONSULTA_IRRELEVANTE",
                    "mensaje": "La consulta no puede resolverse con los datos disponibles."
                }
            )

        try:
            # Ejecuta el agente
            state = await agent.ainvoke({
                "consulta": request.consulta,
                "idioma": request.idioma,
                "filtros": {}
            })

            # Obtiene los datos del estado del agente
            datos = []
            if state.get("tool_results", {}).get("datos"):
                datos = state["tool_results"]["datos"]
            elif state.get("tool_results", {}).get("brechas"):
                datos = state["tool_results"]["brechas"]

            # Construye la respuesta
            return ConsultaResponse(
                respuesta_ia=state.get("respuesta_ia", ""),
                datos=datos,
                fuentes=state.get("fuentes", []),
                visualizacion_sugerida=state.get("visualizacion_sugerida", "tabla_datos"),
                idioma=request.idioma
            )
        except Exception as e:
            # Si hay un error, devuelve CONSULTA_IRRELEVANTE
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "CONSULTA_IRRELEVANTE",
                    "mensaje": "La consulta no puede resolverse con los datos disponibles."
                }
            )
