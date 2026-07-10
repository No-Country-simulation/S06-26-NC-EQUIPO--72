import logging
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse
from app.agent.graph import agent

logger = logging.getLogger(__name__)



class AIService:
    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Procesa una consulta del usuario
        """
        try:
            # Ejecuta el agente
            state = await agent.ainvoke({
                "consulta": request.consulta,
                "idioma": request.idioma,
                "filtros": {},
            })
            
            if state.get("fuera_de_dominio"):
                raise HTTPException(
                    status_code=422,
                    detail={
                        "error": "CONSULTA_FUERA_DE_DOMINIO",
                        "mensaje": state.get("respuesta_ia"),
                    }
                )
            
            # Extrae los datos de la respuesta
            tool_results = state.get("tool_results", {})
            datos = tool_results if isinstance(tool_results, list) else []

            return ConsultaResponse(
                respuesta_ia=state.get("respuesta_ia", ""),
                datos=datos,
                fuentes=state.get("fuentes", []),
                visualizacion_sugerida=state.get("visualizacion_sugerida", "tabla_datos"),
                idioma=request.idioma,
            )

        except HTTPException:
            raise  # re-lanza HTTPExceptions sin modificar

        except Exception as e:
            logger.exception("Error inesperado procesando consulta: %s", request.consulta)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "ERROR_INTERNO",
                    "mensaje": "Ocurrió un error procesando la consulta.",
                }
            )
