
# Arquitectura de Integración de IA



## 1. Resumen de la Arquitectura

Esta arquitectura describe la integración end-to-end del servicio de IA con el resto del sistema, desde la solicitud del frontend hasta la respuesta final.

### Componentes Principales

| Componente       | Tecnología       | Responsabilidad Principal                                                                 |
|------------------|------------------|-------------------------------------------------------------------------------------------|
| **Frontend**     | React            | Interfaz de usuario, envía consultas en lenguaje natural y visualiza resultados           |
| **Backend**      | Spring Boot      | Proxy seguro, validación básica, orquestación de flujos y acceso a DB                     |
| **AI Service**   | FastAPI + LangGraph | Grafo multi-agente: clasificación, schema linking, tool calling (endpoints / Text-to-SQL), ReAct + reflexión. LLMs vía Groq (con fallback a Gemini) y embeddings en Qdrant |
| **Base de Datos**| MySQL            | Almacenamiento de datos de Vísent, indicadores territoriales y programas sociales          |
| **Qdrant**       | Qdrant           | Vector store con embeddings de endpoints y tablas para el schema linking                  |
| **Docker**       | Docker Compose   | Orquestación de contenedores para entorno de desarrollo/producción                         |

---

## 2. Principio Clave de la Integración

**Regla de Prioridad para Obtener Datos:**
1. **Primero**: Usar endpoints existentes del backend (como `/brechas`, `/mapa`, `/programas`, `/indicadores/evolucion`)
2. **Solo si no hay alternativa**: Usar Text-to-SQL para consultas sencillas

---

## 3. Flujo Principal (POST /datos)

El flujo principal es para el uso del frontend, donde el usuario envía una consulta en lenguaje natural.

```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    participant AIService as AI Service
    participant DB as Base de Datos

    Frontend->>Backend: POST /api/datos {consulta, idioma}
    activate Backend

    Backend->>Backend: Validación básica (campos requeridos)
    Backend->>AIService: POST /consulta {consulta, idioma}
    activate AIService

    AIService->>AIService: Analizar consulta y determinar tools necesarias
    alt Si la consulta requiere datos complejos (brechas)
        AIService->>Backend: GET /api/brechas {servicio, municipio, ...}
        activate Backend
        Backend->>DB: Consultar datos (cruzar Vísent, indicadores, programas)
        DB-->>Backend: Resultados de brechas
        Backend-->>AIService: Respuesta 200 {brechas, criterio}
        deactivate Backend
    else Si la consulta requiere datos específicos
        AIService->>AIService: Text-to-SQL (generar consulta SQL)
        AIService->>DB: Ejecutar SQL (solo lectura)
        DB-->>AIService: Resultados SQL
    end

    AIService->>AIService: Generar respuesta estructurada (respuesta_ia, datos, fuentes, visualizacion_sugerida)
    AIService-->>Backend: Respuesta 200 {respuesta_ia, datos, fuentes, visualizacion_sugerida, idioma}
    deactivate AIService

    Backend->>Backend: Calcular total_registros = len(datos)
    Backend-->>Frontend: Respuesta 200 {respuesta_ia, visualizacion_sugerida, datos, fuentes, total_registros, idioma}
    deactivate Backend
```

### Detalles Paso a Paso

1. **Solicitud Frontend -> Backend**
   - El frontend envía una consulta en lenguaje natural y el idioma deseado
   - Endpoint: `POST /api/datos`
   - El backend valida que los campos `consulta` estén presentes

2. **Proxy Backend -> AI Service**
   - El backend actúa como puente seguro:
     - Autenticación/autorización (si es necesario en el futuro)
     - Rate limiting
     - Logging
     - Transformación de formato de datos si es necesario
   - Endpoint AI Service: `POST /consulta`

3. **Razonamiento AI Service (Sigue la Regla de Prioridad)**
   - El AI Service analiza la consulta y decide la mejor fuente de datos:
     a. **Primero**: ¿Hay un endpoint del backend que ya devuelve estos datos? (ej: `/brechas`, `/mapa`, `/programas`)
     b. **Solo si no**: Usar Text-to-SQL para consultas sencillas

4. **Obtención de Datos**
   - **Opción 1 (Endpoints del Backend - Prioridad Alta):**
     - El AI Service llama al endpoint correspondiente del backend
     - El backend consulta la DB y devuelve datos estructurados
   - **Opción 2 (Text-to-SQL):**
     - El AI Service genera SQL y lo ejecuta directamente contra la DB (solo permisos de lectura)
     - **Solo para consultas sencillas** que no tienen endpoint en el backend

5. **Generación de Respuesta AI Service**
   - El AI Service genera una respuesta estructurada con:
     - `respuesta_ia`: Explicación en lenguaje natural
     - `datos`: Datos crudos para visualizar
     - `fuentes`: Orígenes de los datos
     - `visualizacion_sugerida`: Tipo de gráfico/mapa recomendado
     - `idioma`: Idioma de la respuesta

