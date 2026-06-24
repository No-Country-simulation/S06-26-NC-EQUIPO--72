
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse


class AIService:
    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        """
        Procesa una consulta del usuario con datos mockeados
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

        # Verifica si la consulta es irrelevante
        consulta_lower = request.consulta.lower()
        if "boca" in consulta_lower or "clima" in consulta_lower or "comida" in consulta_lower:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "CONSULTA_IRRELEVANTE",
                    "mensaje": "La consulta no puede resolverse con los datos disponibles."
                }
            )

        # Datos mockeados basados en el contrato (ejemplo 1: formaciones)
        respuesta_ia = "En la región FPOLIS_NORTE hay 8.200 personas en horario laboral con cobertura WCDMA precaria y ningún programa de formación activo. Es la zona de mayor brecha para jóvenes de income D."
        datos = [
            {
                "cluster": "FPOLIS_NORTE",
                "municipio": "Florianópolis",
                "n_usuarios": 8200,
                "congestionamento_medio": 0.81,
                "programas_activos": 0,
                "severidad_brecha": "ALTA"
            }
        ]
        fuentes = [
            {"nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10"},
            {"nombre": "DATASUS", "codigo_origem": "SIH-SUS", "fecha_referencia": "2025-12-01"}
        ]
        visualizacion_sugerida = "mapa_brechas"
        
        return ConsultaResponse(
            respuesta_ia=respuesta_ia,
            datos=datos,
            fuentes=fuentes,
            visualizacion_sugerida=visualizacion_sugerida,
            idioma=request.idioma
        )

