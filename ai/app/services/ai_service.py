import os
import pandas as pd
from fastapi import HTTPException
from app.models.schemas import ConsultaRequest, ConsultaResponse

class AIService:
    def __init__(self):
        self.ruta_movilidad = "ai/data/mobilidade_agregada.csv"
        self.ruta_indicadores = "ai/data/indicadores_territoriales.csv"

    def _cargar_datasets(self):
        if not os.path.exists(self.ruta_movilidad) or not os.path.exists(self.ruta_indicadores):
            raise HTTPException(
                status_code=500,
                detail="Error interno: Archivos del dataset ausentes en el servidor de IA."
            )
        return pd.read_csv(self.ruta_movilidad), pd.read_csv(self.ruta_indicadores)

    async def process_query(self, request: ConsultaRequest) -> ConsultaResponse:
        if not request.consulta or request.consulta.strip() == "":
            raise HTTPException(
                status_code=422,
                detail={"error": "CONSULTA_VACIA", "mensaje": "La consulta no puede ser vacía."}
            )

        consulta_lower = request.consulta.lower()
        df_movilidad, df_indicadores = self._cargar_datasets()

        municipio_target = "Florianópolis"
        if "josé" in consulta_lower or "são josé" in consulta_lower:
            municipio_target = "São José"
        elif "palhoça" in consulta_lower:
            municipio_target = "Palhoça"
        elif "biguaçu" in consulta_lower:
            municipio_target = "Biguaçu"

        cluster_target = "FPOLIS_NORTE"
        if "sur" in consulta_lower or "sul" in consulta_lower:
            cluster_target = "FPOLIS_SUL"
        elif "centro" in consulta_lower:
            cluster_target = "FPOLIS_CENTRO"
        elif "continente" in consulta_lower:
            cluster_target = "FPOLIS_CONTINENTE"

        datos_filtrados = df_movilidad[
            (df_movilidad['municipio'].str.lower() == municipio_target.lower()) & 
            (df_movilidad['cluster'] == cluster_target)
        ]

        if datos_filtrados.empty:
            datos_filtrados = df_movilidad[df_movilidad['municipio'].str.lower() == municipio_target.lower()]

        if datos_filtrados.empty:
            raise HTTPException(
                status_code=422,
                detail={"error": "SIN_DATOS", "mensaje": f"No se encontraron registros de simulación para {municipio_target}."}
            )

        n_usuarios_real = int(datos_filtrados['n_usuarios'].sum()) if 'n_usuarios' in datos_filtrados.columns else len(datos_filtrados)
        congestion_real = float(datos_filtrados['congestionamento_medio'].mean()) if 'congestionamento_medio' in datos_filtrados.columns else 0.0
        severidad_real = "ALTA" if congestion_real > 0.70 else "MEDIA" if congestion_real > 0.40 else "BAJA"

        indicadores_municipio = df_indicadores[df_indicadores['municipio'].str.lower() == municipio_target.lower()]
        programas_activos_real = int(indicadores_municipio['programas_activos'].sum()) if 'programas_activos' in indicadores_municipio.columns else 0

        respuesta_ia = (
            f"Análisis de IA basado en el volumen estructurado de 'mobilidade_agregada' para {municipio_target}: "
            f"Se procesó el escenario en el cluster {cluster_target}, detectando un nivel de congestionamiento medio de {congestion_real:.2f}. "
            f"Cruzando esto con los indicadores territoriales del municipio, se registran {programas_activos_real} programas activos. "
            f"Dada la presencia de {n_usuarios_real} usuarios en los segmentos afectados, la severidad se determina como {severidad_real}."
        )
        
        datos = [
            {
                "cluster": cluster_target,
                "municipio": municipio_target,
                "n_usuarios": n_usuarios_real,  
                "congestionamento_medio": round(congestion_real, 2),
                "programas_activos": programas_activos_real,
                "severidad_brecha": severidad_real
            }
        ]
        
        fuentes = [
            {"nombre": "Dataset Movilidad Integrado (mobilidade_agregada)", "codigo_origem": "mobilidade_agregada", "fecha_referencia": "2026-03-10"},
            {"nombre": "Indicadores Territoriales (DATASUS)", "codigo_origem": "indicadores_territoriales", "fecha_referencia": "2025-12-01"}
        ]
        
        return ConsultaResponse(
            respuesta_ia=respuesta_ia,
            datos=datos,
            fuentes=fuentes,
            visualizacion_sugerida="mapa_brechas",
            idioma=request.idioma
        )