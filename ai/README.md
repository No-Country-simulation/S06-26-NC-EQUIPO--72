
# App BiT - AI Service

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
---

## Arquitectura interna

El AI Service implementa un grafo de nodos con LangGraph. Cada consulta pasa por cuatro nodos en secuencia:

```
[planner] -> [schema_linker] -> [tool_caller] -> [formatter]
```

### Nodos del grafo

**planner** - clasifica la intención de la consulta y determina qué tipo de dato se necesita (`SALUD_MENTAL`, `EMPLEO`, `FORMACION`, etc.).

**schema_linker** - decide cómo obtener los datos usando embeddings semánticos de los endpoints y tablas disponibles (ver sección Schema Linking más abajo). Esto determina si se llama a un endpoint del backend o se genera Text-to-SQL.

**tool_caller** - ejecuta la decisión del schema_linker: llama al endpoint del backend correspondiente o, como fallback, genera y ejecuta una consulta SQL de solo lectura contra la DB.

**formatter** - recibe los datos crudos retornados y genera la respuesta final en lenguaje natural con `respuesta_ia`, `datos`, `fuentes` y `visualizacion_sugerida`.

---

## Schema Linking con embeddings

El schema_linker usa Qdrant para decidir cómo resolver cada consulta sin gastar tokens en esa decisión. Al levantar el servicio, se indexan embeddings de:

- **Descripciones de endpoints** del backend (`GET /brechas`, `GET /mapa/indicadores`, `GET /programas`, etc.)
- **Descripciones de tablas** de la DB (`concentracao`, `indicadores_territoriales`, `programas_sociales`, etc.)

Cuando llega una consulta, el schema_linker busca similitud semántica en Qdrant y toma una decisión:

```
consulta: "¿dónde falta conectividad en zona norte?"
      
Schema Linker busca en Qdrant
      
Alta similitud con GET /brechas -> llama al endpoint
      
Baja similitud con todos los endpoints -> fallback a Text-to-SQL
      con el schema mínimo relevante (no el schema completo)
```

### ¿Por qué embeddings de tablas y no de filas?

Se indexan solo las descripciones de las tablas y endpoints (~10 textos cortos), no el contenido de las tablas. Esto mantiene el costo de tokens mínimo y el índice liviano. El embedding se calcula una sola vez al levantar el servicio.

---

## Regla de prioridad para obtener datos

```
1. Primero: llamar a un endpoint existente del backend
   (/brechas, /mapa, /mapa/indicadores, /programas)

2. Solo si ningún endpoint cubre la consulta:
   Text-to-SQL con permisos de solo lectura (SELECT)
```

### ¿Por qué esta prioridad?

Los endpoints del backend encapsulan lógica de negocio compleja (cruces entre Vísent, `indicadores_territoriales` y `programas_sociales`). Text-to-SQL sobre tablas crudas no puede replicar esa lógica sin riesgo de inconsistencias. El fallback a SQL existe para consultas simples que no tienen endpoint equivalente.

---

## Text-to-SQL (fallback)

Cuando el schema_linker no encuentra un endpoint con suficiente similitud semántica, el agente genera SQL usando solo el schema mínimo relevante identificado por el schema_linker (no el schema completo de la DB). Esto reduce el consumo de tokens aproximadamente un 75% comparado con Text-to-SQL clásico.

El usuario de DB asignado al AI Service tiene **solo permisos de SELECT** — nunca puede escribir, modificar ni eliminar datos.

---



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