6. **Respuesta Backend -> Frontend**
   - El backend calcula `total_registros` (tamaño de la lista `datos`)
   - El backend devuelve la respuesta final al frontend

### 3.1 Pipeline interno del AI Service (grafo multi-agente)

Dentro de `POST /consulta`, la consulta atraviesa un grafo de nodos LangGraph que sanitiza, clasifica, rutea, obtiene datos y refleja sobre la respuesta:

```
Flujo simple:      input_guardrail → planner → query_classifier → schema_linker
                   → tool_caller ⇄ react_reasoner (si datos vacíos)
                   → output_guardrail → formatter → reflector
Flujo compuesto:   input_guardrail → planner → query_classifier → task_decomposer
                   → parallel_executor → result_merger → output_guardrail
                   → formatter → reflector
Fuera de dominio:  planner → fuera_de_dominio → END (422 CONSULTA_IRRELEVANTE)
```

- **planner**: clasifica la intención y extrae filtros (servicio, municipio, indicador, periodo). Modelo ligero.
- **query_classifier**: decide simple vs compuesta.
- **schema_linker**: decide endpoint del backend o Text-to-SQL usando reglas determinísticas + embeddings de Qdrant.
- **tool_caller / react_reasoner**: ejecuta la decisión; si el tool devuelve datos vacíos, razona y reintenta (ReAct).
- **formatter / reflector**: genera la respuesta final y evalúa su calidad, reformateando si es pobre (Reflexion).

**Fallback de modelos:** los nodos usan dos modelos de Groq (`llama-3.1-8b-instant` y `llama-3.3-70b-versatile`). Ante rate-limit (TPM/TPD) o error transitorio de Groq, cada llamada cae automáticamente a `gemini-3.1-flash-lite` (pool de límites separado) en vez de esperar.

---

## 4. Flujo de Error (Consulta Irrelevante)

Si la consulta no puede resolverse con los datos disponibles:

```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    participant AIService as AI Service

    Frontend->>Backend: POST /api/datos {consulta: "¿Cómo está el clima?"}
    activate Backend

    Backend->>AIService: POST /consulta {consulta, idioma}
    activate AIService

    AIService->>AIService: Detectar consulta irrelevante
    AIService-->>Backend: Respuesta 422 {error: "CONSULTA_IRRELEVANTE", mensaje: "..."}
    deactivate AIService

    Backend-->>Frontend: Respuesta 422 {error: "CONSULTA_IRRELEVANTE", mensaje: "..."}
    deactivate Backend
```

---

## 5. Consideraciones Clave y Alternativas

### 5.1 ¿Por qué priorizar endpoints del backend sobre Text-to-SQL?

1. **Control de acceso a datos**: Todo el acceso a la DB está centralizado en el backend
2. **Mantenibilidad**: La lógica de consulta compleja está en un solo lugar
3. **Seguridad**: El AI Service no necesita acceso directo a la DB para consultas comunes
4. **Rendimiento**: Los endpoints del backend ya estarán optimizados y testeados

### 5.2 ¿Cuándo usar Text-to-SQL?

Solo cuando:
- La consulta es **sencilla**
- No existe un endpoint en el backend que devuelva esos datos
- Es una consulta de lectura única (SELECT)

**Importante:**
- El AI Service **solo debe tener permisos de lectura** en la DB
- Las consultas deben estar limitadas en tiempo (timeout) para evitar cargas excesivas


## 6. Diagrama de Arquitectura General

```mermaid
graph TD
    Frontend[React Frontend]
    Backend[Spring Boot Backend]
    AIService[FastAPI AI Service]
    DB[(MySQL DB)]
    Qdrant[Qdrant Vector Store]
    
    Frontend -- POST /datos --> Backend
    Backend -- POST /consulta --> AIService
    AIService -- GET /brechas, /mapa, /indicadores/evolucion, etc. --> Backend
    AIService -- SQL Lectura --> DB
    Backend -- SQL --> DB
    AIService -- embeddings --> Qdrant
```

---

## 7. Seguridad

- **Autenticación:** En producción, el backend y el AI Service deben autenticarse entre sí (ej: API keys, OAuth2)
- **Permisos DB:** El usuario de DB para el AI Service solo debe tener permisos de SELECT
- **Rate Limiting:** El backend debe limitar la cantidad de consultas por usuario para evitar abusos
- **Sanitización:** El AI Service debe validar y sanitizar cualquier SQL generado para evitar inyecciones

---

## 8. Logging y Monitoreo

- **Backend:** Loguear todas las solicitudes y respuestas del endpoint /datos
- **AI Service:** Loguear:
  - Consultas recibidas
  - Tools utilizadas
  - SQL generado (solo si se usa)
  - Tiempo de respuesta
- **Monitoreo:** Alertas por tiempos de respuesta lentos o errores frecuentes

---

## 9. Resumen de Contratos Relacionados

Para más detalles:
- [API_CONTRATOS.md](./API_CONTRATOS.md): Contratos entre frontend y backend
