
# Estructura del Servicio AI

El servicio AI está organizado en una arquitectura por capas para mantener la separación de responsabilidades:

```
ai/
├── app/
│   ├── agent/              # Lógica del agente LangChain/LangGraph
│   │   ├── graph.py       # Definición del grafo del agente
│   │   ├── prompts.py     # Prompts del sistema
│   │   └── tools.py       # Herramientas del agente
│   ├── api/                # Capa de rutas/endpoints
│   │   └── routes.py      # Definición de endpoints FastAPI
│   ├── controllers/        # Capa de controladores
│   │   └── ai_controller.py  # Manejo de requests/responses
│   ├── core/               # Configuración y utilidades core
│   │   └── config.py      # Configuración del servicio (Pydantic Settings)
│   ├── middlewares/        # Middlewares FastAPI
│   │   └── logging_middleware.py  # Ejemplo de middleware de logging
│   ├── models/             # Pydantic schemas/models
│   │   └── schemas.py     # Schemas de request/response
│   ├── repositories/       # Capa de acceso a datos (para Qdrant, etc.)
│   ├── services/           # Capa de lógica de negocio
│   │   └── ai_service.py  # Lógica del servicio AI
│   └── vectorstore/        # Lógica de vector store (Qdrant)
│       └── qdrant.py
├── main.py                 # Punto de entrada de la aplicación FastAPI
├── Dockerfile
├── requirements.txt
└── README.md
```

## Descripción de Capas

1. **api**: Define los endpoints de la API REST usando FastAPI.
2. **controllers**: Maneja las solicitudes HTTP, valida inputs y coordina con la capa de servicios.
3. **services**: Contiene la lógica de negocio principal del servicio AI.
4. **models**: Define los schemas Pydantic para validar requests y responses.
5. **agent**: Contiene la lógica específica del agente LangChain/LangGraph (prompts, tools, grafo).
6. **vectorstore**: Lógica para interactuar con el vector store (Qdrant).
7. **middlewares**: Middlewares para procesar solicitudes/respuestas (ej: logging, autenticación).
8. **core**: Configuración general del servicio y utilidades compartidas.
9. **repositories**: Capa de abstracción para acceso a datos (si se integra más fuentes de datos).

