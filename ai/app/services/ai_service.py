
from app.models.schemas import ConsultaRequest, ConsultaResponse


class AIService:
    async def process_query(self, request: ConsultaRequest) -&gt; ConsultaResponse:
        """
        Procesa una consulta del usuario con datos mockeados
        """
        # Datos mockeados basados en los contratos
        mock_response = ConsultaResponse(
            respuesta_ia="En SAO_JOSE_KOBRASOL hay 8.200 personas con cobertura WCDMA precaria y ningún programa activo. Es la zona de mayor brecha para jóvenes de income D.",
            datos=[
                {
                    "cluster": "SAO_JOSE_KOBRASOL",
                    "periodo": "MANHA",
                    "n_usuarios": 8200,
                    "congestionamento_medio": 0.68,
                    "taxa_internacao_psiquiatrica": 14.2
                }
            ],
            fuentes=[
                {"nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10"},
                {"nombre": "DATASUS", "codigo_origem": "SIH-SUS", "fecha_referencia": "2025-12-01"}
            ],
            visualizacion_sugerida="mapa_brechas",
            idioma=request.idioma
        )
        
        return mock_response

