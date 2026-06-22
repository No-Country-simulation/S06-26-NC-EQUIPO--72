
# App BiT — AI Service

Agente de IA para consultas en lenguaje natural sobre datos de inclusión social.

## Estructura del Proyecto

```
ai/
├── app/
│   ├── api/          # Rutas de la API FastAPI
│   ├── controllers/  # Logica de controladores
│   ├── core/         # Configuración y variables de entorno
│   ├── models/       # Modelos de datos (Pydantic)
│   ├── services/     # Logica de negocio
│   ├── vectorstore/  # Integración con Qdrant (opcional)
│   └── agent/        # Agente de IA (LangChain/LangGraph)
├── data/             # Carpeta para datasets CSV (ignorada por Git)
├── data_resultado/   # Resultados de análisis
├── main.py           # Punto de entrada FastAPI
└── corregir_tensor_od.py  # Script para corregir valores nulos en tensor_od.csv
```

## Documentación de la API (Swagger UI)

La documentación interactiva está disponible automáticamente con FastAPI
- **Swagger UI**: `http://localhost:8000/docs` — Probar los endpoints directamente desde el navegador
- **Redoc**: `http://localhost:8000/redoc` — Documentación más limpia
- **OpenAPI Schema**: `http://localhost:8000/openapi.json` — Esquema JSON de la API

## Endpoints disponibles

| Método | Ruta       | Descripción                                    |
|--------|------------|------------------------------------------------|
| GET    | `/health`  | Verificar el estado del servicio               |
| POST   | `/consulta`| Enviar una consulta al agente de IA            |

## Preparación de Datasets

1. Colocar todos los archivos CSV del dataset Vísent CDRView en la carpeta `ai/data/`
2. Corregir `tensor_od.csv` (soluciona 44 valores nulos):
    ```bash
    cd ai
    python corregir_tensor_od.py
    ```
    Este script:
    - Crea un backup del original (`tensor_od.csv.original`)
    - Usa `antenas_flp.csv` para recuperar la información correcta de `SAO_JOSE_ROÇADO`
    - Corrige las coordenadas que estaban en `0.0, 0.0`
    - Guarda el CSV corregido

## Configuración (Docker - Recomendado para desarrollo)

1. Copiar y configurar variables de entorno:
    ```bash
    cd ai
    cp .env.example .env
    ```
    Edita `.env` con tus credenciales de OpenRouter y otras configuraciones.

2. Iniciar el servicio con Docker Compose (desde la raíz del proyecto):
    ```bash
    docker-compose up --build
    ```

3. El servicio estará disponible en `http://localhost:8000`.

## Ejecución local (sin Docker)

Si prefieres correr el servicio sin Docker:

1. Crear entorno virtual:
    ```bash
    python -m venv venv
    ```

2. Activar entorno virtual:
    - Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    - Windows:
        ```bash
        venv\Scripts\activate
        ```

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Ejecutar el servicio:
    ```bash
    uvicorn main:app --reload
    ```

## Scripts Útiles

- **`corregir_tensor_od.py`**: Corrige valores nulos en `tensor_od.csv`
- **`analisis_preguntas_clave.py`**: Análisis de datos para las 3 preguntas clave del desafío

