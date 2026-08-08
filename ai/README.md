# App BiT - AI Service

Agente de IA que responde consultas en lenguaje natural sobre datos de **inclusión social** en la Región Metropolitana de Florianópolis (RMF), Brasil. Implementado con **FastAPI + LangGraph**, LLMs vía **Groq** (con fallback a **Gemini**), embeddings en **Qdrant** y un **pipeline ETL** integrado que carga CSVs a MySQL al arrancar.

Este README documenta cómo funciona el sistema por dentro para que un desarrollador nuevo pueda entenderlo sin leer todo el código. Los archivos fuente se citan en cada sección para profundizar cuando haga falta.

---

## Índice

1. [Vista general de la arquitectura](#1-vista-general-de-la-arquitectura)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Ciclo de vida de una consulta](#3-ciclo-de-vida-de-una-consulta)
4. [El grafo multi-agente (LangGraph)](#4-el-grafo-multi-agente-langgraph)
5. [Nodos del grafo](#5-nodos-del-grafo)
6. [Estado compartido (AgentState)](#6-estado-compartido-agentstate)
7. [Capa de LLMs: modelos, rotación y fallback](#7-capa-de-llms-modelos-rotacin-y-fallback)
8. [Schema Linking: cómo se decide de dónde sacar los datos](#8-schema-linking-cmo-se-decide-de-dnde-sacar-los-datos)
9. [Herramientas (tools): endpoints y Text-to-SQL](#9-herramientas-tools-endpoints-y-text-to-sql)
10. [HITL: pausas de clarificación con el gestor](#10-hitl-pausas-de-clarificacin-con-el-gestor)
11. [Consultas compuestas: sub-agentes paralelos y merge](#11-consultas-compuestas-sub-agentes-paralelos-y-merge)
12. [Patrones de robustez: ReAct loop y Reflexión](#12-patrones-de-robustez-react-loop-y-reflexin)
13. [Seguridad: defensa contra prompt injection](#13-seguridad-defensa-contra-prompt-injection)
14. [DSPy: optimización offline de prompts (inactiva por defecto)](#14-dspy-optimizacin-offline-de-prompts-inactiva-por-defecto)
15. [Vectorstore (Qdrant)](#15-vectorstore-qdrant)
16. [Pipeline ETL](#16-pipeline-etl)
17. [Evaluaciones](#17-evaluaciones)
18. [Tests](#18-tests)
19. [Configuración y variables de entorno](#19-configuracin-y-variables-de-entorno)
20. [Endpoints de la API](#20-endpoints-de-la-api)
21. [Scripts útiles](#21-scripts-tiles)
22. [Documentación relacionada](#22-documentacin-relacionada)

---

## 1. Vista general de la arquitectura

```
                        ┌─────────────────────────────────────────────┐
                        │                  Backend                    │
                        │             Spring Boot (:8080)             │
                        │   /brechas /mapa /programas /indicadores... │
                        └───────┬───────────────────────────▲─────────┘
                                │ GET /api/...              │
                                │ (endpoints de negocio)    │ datos crudos
                        ┌───────▼───────────────────────────┴─────────┐
                        │               AI Service (FastAPI)          │
                        │                    :8000                     │
                        │  ┌──────────────────────────────────────┐    │
                        │  │   Grafo LangGraph (app/agent/)       │    │
                        │  │  input_guardrail -> planner -> ...     │    │
                        │  └───────────────────┬──────────────────┘    │
                        │            LLMs Groq │ fallback Gemini       │
                        │            (rotación de cuentas)             │
                        └───┬───────────────┬───────────────┬──────────┘
                            │               │               │
                    ┌───────▼─────┐  ┌──────▼──────┐  ┌─────▼──────────┐
                    │   MySQL     │  │   Qdrant    │  │  Google Gemini │
                    │ (Vísent +   │  │ (embeddings │  │ (embeddings +  │
                    │ indicadores)│  │  endpoints) │  │  fallback LLM) │
                    └─────────────┘  └─────────────┘  └────────────────┘
```

Componentes externos y su responsabilidad:

| Componente | Tecnología | Responsabilidad |
|---|---|---|
| **Frontend** | React | Muestra la consulta y el resultado (mapas, tablas, gráficos) |
| **Backend** | Spring Boot | Proxy seguro hacia el AI Service, expone los **endpoints de negocio** (`/brechas`, `/mapa`, `/programas`, `/indicadores/evolucion`, etc.) que cruzan Vísent + indicadores + programas |
| **AI Service** | FastAPI + LangGraph | Interpreta la consulta, decide la fuente de datos, la ejecuta y redacta la respuesta |
| **MySQL** | MySQL | Datos de red (Vísent), indicadores territoriales y programas sociales |
| **Qdrant** | Qdrant | Vector store con embeddings de endpoints/tablas para el schema linking |
| **Groq / Google** | API | LLMs primarios (Groq) y de respaldo (Gemini), embeddings (Gemini) |

**Principio clave de prioridad de datos** (ver `app/vectorstore/documents.py` y `docs/ARQUITECTURA_AI.md`):
1. **Primero**: llamar a un endpoint del backend (encapsula lógica de negocio compleja).
2. **Solo si ningún endpoint cubre la consulta**: Text-to-SQL con usuario de solo lectura.

---

## 2. Estructura del proyecto

```
ai/
├── main.py                     # Punto de entrada FastAPI: startup (ETL + vectorstore + limpieza HITL) + middlewares
├── app/
│   ├── agent/                  # ★ Núcleo del agente (LangGraph)
│   │   ├── graph.py            # Ensamblador del grafo (StateGraph): registra nodos y routing
│   │   ├── nodes/              # ★ Nodos del grafo, uno por archivo (planner, classifier, tool_caller, ...)
│   │   │   ├── planner.py      #   planner + normalización del plan
│   │   │   ├── classifier.py   #   query_classifier (simple/compuesta)
│   │   │   ├── decomposer.py   #   task_decomposer (compuestas)
│   │   │   ├── executor.py     #   parallel_executor + result_merger
│   │   │   ├── tool_caller.py  #   tool_caller + react_reasoner (loop ReAct)
│   │   │   ├── formatter.py    #   formatter + _corregir_visualizacion
│   │   │   ├── reflector.py    #   _gate_reflexion + reflector
│   │   │   ├── clarification.py#   clarification_detector + _integrar_respuesta_al_plan (HITL)
│   │   │   ├── fuera_de_dominio.py
│   │   │   └── routing.py      #   funciones _route_after_* (routing condicional)
│   │   ├── state.py            # AgentState (TypedDict) + getters seguros
│   │   ├── prompts.py          # Prompts de todos los nodos (PLANNER, FORMATTER, etc.) + preludio de seguridad
│   │   ├── schema_linker.py    # Reglas determinísticas + fallback a embeddings (Qdrant)
│   │   ├── tools.py            # llamar_endpoint() y ejecutar_sql() (Text-to-SQL) + hardening SQL
│   │   ├── sub_agent.py        # Ejecutor de sub-tareas de consultas compuestas (validación de allowlist)
│   │   ├── merge.py            # Join exacto en Python puro (_merge_join)
│   │   ├── guardrails.py       # input_guardrail y output_guardrail + detección de inyección/fuga
│   │   ├── security.py         # ★ Allowlists de endpoints/params + preludio y delimitadores instrucciones/datos
│   │   ├── normalizer.py       # Corrección determinística del plan (municipio/cluster/indicador)
│   │   ├── resumir.py          # Resumen/contexto para el formatter (envuelve datos como <datos_herramientas>)
│   │   ├── retry.py            # Decoradores tenacity: llm_retry y http_retry
│   │   ├── llm_layer.py        # ★ Construcción de chains, rotación de cuentas y _llm_ainvoke_con_fallback
│   │   ├── parsing.py          # ★ _extraer_json_con_fallback (parseo JSON robusto)
│   │   ├── output_schemas.py   # Schemas Pydantic de salida de cada nodo (structured output)
│   │   ├── json_utils.py       # Serialización de tipos MySQL (Decimal, date, timedelta)
│   │   ├── dspy_config.py      # LMs de DSPy (rotación de claves Groq) — solo offline
│   │   └── dspy_modules.py     # Módulos DSPy baseline (Planner/Classifier/Clarification)
│   ├── api/routes.py           # Rutas HTTP: POST /consulta, POST /consulta/respuesta
│   ├── controllers/ai_controller.py  # Capa de controlador (delgada)
│   ├── services/ai_service.py  # Lógica de negocio: timeout, idioma, HITL, sanitización, respuestas
│   ├── core/config.py          # Settings (pydantic-settings, lee .env) — incluye auth/rate-limit
│   ├── core/observability.py   # Activa tracing de LangSmith si está configurado
│   ├── models/schemas.py       # Pydantic: ConsultaRequest, ConsultaResponse, ResumeRequest
│   ├── middlewares/
│   │   ├── logging_middleware.py    # Header X-Process-Time
│   │   └── security_middleware.py   # ★ Auth por X-API-Key + rate limit por IP
│   ├── vectorstore/            # Qdrant: documents, indexer, searcher
│   └── etl/                    # pipeline.py, database.py, loaders_fast.py
├── dspy_optimize/              # Compilación MIPROv2 offline (compile, dataset, metrics, inspect)
├── evals/                      # Datasets golden/OOD y runner de evaluación
├── scripts/                    # Utilidades (corregir CSV, optimizar threshold, etc.)
├── tests/                      # Pytest (193 tests); conftest.py (raíz) con fixture de grafo aislado
├── data/                       # CSVs del ETL (ignorados por Git)
├── compiled_modules/           # Módulos DSPy compilados (VACÍO por defecto -> DSPy inactivo)
├── Dockerfile
├── requirements.txt
├── plan.md                     # Plan de trabajo DSPy (contexto histórico del proyecto)
└── README_DATASET.md           # Análisis del dataset
```

---

## 3. Ciclo de vida de una consulta

Flujo completo desde el HTTP request hasta la respuesta:

```
POST /consulta  ->  AIService.process_query()
  1. Detecta idioma (es/pt/en) con langdetect
  2. Pre-clasifica simple/compuesta (heurística sin LLM) para elegir timeout (30s/60s)
  3. ainvoke del grafo con un thread_id nuevo (checkpointer InMemorySaver)
  4. Si el grafo pausa (HITL) -> devuelve session_id + pregunta de clarificación
  5. Si el grafo termina -> limpia el thread y construye ConsultaResponse
  6. Manejo de errores: 504 timeout, 503 rate-limit/saturado, 422 fuera de dominio, 500 interno
```

Dentro del grafo (detalle en [§4](#4-el-grafo-multi-agente-langgraph)):

```
Flujo simple:
  input_guardrail -> planner -> clarification_detector -> query_classifier -> schema_linker
  -> tool_caller ⇄ (react_reasoner si datos vacíos) -> output_guardrail -> formatter -> reflector

Flujo compuesto:
  input_guardrail -> planner -> clarification_detector -> query_classifier -> task_decomposer
  -> parallel_executor -> result_merger -> output_guardrail -> formatter -> reflector

Fuera de dominio:
  input_guardrail -> planner -> fuera_de_dominio -> END  (o clarification_detector si es
  consulta corta ambigua -> query_classifier)

HITL (clarificación):
  clarification_detector pausa con interrupt() -> AI Service devuelve la pregunta
  -> POST /consulta/respuesta con session_id + respuesta_gestor -> el grafo reanuda
  -> el nodo integra la respuesta al plan y continúa
```

Ver `app/services/ai_service.py` para la capa de servicio y `app/agent/graph.py:79` (`build_graph`) para la construcción del grafo.

---

## 4. El grafo multi-agente (LangGraph)

Definido en `app/agent/graph.py:79` (`build_graph`), se construye con `StateGraph(AgentState)`. Un único grafo con routing condicional maneja todos los flujos (simple, compuesta, fuera de dominio, HITL). **Los nodos viven en `app/agent/nodes/`** (un archivo por nodo); `graph.py` solo los registra y conecta.

**Nodos registrados** (`graph.py:82`): `planner`, `fuera_de_dominio`, `input_guardrail`, `output_guardrail`, `clarification_detector`, `query_classifier`, `task_decomposer`, `parallel_executor`, `result_merger`, `schema_linker`, `tool_caller`, `react_reasoner`, `formatter`, `reflector`.

**Routing condicional** (funciones `_route_after_*`, definidas en `app/agent/nodes/routing.py`):

| Desde | Función de routing | Decisiones |
|---|---|---|
| `input_guardrail` | `_route_after_input_guardrail` | `END` si consulta inválida, si no `planner` |
| `planner` | `_route_after_planner` | `fuera_de_dominio` si el plan lo marca (salvo consulta corta ambigua, que NO es FOD); si no, siempre a `clarification_detector` (la clave "query_classifier" del mapa se enruta a ese nodo) |
| `query_classifier` | `_route_after_classifier` | `task_decomposer` si compuesta, si no `schema_linker` |
| `task_decomposer` | `_route_after_task_decomposer` | `parallel_executor` si logró descomponer, si no `schema_linker` (revertido a simple) |
| `tool_caller` | `_route_after_tool_caller` | `react_reasoner` si datos vacíos + hay retries + es simple, si no `output_guardrail` |
| `reflector` | `_route_after_reflector` | `formatter` si score pobre + hay presupuesto de retry, si no `END` |

**Checkpointer**: `_checkpointer = InMemorySaver()` global (`graph.py:75`). Es **requerido** para que `interrupt()` funcione (HITL). Tests y evals pasan su propia instancia (`build_graph(checkpointer=...)`) para no contaminar el de producción.

**Cómo se ejecuta el grafo**: `agent.ainvoke(initial_state, config)`. `config` lleva `thread_id` y `recursion_limit` (25). El estado inicial mínimo es `{consulta, idioma, request_id, filtros}`.

---

## 5. Nodos del grafo

Cada nodo es una función async que recibe el `state` completo y devuelve un `state` actualizado (patrón reducer de LangGraph). Salvo `input_guardrail`, `output_guardrail`, `schema_linker`, `tool_caller`, `parallel_executor`, `result_merger` y los routers, todos los nodos LLM usan el decorador `@llm_retry`.

### input_guardrail (`app/agent/guardrails.py`)
Determinístico, sin LLM. Valida que la consulta no esté vacía (< 3 chars -> corta con mensaje), la trunca a 500 chars y elimina caracteres de control. **Detecta prompt injection** (`_detectar_inyeccion`: regex + base64 largo + typoglycemia fuzzy) y corta el flujo con `flag_inyeccion` y una respuesta genérica de seguridad. Sanea el input antes de gastar cualquier llamada LLM.

### planner (`app/agent/nodes/planner.py:82`)
Clasifica la intención y extrae filtros. Usa el modelo **light** (`groq/compound-mini`) con **structured output** (Pydantic `PlanOutput`). Produce un `plan`:

```json
{
  "fuera_de_dominio": false,
  "servicio": "EMPLEO" | "FORMACION" | "MENTORIA" | "EXPERIENCIA" | "SALUD_MENTAL" | "EDUCACION" | null,
  "municipio": "Florianópolis" | "São José" | "Palhoça" | "Biguaçu" | null,
  "periodo": "MADRUGADA" | "MANHA" | "TARDE" | "NOITE" | null,
  "cluster": "TRINDADE" | ... (23 clusters) | null,
  "income_cluster": "A"|"B"|"C"|"D" | null,
  "indicador": "taxa_emprego_formal" | ... | null,
  "fecha": "YYYY-MM-DD" | null,
  "razon": "..."
}
```

- Antes de usar el resultado, pasa por `normalizar_plan()` (`app/agent/normalizer.py`): **corrección determinística post-LLM** de municipio/cluster/indicador contra listas canónicas (tolerando typos y tildes con `difflib`), infiere el `servicio` si quedó null y **revierte FOD alucinado** si la consulta tiene señales claras de dominio.
- Si el structured output falla, hay un fallback manual de parseo JSON (`_extraer_json_con_fallback`, `app/agent/parsing.py:8`) que nunca tira el pipeline.
- Si DSPy está habilitado (ver [§14](#14-dspy-optimizacin-offline-de-prompts-inactiva-por-defecto)), intenta primero el módulo compilado.

### fuera_de_dominio (`app/agent/nodes/fuera_de_dominio.py:28`)
Corta el flujo temprano sin gastar llamadas a Qdrant/backend/LLM. Devuelve un mensaje en el idioma detectado y marca `fuera_de_dominio=True` (que el servicio traduce a HTTP 422 `CONSULTA_FUERA_DE_DOMINIO`).

### clarification_detector (`app/agent/nodes/clarification.py:209`) — HITL
Detecta ambigüedad. Primero evalúa **señales determinísticas sin LLM** (`_evaluar_señales_deterministicas`): múltiples servicios mencionados, cluster inter-municipal sin municipio, consulta muy corta sin filtros. Si no hay señal, y solo si la consulta lo merece (`_merece_evaluacion_llm`), evalúa con LLM light. Si decide que necesita clarificación, **pausa el grafo con `interrupt()`** (ver [§10](#10-hitl-pausas-de-clarificacin-con-el-gestor)).

### query_classifier (`app/agent/nodes/classifier.py:26`)
Decide **simple** (una fuente) vs **compuesta** (dos o más fuentes a combinar). Usa el modelo **primary** (`openai/gpt-oss-120b`) con structured output (`QueryClassification`). Determina además `merge_strategy`: `join` (combinar métricas por zona/cluster) o `relacional` (analizar correlación). Tiene un fallback manual robusto si el modelo omite `merge_strategy`.

### task_decomposer (`app/agent/nodes/decomposer.py:23`)
Solo para compuestas. Descompone la consulta en sub-tareas (`SubTaskDefinition`: `sub_agent_id`, `endpoint`, `params`, `descripcion`). Usa el modelo primary. Si falla, revierte a `query_type="simple"` y sigue el flujo simple.

### parallel_executor (`app/agent/nodes/executor.py:11`)
Ejecuta todas las sub-tareas **en paralelo** con `asyncio.gather` (con `return_exceptions=True` para que un fallo no cancele el resto). Cada sub-tarea la ejecuta `run_sub_agent` (`app/agent/sub_agent.py`), que valida el endpoint/params contra la allowlist de seguridad y llama al endpoint del backend normalizando el resultado a `list[dict]`. Deduplica las fuentes.

### result_merger (`app/agent/nodes/executor.py:65`)
Combina los resultados de los sub-agentes según `merge_strategy`:
- **join**: `_merge_join()` en Python puro (`app/agent/merge.py`) por `join_key` (default `cluster`). A tiene prioridad sobre B en campos con el mismo nombre.
- **relacional**: pasa ambos datasets por separado al formatter con metadata (`tool_results_meta.datasets`) para que el LLM analice la correlación.
- Fallback: usa el primer resultado disponible.

### schema_linker (`app/agent/schema_linker.py`)
Decide **cómo** obtener los datos: llamar a un endpoint del backend o generar Text-to-SQL. Primero intenta reglas determinísticas sobre el plan; si no hay señal clara, usa embeddings en Qdrant. Devuelve `schema_decision`. Detalle completo en [§8](#8-schema-linking-cmo-se-decide-de-dnde-sacar-los-datos).

### tool_caller (`app/agent/nodes/tool_caller.py:27`)
Ejecuta la decisión del schema_linker:
- `tipo == "endpoint"` -> `llamar_endpoint()` (HTTP GET al backend).
- `tipo == "sql"` -> `ejecutar_sql()` (genera SQL con el modelo primary y lo ejecuta contra MySQL).

Normaliza el resultado a `list[dict]` (contrato de estado) y guarda las fuentes.

### react_reasoner (`app/agent/nodes/tool_caller.py:136`) — ReAct loop
Si el tool call devolvió datos vacíos (y hay retries y es simple), razona con el modelo primary por qué falló y propone un ajuste (`nuevo_endpoint` / `nuevos_params`). `_aplicar_correccion_react` actualiza `schema_decision` y `tool_caller` re-intenta. El ajuste valida el endpoint contra la allowlist de seguridad antes de aplicarse. Su propio contador (`react_retry_count`) no interfiere con el presupuesto del reflector.

### output_guardrail (`app/agent/guardrails.py`)
Determinístico. Registra advertencias en `tool_results_meta` (datos vacíos, tool_error, `/brechas` sin `severidad_brecha`, sub-agentes con error) y calcula `datos_validos`. **Detecta fugas de información sensible en la respuesta** (`_detectar_fuga_respuesta`: credenciales/API keys, markup de exfiltración, URLs externas, base64) y reemplaza la respuesta por una genérica (ver [§13](#13-seguridad-defensa-contra-prompt-injection)).

### formatter (`app/agent/nodes/formatter.py:47`)
Genera la respuesta final en lenguaje natural. Usa el modelo **light** con structured output (`FormatterOutput`: `respuesta_ia` + `visualizacion_sugerida`). Antes de llamar al LLM:
1. Filtra campos técnicos internos (`_limpiar_para_formatter`).
2. Resume datasets grandes por **estimación de tokens** (`resumir_para_formatter`, `app/agent/resumir.py`) para no exceder el TPM del modelo.
3. Construye un contexto enriquecido (`_construir_contexto_formatter`) con tipo de datos detectado, merge, total de registros y feedback de reflexión previo. Los datos de las tools se envuelven como `<datos_herramientas>` (tratar como DATOS, no instrucciones).

Luego corrige la visualización con un mapa determinístico endpoint -> visualización (`_corregir_visualizacion`, `app/agent/nodes/formatter.py:28`): `/brechas`->`mapa_brechas`, `/mapa*`->`mapa_indicadores`, `/indicadores/evolucion`->`grafico_barras`, `/programas`->`tabla_datos`.

### reflector (`app/agent/nodes/reflector.py:39`) — Reflexión
Evalúa la calidad de la respuesta con el modelo primary. Para no gastar llamadas de más, `_gate_reflexion` (`app/agent/nodes/reflector.py:21`) solo invoca el LLM si hay señales determinísticas de respuesta pobre (datos vacíos, tool_error, respuesta < 80 chars, o ya hubo un retry). Si `quality_score < 0.6` y `reflection_retry_count < reflector_max_retries` (1), vuelve al formatter con `feedback_al_formatter` explícito.

---

## 6. Estado compartido (AgentState)

Definido en `app/agent/state.py` como `TypedDict`. Campos principales:

| Campo | Tipo | Quién lo escribe | Uso |
|---|---|---|---|
| `consulta` | str | inicial / guardrail | Texto sanitizado |
| `idioma` | str | AIService | es/pt/en |
| `request_id` | str | AIService | Trazabilidad en logs |
| `plan` | dict | planner (+clarification en HITL) | Filtros extraídos |
| `query_type` | str | query_classifier | `simple` / `compuesta` |
| `schema_decision` | dict | schema_linker / react_reasoner | Endpoint o SQL + params |
| `task_decomposition` | list | task_decomposer | Sub-tareas |
| `sub_agent_results` | list | parallel_executor | Resultados por sub-agente |
| `merged_results` | list | result_merger | Resultado del merge |
| `tool_results` | list | tool_caller | Siempre `list[dict]` (contrato) |
| `tool_results_meta` | dict | output_guardrail / result_merger | Advertencias y metadata |
| `merge_strategy` / `join_key` | str | classifier/decomposer | Join vs relacional |
| `respuesta_ia` | str | formatter | Respuesta final |
| `visualizacion_sugerida` | str | formatter | `mapa_brechas`, `mapa_indicadores`, `tabla_datos`, `grafico_barras` |
| `fuentes` | list | tool_caller / parallel_executor | Fuentes citadas |
| `fuera_de_dominio` | bool | planner/guardrail | Corta el flujo |
| `react_retry_count` / `reflection_retry_count` | int | loops | Presupuestos de reintento |
| `reflection_score` / `reflection_feedback` | float/str | reflector | Calidad y feedback |
| HITL (`session_id`, `necesita_clarificacion`, `pregunta_clarificacion`, `opciones_clarificacion`, `respuesta_gestor`, `hitl_activado`) | varios | clarification_detector | Pausa y reanudación |

**Contrato importante**: `tool_results` siempre debe ser `list[dict]`. Hay getters seguros (`get_tool_results`, `get_plan`, `get_schema_decision`, etc.) que garantizan tipos válidos, para que ningún nodo tenga que repetir `.get()` con defaults incorrectos.

---

## 7. Capa de LLMs: modelos, rotación y fallback

Todo está en `app/core/config.py` y `app/agent/llm_layer.py`.

### Modelos (migrados en ago-2026 por deprecación de `llama-3.x`)

| Tier | Modelo | Nodos que lo usan |
|---|---|---|
| **Light** | `groq/compound-mini` | planner, formatter, clarification_detector |
| **Primary** | `openai/gpt-oss-120b` | query_classifier, task_decomposer, react_reasoner, reflector, Text-to-SQL |
| **Fallback** | `gemini-3.1-flash-lite` | cualquier nodo ante rate-limit de Groq |

Notas operativas:
- `groq/compound-mini` es un **modelo compuesto**: los prompts largos enrutan a `llama-3.3-70b-versatile`, que tiene su **propia cuota diaria** (100K tok/día para tráfico compound). Al agotarse, el sistema cae al fallback Gemini de forma transparente.
- `openai/gpt-oss-120b` es un **modelo de razonamiento**: genera un `reasoning` interno y la respuesta final en `content`.
- Embeddings: `gemini-embedding-001` (Google).

### Rotación de cuentas Groq

`settings.claves_groq()` (`config.py:93`) arma un **pool de claves** a partir de `GROQ_API_KEY_PRIMARY` + `GROQ_API_KEY_LIGHT` + `GROQ_API_KEY_EXTRA` + `GROQ_API_KEYS_ROTACION` (JSON array), con deduplicación. Cada clave es una cuenta con su propia cuota diaria de TPM/TPD.

En runtime (`_construir_chain`, `app/agent/llm_layer.py:27`) se crea **una instancia `ChatOpenAI` por cuenta del pool** (mismo modelo, key distinta, `max_retries=0`). `_llm_ainvoke_con_fallback` (`app/agent/llm_layer.py:94`) recorre el pool ante un 429; si todas agotan, usa el fallback Gemini (pool de límites separado). Este mismo pool lo reutiliza DSPy offline con `_RotatingLM` (`app/agent/dspy_config.py:24`).

**¿Por qué `max_retries=0`?** El cliente openai reintenta internamente con backoff que puede llegar a 54s en un 429, comiéndose el timeout global. Con 0, el `RateLimitError` propaga a la rotación de cuentas y luego al decorador `@llm_retry`.

### Retries (tenacity)

`app/agent/retry.py`:
- `@llm_retry`: reintenta errores transitorios de API (`RateLimitError`, `APITimeoutError`, `APIConnectionError`, `InternalServerError`) con espera exponencial 1-8s. **No** reintenta errores determinísticos (Pydantic, programación).
- `@http_retry`: reintenta errores de red/5xx del backend (httpx), 1-4s.

### Gestión de errores del servicio (`app/services/ai_service.py`)

- **504 TIMEOUT**: el grafo superó `agent_timeout_simple` (30s) o `agent_timeout_compuesta` (60s).
- **503 IA_SATURADA**: `RateLimitError` tras agotar retries, o `APIStatusError` (ej. 413 request demasiado grande para el TPM).
- **422 CONSULTA_FUERA_DE_DOMINIO**: consulta fuera del dominio.
- **500 ERROR_INTERNO**: excepción inesperada.
- **404 SESION_NO_ENCONTRADA**: al reanudar una sesión HITL expirada.

---

## 8. Schema Linking: cómo se decide de dónde sacar los datos

Archivo: `app/agent/schema_linker.py`. Este nodo decide si `tool_caller` llama a un endpoint del backend o genera Text-to-SQL, **sin gastar tokens en esa decisión** cuando es posible.

### Paso 1 — Routing determinístico (`_route_por_plan`)

Reglas basadas en lo que el planner ya extrajo + palabras clave de la consulta. Se ejecutan **antes** del embedding search porque son más confiables. Orden de evaluación (importa):

1. **Señal de brecha** (`brecha`, `falta`, `no hay`, `carenc`, `sin cobertura`, `sin oferta`...) -> `/brechas`.
2. **"programa"** sin señal de brecha -> `/programas` (catálogo).
3. **Evolución temporal + indicador** (`evolución`, `tendencia`, `histórico`, `cambió`, `bajó`...) -> `/indicadores/evolucion`. Se evalúa **antes** de las reglas de indicador/servicio que lo sombreaban con `/mapa/indicadores`.
4. **Indicador específico extraído** -> `/mapa/indicadores`.
5. **Servicio con indicador social** (`EMPLEO`, `SALUD_MENTAL`, `EDUCACION`) -> `/mapa/indicadores`.
6. **Red pura sin servicio** (`conectividad`, `señal`, `antena`, `cobertura`, `5g`...) -> `/mapa`.

Cada regla devuelve `score: 1.0` (confianza determinística, no viene de Qdrant).

### Paso 2 — Fallback a embeddings (Qdrant)

Si no hay señal determinística, se enriquece la consulta con el servicio/indicador del plan (`consulta | servicio: X | indicador: Y`) y se busca similitud semántica en Qdrant (`app/vectorstore/searcher.py::search`). Primero `tipo="endpoint"`, y si no supera el umbral, `tipo="sql"`.

### Umbral (`SCHEMA_LINKER_THRESHOLD`, default 0.68)

Si el score del mejor match queda bajo el umbral, se descarta y se usa el siguiente (SQL). Se calibró con `scripts/optimize_threshold.py` sobre un dataset OOD (parafraseado) — el golden resuelve todo por reglas determinísticas, así que el umbral solo afecta consultas nuevas. Calibración actual: **0.68** (elimina un FP sin perder matches correctos).

### Construcción de la decisión

- `_build_endpoint_decision`: mapea el payload de Qdrant + plan a los `params` correctos por endpoint. Valida que el servicio sea una categoría válida para `/mapa/indicadores` (SOLO `SALUD_MENTAL|EMPLEO|EDUCACION`); si no, redirige a `/brechas`. Elimina params `None`.
- `_build_sql_decision`: si el plan tiene servicio con tabla mapeada (`EMPLEO`/`SALUD_MENTAL` -> `indicadores_territoriales`) usa ese schema mínimo; si no, un default genérico (`concentracao`).

---

## 9. Herramientas (tools): endpoints y Text-to-SQL

Archivo: `app/agent/tools.py`.

### `llamar_endpoint` (`tools.py:216`)

Hace HTTP al backend (`BACKEND_URL` + endpoint) con retry `@http_retry`. **Valida el endpoint contra la allowlist de seguridad** (`validar_endpoint`, ver [§13](#13-seguridad-defensa-contra-prompt-injection)) y **filtra los params a las claves permitidas** (`filtrar_params`); un endpoint fuera de la allowlist devuelve `{"resultado": [], "fuentes": [], "error": "endpoint no permitido"}`. Normaliza la respuesta a `list[dict]` (maneja que el backend devuelva un dict anidado en claves `brechas`/`evolucion`/`programas`/`regiones`, o un array top-level como `/programas`). Ante errores HTTP/red persistentes degrada a lista vacía sin romper el pipeline.

### `ejecutar_sql` (`tools.py:267`) — Text-to-SQL

1. Genera SQL con el modelo **primary** (con rotación de cuentas y fallback Gemini) usando `TEXT_TO_SQL_PROMPT` y el **schema mínimo** relevante (no el schema completo -> ~75% menos tokens).
2. **Validaciones de seguridad** (`_sanitizar_sql`, `tools.py:106`, Fase 2 del plan de seguridad):
   - Solo `SELECT` (si no, aborta).
   - Rechaza **multi-statement** (`;` seguido de otra query).
   - Rechaza keywords peligrosas (`UNION`, `INSERT`, `DROP`, `INTO OUTFILE/DUMPFILE`, `LOAD_FILE`, `SLEEP`, `@@`, `INFORMATION_SCHEMA`, `/*`).
   - Solo tablas de la **allowlist** (`_TABLAS_PERMITIDAS`).
   - Garantiza **`LIMIT 50`** (reescribe si el LLM pidió más).
   - Previene **full scans** en tablas grandes (`concentracao`, `mobilidade_agregada`): si la cláusula `WHERE` real no filtra `day_date`, agrega el filtro del día más reciente.
3. Ejecuta contra MySQL con el usuario de **solo lectura** (`DB_READONLY_USER`) vía `aiomysql`. Devuelve filas como `list[dict]` y la fuente `Vísent CDRView v2`.

**Prioridad de datos**: primero endpoints (lógica de negocio del backend), SQL solo como fallback.

---

## 10. HITL: pausas de clarificación con el gestor

El sistema puede **pausar** una consulta y pedir clarificación al gestor antes de responder. Implementado con `interrupt()` de LangGraph (ver `app/agent/nodes/clarification.py:209` y `app/services/ai_service.py:203`).

### Flujo

```
POST /consulta "¿Cómo están la mentoría y la formación en São José?"
  -> clarification_detector detecta 2 servicios -> interrupt(...) pausa
  -> respuesta: { requiere_clarificacion: true, session_id, pregunta, opciones }

El gestor elige (ej. "Mentoría")

POST /consulta/respuesta { session_id, respuesta_gestor: "Mentoría" }
  -> Command(resume=...) reanuda el grafo en la línea del interrupt()
  -> _integrar_respuesta_al_plan() mapea la respuesta a valores canónicos
    (servicio/municipio/periodo) y continúa el flujo normal
```

### Señales determinísticas de ambigüedad (sin LLM)

1. **Múltiples servicios mencionados** en la consulta.
2. **Cluster inter-municipal** (`ESTREITO_CAPOEIRAS`) sin municipio -> pregunta si Florianópolis o São José.
3. **Consulta muy corta sin filtros** (≤ 3 palabras).

### Mecánica

- El estado completo se persiste en el checkpointer entre pausa y reanudación.
- `_integrar_respuesta_al_plan` (`app/agent/nodes/clarification.py:116`) mapea la respuesta del gestor a valores canónicos del dominio. La respuesta es **autoritativa**: sobrescribe lo que el planner infirió.
- **Seguridad (Fase 4.3)**: `ai_service.py` sanitiza la respuesta del gestor antes de reinyectarla al grafo (trunca a 500 chars y elimina caracteres de control), y `_integrar_respuesta_al_plan` **no apenda el texto crudo a `plan["razon"]`** si `_detectar_inyeccion` detecta señales (solo se aplican los valores canónicos). Así, una respuesta del gestor con instrucciones maliciosas no llega a otros prompts.
- **Una sola oportunidad de clarificación por consulta** (MVP). Si la respuesta no desambigua del todo, el agente continúa con lo que pudo inferir.
- Las sesiones expiran a los 15 min (`hitl_session_ttl_seconds`); `main.py` corre un loop de limpieza que elimina sesiones y threads expirados.

---

## 11. Consultas compuestas: sub-agentes paralelos y merge

Para consultas que combinan **dos o más fuentes** de datos:

1. **task_decomposer** divide la consulta en sub-tareas (`/mapa` + `/mapa/indicadores(EDUCACION)`, etc.).
2. **parallel_executor** las ejecuta en paralelo (`asyncio.gather`), cada una un `run_sub_agent`.
3. **result_merger** combina según `merge_strategy`:
   - **join** (`_merge_join`): combina métricas por `join_key` (default `cluster`). Registros de A sin match en B se incluyen con campos de B ausentes. Valida en runtime que el `join_key` exista en ambas fuentes (si no, loguea error y devuelve A sin merge).
   - **relacional**: pasa ambos datasets por separado al formatter con metadata, para que el LLM analice la correlación (ej. "alto desempleo y baja conectividad").

Las compuestas no usan el loop ReAct (el manejo de errores está en `parallel_executor`). El timeout global es mayor (60s) porque una consulta relacional hace ~5 llamadas LLM.

---

## 12. Patrones de robustez: ReAct loop y Reflexión

Dos patrones con presupuestos de reintento **independientes** (contadores separados en el estado):

### ReAct (solo consultas simples)

```
tool_caller -> (datos vacíos?) -> react_reasoner -> tool_caller -> ... -> output_guardrail
                loop hasta max_retries_llm (2)
```

El `react_reasoner` razona por qué el tool call devolvió vacío y propone un ajuste (otro endpoint o params corregidos). El ajuste se aplica de forma determinística (`_aplicar_correccion_react`), se limpian params `None`, y `tool_caller` re-intenta.

### Reflexión

```
formatter -> reflector -> (score < 0.6 y hay retries?) -> formatter con feedback -> reflector -> END
                             loop hasta reflector_max_retries (1)
```

El gate `_gate_reflexion` evita invocar el LLM reflector en consultas que aparentan estar bien (ahorra costo del 70B). El feedback del reflector se inyecta al formatter en la siguiente iteración.

---

## 13. Seguridad: defensa contra prompt injection

El servicio expone un agente LLM con herramientas (HTTP + Text-to-SQL), por lo que es un objetivo de **prompt injection** (LLM01 del OWASP LLM Top 10 2025). La defensa sigue el principio de OWASP de **no confiar en el filtrado de input como única barrera**: es **defensa en profundidad**, 100% determinística (sin guardrail de modelo tipo Llama Guard). Está implementada en 7 fases:

### 13.1 Allowlist de endpoints y params (Fase 1) — `app/agent/security.py`

El agente solo puede llamar a los endpoints del backend incluidos en `ENDPOINTS_PERMITIDOS`: `/brechas`, `/mapa`, `/mapa/indicadores`, `/indicadores/evolucion`, `/programas`. Cada endpoint tiene sus params permitidos (`PARAMS_PERMITIDOS_POR_ENDPOINT`). Se aplica en tres puntos:
- `tools.py:llamar_endpoint` — un endpoint fuera de la allowlist devuelve resultado vacío con error.
- `sub_agent.py:run_sub_agent` — valida antes de llamar (consultas compuestas).
- `nodes/tool_caller.py:_aplicar_correccion_react` — el ajuste propuesto por el ReAct loop debe pasar la allowlist.

### 13.2 Hardening del Text-to-SQL (Fase 2) — `tools.py:_sanitizar_sql`

Todo SQL generado por el LLM pasa validación antes de ejecutarse: solo `SELECT`, sin multi-statement, sin keywords peligrosas, solo tablas de la allowlist, `LIMIT 50` forzado, y filtro de día más reciente para evitar full scans en tablas grandes (ver [§9](#9-herramientas-tools-endpoints-y-text-to-sql)).

### 13.3 Separación estructural instrucciones/datos (Fase 3) — `app/agent/security.py`

Todos los prompts incluyen un **preludio de jerarquía de instrucciones** (`_PRELUDE_SEGURIDAD`) que ordena al modelo tratar el contenido delimitado como DATOS, nunca como instrucciones. La consulta del usuario viaja entre `<consulta_usuario>...</consulta_usuario>` (`envolver_consulta`) y los datos de las tools entre `<datos_herramientas>...</datos_herramientas>` (`envolver_datos`). Esto evita que texto inyectado en datos o en la consulta se interprete como orden.

### 13.4 Sanitización y detección en el input (Fase 4) — `app/agent/guardrails.py`

- `input_guardrail` corre `_detectar_inyeccion` sobre la consulta: regex de patrones clásicos ("ignora las instrucciones", "developer mode", "system prompt", "override", etc.), base64 largo (instrucciones ofuscadas) y **typoglycemia fuzzy** ("ignroe" ~ "ignore"). Ante detección corta el flujo con `flag_inyeccion` y una respuesta genérica de seguridad.
- `ai_service.py:resume_query` sanitiza la **respuesta del gestor** (canal HITL) antes de reinyectarla: trunca a 500 chars y elimina caracteres de control. Además, `_integrar_respuesta_al_plan` no apenda texto crudo a `plan["razon"]` si detecta inyección (ver [§10](#10-hitl-pausas-de-clarificacin-con-el-gestor)).

### 13.5 Validación de output zero-trust (Fase 5) — `app/agent/guardrails.py`

`output_guardrail` corre `_detectar_fuga_respuesta` sobre la respuesta generada: credenciales/API keys (`api_key`, `secret`, `password`, `sk-`, `AIza`, `gsk_`), markup de exfiltración (`<img src=http...>`, imágenes markdown), URLs externas largas y bloques base64. Ante fuga, **reemplaza la respuesta por una genérica** — nunca se entrega contenido con credenciales o exfiltración.

### 13.6 Auth, rate limit y logs (Fase 6) — `app/middlewares/security_middleware.py`

- **Auth**: `POST /consulta` y `POST /consulta/respuesta` requieren el header `X-API-Key` con el valor de `API_AUTH_TOKEN` (comparación en tiempo constante). Si la variable está vacía, la auth queda deshabilitada (compatibilidad con dev local). El backend Spring Boot envía el header vía `ai.service.api-token` (ver `back/src/main/java/.../config/Config.java`).
- **Rate limit**: ventana deslizante en memoria por IP (default 30 req/60s) que devuelve `429` con `Retry-After`. Las peticiones autenticadas con la key válida se **eximen** (todo el tráfico del backend llega como una sola IP; el backend es quien limita por usuario).
- **Logs redactados**: `ai_service.py` no loguea el texto de `request.consulta` (solo `request_id`). `/health` no expone `backend_url`.

### 13.7 Tests de seguridad (Fase 7) — `tests/test_security.py`

42 tests con payloads del OWASP LLM Prompt Injection Cheat Sheet + casos del sistema: inyección en `_detectar_inyeccion`/`input_guardrail`, bypass SQL (UNION, `;DROP`, LIMIT excesivo, INTO OUTFILE, full-scan con `WHERE 1=1`), endpoints no permitidos desde sub_agent/react_reasoner, respuesta del gestor con instrucciones que no llega a `plan["razon"]`, datos de tools con instrucciones que el formatter trata como dato, y auth/rate-limit del middleware.

> **Nota**: el `normalizer.py` deliberadamente **no** endurece los valores no canónicos (municipio/cluster/indicador siguen como texto libre) — decisión de producto. La defensa contra inyección no depende de ello.

---

## 14. DSPy: optimización offline de prompts (inactiva por defecto)

El proyecto evaluó **DSPy + MIPROv2** para optimizar los prompts de los nodos. Conclusión (ago-2026, ver `plan.md`): **sin mejora** — el golden ya da 100% con los prompts artesanales, así que no hay headroom. El pipeline queda documentado y reproducible pero **no está activo en producción**.

Estado actual:
- `settings.dspy_compiled = False` (default). El nodo planner usa el módulo DSPy compilado **solo si** el flag está en True **y** existe `compiled_modules/planner.json`.
- El archivo `planner.json` **fue borrado** tras los evals de aceptación (regresión en golden: 97.86% vs 100%). `compiled_modules/` está vacío.
- La integración está codificada en `app/agent/nodes/planner.py` (`_plan_via_dspy`, `_plan_desde_prediccion`, `_run_dspy_async`) pero es **inerte** sin el flag + archivo.
- El fallback Groq->Gemini queda intacto: cualquier error del módulo DSPy cae a la infra actual.

Archivos:
- `app/agent/dspy_config.py`: LMs de DSPy (`_RotatingLM` con pool de claves Groq, y `get_gemini_lm` gratis para compilar sin gastar cuota).
- `app/agent/dspy_modules.py`: módulos baseline (PlannerModule, QueryClassifierModule, ClarificationDetectorModule) y `load_compiled_module` / `init_modules`.
- `dspy_optimize/compile.py`: script offline de compilación MIPROv2.
- `dspy_optimize/dataset.py`: datasets DSPy desde el golden + dataset OOD anotado del planner.
- `dspy_optimize/metrics.py`: métricas por nodo.
- `dspy_optimize/inspect_compiled.py`: inspecciona instrucciones/demos que MIPROv2 encontró.

Para habilitar en el futuro: compilar con `compile.py`, correr los evals de aceptación (`run_evals.py --use-compiled`) y solo activar si no regresan el golden ni el OOD.

---

## 15. Vectorstore (Qdrant)

Archivos: `app/vectorstore/{documents,indexer,searcher}.py`.

- **`documents.py`**: los 9 documentos indexados (5 endpoints + 4 tablas). Cada texto está redactado para capturar la **intención** de las consultas que resuelve, no solo el nombre técnico. Ej: `ep_indicadores_evolucion` describe "cómo viene cambiando un indicador en el tiempo".
- **`indexer.py`**: al arrancar, embebe los documentos con `gemini-embedding-001` y los sube a la colección `appbit`. Usa un **hash de invalidación** (contenido + modelo de embedding + task_type): si cambió cualquiera, re-indexa. Solo se indexan **descripciones** (9 textos cortos), no filas -> índice liviano y barato.
- **`searcher.py`**: dado el query, lo embebe y hace una búsqueda de similitud coseno en Qdrant, restringida por `tipo` (`endpoint` | `sql`), excluyendo el punto meta. Aplica el umbral `schema_linker_threshold` y devuelve el payload del mejor match o `None`.

---

## 16. Pipeline ETL

El pipeline ETL carga los CSVs de `ai/data/` a MySQL **automáticamente al arrancar el servicio** (hilo en background, `main.py:97`). Idempotente: salta tablas que ya tienen datos.

**Orden de carga** (`app/etl/pipeline.py`): `antenas` -> `assinantes` -> `mobilidade_agregada` -> `concentracao` (depende de mobilidade) -> `flujo_od` -> `fluxo_vias`. Si `mobilidade_agregada` falla, salta `concentracao` (dependencia).

**Carga** (`app/etl/loaders_fast.py`): usa `LOAD DATA LOCAL INFILE` para tablas chicas y carga por chunks (100K filas) para `tensor_mobilidade.csv` (~2.7GB). Aplica transformaciones: `download_bytes`->`download_gb`, renames de columnas (`periodo_sessao`->`periodo`, etc.), y ajustes de sesión para acelerar (`foreign_key_checks=0`).

**Pre-requisito**: las tablas las crea el backend (se espera que existan con `wait_for_tables`). Los CSVs saneados se descargan del Drive referenciado en la sección de dataset; `tensor_od.csv` sin sanear necesita `scripts/corregir_tensor_od.py`.

**Endpoints de estado**: `GET /health` y `GET /etl/status` reportan `running/completed/error`.

---

## 17. Evaluaciones

Archivos en `evals/` y `app/../`:

- **`evals/golden_dataset.json`**: **35 consultas** en 8+ categorías (brechas de servicio, indicador simple, red pura, programas, compuestas, evolución temporal, fuera de dominio, ambiguas, y 5 casos HITL). Cada una con `expected` por nodo (plan.servicio, plan.municipio, query_type, schema_decision.endpoint, tool_results_not_empty, visualizacion_sugerida, etc.).
- **`evals/run_evals.py`**: runner que ejecuta el golden contra el agente real. Características:
  - Secuencial con **cooldown entre consultas** (default 45s) para respetar el TPM free-tier de Groq; reintentos a nivel eval con backoff.
  - Timeout por consulta (90s) para no colgar el run.
  - Guardado incremental `.partial` con **reanudación**.
  - Reporte por consulta, categoría y nodo (PLANNER, QUERY_CLASSIFIER, SCHEMA_LINKER, FORMATTER, TOOL_CALLER, REFLECTOR, END_TO_END).
  - Compara municipios normalizando acentos/case.
  - `--use-compiled` para probar módulos DSPy compilados (deshabilitado por defecto).

```bash
cd ai
PYTHONUNBUFFERED=1 python evals/run_evals.py --json evals/reporte_full.json
```

- **`evals/ood_dataset.json`** (14 consultas parafraseadas para ejercitar embeddings, usadas para calibrar el threshold) y **`evals/ood_planner_dataset.json`** (20 consultas anotadas para el planner, usadas como devset de DSPy).
- Resultado de referencia (light `groq/compound-mini`): **100% (35/35)**, score 1.0, 0 rate-limits, latencia p50 4.55s (`evals/reporte_compoundmini.json`).

---

## 18. Tests

193 tests con pytest en `tests/`. El `conftest.py` de la raíz provee una fixture `test_agent` con un **checkpointer aislado** por test (no contamina el de producción). Temas cubiertos:

| Archivo | Qué valida |
|---|---|
| `test_routing.py` | Routing del grafo (simple/compuesta/FOD) |
| `test_normalizer.py` | Corrección determinística del plan |
| `test_guardrails.py` | input/output guardrails |
| `test_security.py` | Defensa anti prompt injection (Fases 1-7): allowlists, SQL, inyección, fugas, auth/rate-limit |
| `test_extraer_json.py` | Parseo JSON con fallback |
| `test_llm_fallback.py` | Rotación de cuentas / fallback Gemini |
| `test_merge_join.py` | `_merge_join` |
| `test_resumir.py` | Resumen para el formatter |
| `test_sub_agent.py` | Sub-agentes |
| `test_context.py` | Contexto del formatter |
| `test_clarification_detector.py` | Señales determinísticas de clarificación |

```bash
cd ai
python -m pytest tests/ -q
```

---

## 19. Configuración y variables de entorno

Config centralizada en `app/core/config.py` (pydantic-settings, lee `ai/.env`). Las variables principales:

### LLMs y APIs
| Variable | Descripción | Default |
|---|---|---|
| `GROQ_BASE_URL` | URL de la API de Groq | `https://api.groq.com/openai/v1` |
| `GROQ_API_KEY_PRIMARY` | Cuenta Groq para `openai/gpt-oss-120b` | - |
| `GROQ_API_KEY_LIGHT` | Cuenta Groq para `groq/compound-mini` | - |
| `GROQ_API_KEY_EXTRA` | Cuenta Groq adicional (rotación) | - |
| `GROQ_API_KEYS_ROTACION` | Pool JSON de cuentas Groq extra (cada una suma su cuota diaria) | `[]` |
| `GROQ_MODEL_PRIMARY` | Modelo primary | `openai/gpt-oss-120b` |
| `GROQ_MODEL_LIGHT` | Modelo light | `groq/compound-mini` |
| `GOOGLE_API_KEY` | Google (embeddings + fallback LLM) | - |
| `GEMINI_EMBEDDING_MODEL` | Modelo de embeddings | `gemini-embedding-001` |
| `GEMINI_MODEL_FALLBACK` | LLM de respaldo | `gemini-3.1-flash-lite` |

### Infraestructura
| Variable | Descripción | Default |
|---|---|---|
| `BACKEND_URL` | URL del backend Spring Boot | `http://backend:8080/api` |
| `QDRANT_URL` | URL de Qdrant | `http://qdrant:6333` |
| `QDRANT_COLLECTION` | Colección en Qdrant | `appbit` |
| `QDRANT_API_KEY` | API key de Qdrant (opcional) | - |
| `DB_*` | Credenciales MySQL del ETL | root/root en `db` |
| `DB_READONLY_*` | Usuario de solo lectura para Text-to-SQL | `ai_readonly` |

### Comportamiento del agente
| Variable | Descripción | Default |
|---|---|---|
| `SCHEMA_LINKER_THRESHOLD` | Umbral de similitud del schema linker | `0.68` |
| `MAX_RETRIES_LLM` | Reintentos de llamadas LLM (ReAct) | `2` |
| `MAX_RETRIES_TOOL` | Reintentos de HTTP al backend | `2` |
| `AGENT_RECURSION_LIMIT` | Límite de nodos del grafo | `25` |
| `AGENT_TIMEOUT_SIMPLE` | Timeout de consultas simples | `30.0` |
| `AGENT_TIMEOUT_COMPUESTA` | Timeout de consultas compuestas | `60.0` |
| `FORMATTER_MAX_RECORDS` | Registros máximos en el contexto del formatter | `8` |
| `FORMATTER_MAX_TOKENS_ESTIMATE` | Estimación de tokens para resumir | `3000` |
| `REFLECTOR_MIN_QUALITY_SCORE` | Umbral de calidad del reflector | `0.6` |
| `REFLECTOR_MAX_RETRIES` | Reintentos del reflector | `1` |
| `HITL_SESSION_TTL_SECONDS` | TTL de sesiones HITL | `900` (15 min) |
| `HITL_CLEANUP_INTERVAL_SECONDS` | Intervalo de limpieza HITL | `60` |
| `LANGSMITH_*` | Tracing de LangSmith (opcional) | desactivado |
| `DSPY_COMPILED` | Habilita módulo DSPy compilado | `false` |

### Seguridad (Fase 6)
| Variable | Descripción | Default |
|---|---|---|
| `API_AUTH_TOKEN` | API key compartida con el backend; si está vacía la auth de `/consulta` queda deshabilitada. El backend la envía como header `X-API-Key` (via `AI_SERVICE_API_TOKEN` del `.env` raíz) | vacío |
| `RATE_LIMIT_MAX_REQUESTS` | Máximo de requests por IP en la ventana | `30` |
| `RATE_LIMIT_WINDOW_SECONDS` | Ventana del rate limit (segundos) | `60` |

### Ejecutar en Docker

```bash
cd ai && cp .env.example .env   # completar credenciales
cd /home/<usuario>/S06-26-NC-EQUIPO--72   # raíz del repo
cp .env.example .env            # elegir perfil dev / dev-mock-csv
docker compose up --build       # AI Service en http://localhost:8000
```

**Nota**: el contenedor AI lee `ai/.env` vía `env_file` en `docker-compose.yml`; los cambios de variables de entorno requieren recrear el contenedor (`docker compose up -d --force-recreate ai`). El `mem_limit` del AI Service es 1600M (necesario para evals con DSPy; el OOM killer mataba el proceso con 900M).

---

## 20. Endpoints de la API

Definidos en `app/api/routes.py` y `app/models/schemas.py`.

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/consulta` | Envía una consulta al agente (`{consulta, filtros?, idioma?}`) -> `ConsultaResponse` o 422 (fuera de dominio) / 401 (sin API key) / 429 (rate limit) / 503 / 504 |
| `POST` | `/consulta/respuesta` | Reanuda una consulta pausada (`{session_id, respuesta_gestor}`) — misma auth/rate limit |
| `GET` | `/health` | Estado del servicio + ETL |
| `GET` | `/etl/status` | Estado del pipeline ETL |

**Auth y rate limit (Fase 6)**: si `API_AUTH_TOKEN` está configurado, los `POST` a `/consulta` y `/consulta/respuesta` exigen el header `X-API-Key: <token>`; sin él responden `401 {"error":"NO_AUTORIZADO"}`. El rate limit por IP (default 30 req/60s) responde `429` con `Retry-After`; las peticiones con key válida se eximen (ver [§13.6](#136-auth-rate-limit-y-logs-fase-6)).

**`ConsultaResponse`** (`schemas.py:11`):
```json
{
  "respuesta_ia": "texto...",
  "datos": [ { "cluster": "...", "severidad_brecha": "ALTA", ... } ],
  "fuentes": [ { "nombre": "...", "endpoint": "..." } ],
  "visualizacion_sugerida": "mapa_brechas",
  "idioma": "es",
  "session_id": null,               // HITL
  "requiere_clarificacion": false,  // HITL
  "pregunta_clarificacion": null,   // HITL
  "opciones_clarificacion": null    // HITL
}
```

Swagger UI: `http://localhost:8000/docs` · Redoc: `/redoc` · OpenAPI: `/openapi.json`.

---

## 21. Scripts útiles

| Script | Función |
|---|---|
| `scripts/corregir_tensor_od.py` | Corrige valores nulos de `tensor_od.csv` (usa `antenas_flp.csv`; backup del original) |
| `scripts/check_csv.py` | Muestra columnas y filas de cada CSV en `data/` |
| `scripts/analisis_preguntas_clave.py` | Análisis de datos para las 3 preguntas clave del desafío |
| `scripts/optimize_threshold.py` | Calibra `schema_linker_threshold` (curva PR sobre golden u OOD) -> `evals/threshold_analysis.json` |
| `dspy_optimize/compile.py` | Compilación MIPROv2 offline de módulos DSPy |
| `dspy_optimize/inspect_compiled.py` | Inspecciona módulos DSPy compilados |

---

## 22. Documentación relacionada

- [Análisis del dataset](README_DATASET.md) — entendimiento de los datos y las preguntas clave.
- [Arquitectura de integración de IA](../docs/ARQUITECTURA_AI.md) — integración end-to-end con el backend/frontend.
- [Contratos de la API](../docs/API_CONTRATOS.md) — contratos de los endpoints del backend.
- [Esquema de la BD](../docs/SCHEMA.md) — esquema MySQL.
- [Referencia técnica CDRView](../docs/CDRView_AppBiT_TechnicalReference_v2_es.md) — contexto de los datos de Vísent.
- [plan.md](plan.md) — plan de trabajo DSPy y plan de seguridad anti prompt injection (historial de decisiones del proyecto).
