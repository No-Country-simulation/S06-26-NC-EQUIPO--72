
# App BiT — AI Service

Agente de IA para consultas en lenguaje natural sobre datos de inclusión social, con pipeline ETL integrado para cargar datos desde CSVs.

## Estructura del Proyecto

```
ai/
├── app/
│   ├── api/          # Rutas de la API FastAPI
│   ├── controllers/  # Logica de controladores
│   ├── core/         # Configuración y variables de entorno
│   ├── etl/          # Pipeline ETL (carga CSVs a BD)
│   │   ├── __init__.py
│   │   ├── database.py  # Conexión a BD y espera a que esté lista
│   │   ├── loaders.py   # Carga y transformación de cada tabla
│   │   └── pipeline.py  # Orquestador principal
│   ├── models/       # Modelos de datos (Pydantic)
│   ├── services/     # Logica de negocio
│   ├── vectorstore/  # Integración con Qdrant (opcional)
│   └── agent/        # Agente de IA (LangChain/LangGraph)
├── data/             # Carpeta para datasets CSV (ignorada por Git)
├── data_resultado/   # Resultados de análisis
├── main.py           # Punto de entrada FastAPI
├── check_csv.py  # Script para ver columnas y filas de los CSV
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

## Preparación de Datasets y Pipeline ETL

### 1. Obtener los datasets
Los archivos CSV están disponibles en este [Google Drive](https://drive.google.com/drive/folders/1nXCg4Il5vmBI_5aldhNMPfAdp_dQyobE?usp=sharing) 

> **Nota:** los CSV de esta carpeta ya están **saneados y corregidos**. No es necesario volver a ejecutar el script de corrección sobre estos archivos.

Descarga y colócalos en la carpeta `ai/data/`:

```
ai/data/
├── antenas_flp.csv
├── assinantes.csv
├── tensor_concentracao.csv
├── tensor_mobilidade.csv
├── tensor_od.csv
└── tensor_fluxo_vias.csv
```

### 2. Corregir `tensor_od.csv` (solo si usás el CSV sin sanear)
Si por algún motivo trabajás con una versión de `tensor_od.csv` que **no** proviene del Drive saneado, este archivo puede tener 44 valores nulos que hay que corregir primero:
```bash
cd ai
python corregir_tensor_od.py
```
Este script:
- Crea un backup del original (`tensor_od.csv.original`)
- Usa `antenas_flp.csv` para recuperar la información correcta de `SAO_JOSE_ROÇADO`
- Corrige las coordenadas que estaban en `0.0, 0.0`
- Guarda el CSV corregido

### 3. Verificar columnas de los CSV
Opcionalmente, puedes ver las columnas de cada CSV:
```bash
python check_csv.py
```

### 4. Pipeline ETL Automático
El pipeline ETL se ejecuta **automáticamente al iniciar el servicio AI** (con el perfil `dev` del Backend).

Lo que hace:
1. Espera que la base de datos MySQL esté lista
2. Lee y carga los CSV en orden (respetando dependencias de claves foráneas)
3. Aplica transformaciones:
   - Convierte `download_bytes` a `download_gb` (divide por 1e9)
   - Renombra columnas (ej: `periodo_sessao` → `periodo`)
   - Carga `tensor_mobilidade.csv` en trozos (por ser ~2.7GB)
4. Inserta los datos en la BD

## Configuración (Docker - Recomendado para desarrollo)

1. Copiar y configurar variables de entorno (para el AI Service):
    ```bash
    cd ai
    cp .env.example .env
    ```
    Edita `.env` con tus credenciales de OpenRouter y otras configuraciones.

2. Configurar variables de entorno del proyecto raíz:
    ```bash
    cd /home/lagorda/S06-26-NC-EQUIPO--72
    cp .env.example .env
    ```
    Edita `.env` y elige el perfil (`dev` o `dev-mock-csv`).

3. Iniciar el servicio con Docker Compose (desde la raíz del proyecto):
    ```bash
    docker-compose up --build
    ```

4. El servicio estará disponible en `http://localhost:8000`.

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

4. Asegúrate de tener la BD MySQL corriendo y configurada correctamente.

5. Ejecutar el servicio:
    ```bash
    uvicorn main:app --reload
    ```

## Scripts Útiles

- **`corregir_tensor_od.py`**: Corrige valores nulos en `tensor_od.csv`
- **`check_csv.py`**: Muestra las columnas y filas de cada CSV en la carpeta `data/`
- **`analisis_preguntas_clave.py`**: Análisis de datos para las 3 preguntas clave del desafío

