
# App BiT — AI Service

Agente de IA para consultas en lenguaje natural sobre datos de inclusión social.

## Documentación de la API (Swagger UI)

¡La documentación interactiva está disponible automáticamente con FastAPI!
- **Swagger UI**: `http://localhost:8000/docs` — Probar los endpoints directamente desde el navegador
- **Redoc**: `http://localhost:8000/redoc` — Documentación más limpia
- **OpenAPI Schema**: `http://localhost:8000/openapi.json` — Esquema JSON de la API

## Endpoints disponibles

| Método | Ruta       | Descripción                                    |
|--------|------------|------------------------------------------------|
| GET    | `/health`  | Verificar el estado del servicio               |
| POST   | `/consulta`| Enviar una consulta al agente de IA            |

## Configuración (Docker - Recomendado para desarrollo)

1. Copiar y configurar variables de entorno:
    ```bash
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

