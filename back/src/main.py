from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="App BiT - API Backend MVP (Issue 10)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "proyecto": "App BiT - Grupo 72"}

@app.post("/api/datos")
async def post_datos_mock(request: Request):
    body = await request.json()
    user_query = body.get("consulta", "¿Cuál es el estado de la conectividad?")

    return {
        "metadata": {
            "region_piloto": "Florianopolis",
            "indicador_defecto": "Empleabilidad",
            "idioma": "es",
            "k_anonimato": 3,
            "fuente": "Vísent CDRView STEP Platform"
        },
        "consulta": user_query,
        "respuesta_ia": "Análisis del Agente (MOCK): Se detectó que el clúster SAO_JOSE_KOBRASOL presenta un alto volumen de transiciones durante el período MANHA, lo que indica alta movilidad laboral. Sin embargo, registra un nivel de congestión medio de 0.72. Se sugiere reforzar la infraestructura de red en este corredor.",
        "mapa_features": {
            "tipo_grafico": "corredores_flujo",
            "elementos": [
                {
                    "id_tramo": "72405_origen_destino",
                    "coordenadas": {
                        "origen": {"lat": -27.5950, "lon": -48.6300, "cluster": "SAO_JOSE_KOBRASOL"},
                        "destino": {"lat": -27.5954, "lon": -48.5480, "cluster": "CBD_BEIRAMAR"}
                    },
                    "metricas": {
                        "usuarios_unicos": 14500,
                        "transiciones_totales": 28000,
                        "porcentaje_flujo_origen": 45.5,
                        "congestion_promedio": 0.72
                    }
                }
            ]
        },
        "tarjetas_resumen": [
            {"titulo": "Densidad de Usuarios en Hora Pico", "valor": "Alta", "estado": "alerta"},
            {"titulo": "Tecnología Predominante", "valor": "LTE (4G)", "estado": "normal"}
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)