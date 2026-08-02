import logging
import json
from app.agent.state import AgentState, get_plan
from app.vectorstore.searcher import search

logger = logging.getLogger(__name__)

_SERVICIO_TABLA_FALLBACK = {
    "EMPLEO": {
        "tablas": ["indicadores_territoriales"],
        "schema_minimo": (
            "indicadores_territoriales(municipio VARCHAR, cluster VARCHAR, "
            "categoria VARCHAR, indicador VARCHAR, valor DECIMAL, "
            "unidad VARCHAR, fonte VARCHAR, fecha_referencia DATE)"
        ),
    },
    "SALUD_MENTAL": {
        "tablas": ["indicadores_territoriales"],
        "schema_minimo": (
            "indicadores_territoriales(municipio VARCHAR, cluster VARCHAR, "
            "categoria VARCHAR, indicador VARCHAR, valor DECIMAL, "
            "unidad VARCHAR, fonte VARCHAR, fecha_referencia DATE)"
        ),
    },
    # FORMACION, MENTORIA, EXPERIENCIA no tienen tabla propia todavía,
    # así que ahí sí seguirías cayendo a un default razonable o a error explícito
}

_PALABRAS_BRECHA = (
    "brecha", "falta", "no hay", "carenc", "desaten",
    "sin programa", "sin cobertura", "sin oferta", "no tienen",
)

_PALABRAS_RED = (
    "conectividad", "red", "señal", "antena", "cobertura",
    "congestión", "congestionamento", "usuarios", "tráfico",
    "descarga", "tecnología", "5g", "4g", "3g", "lte", "nr",
    "wcdma", "hotspot", "densidad", "mapa",
)

_PALABRAS_EVOLUCION = (
    "evolución", "evolucion", "tendencia", "histórico", "historico",
    "tiempo", "meses", "años", "creció", "bajó", "cambió", "progreso",
)

# Categorías válidas para /mapa/indicadores. FORMACION/MENTORIA/EXPERIENCIA
# son servicios válidos en /brechas pero NO como categoria aquí (Fix Bug E).
_CATEGORIAS_VALIDAS_MAPA = {"SALUD_MENTAL", "EMPLEO", "EDUCACION"}


def _route_por_plan(plan: dict, consulta_lower: str) -> dict | None:
    """
    Reglas determinísticas basadas en lo que el planner ya extrajo.
    Se ejecutan ANTES del embedding search porque son más confiables
    que la similitud semántica del texto libre (que se puede confundir
    con palabras sueltas como "conectividad" en una consulta de empleo).
    Devuelve None si el plan no da señal suficiente -> cae a vector search.
    """
    es_consulta_de_brecha = any(p in consulta_lower for p in _PALABRAS_BRECHA)

    # 1. Señal de brecha explícita siempre gana -> /brechas
    if es_consulta_de_brecha:
        return {
            "id": "ep_brechas",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/brechas",
            "score": 1.0,  # confianza determinística, no viene de Qdrant
        }

    # 2. Catálogo de programas: la palabra "programa" sin señal de brecha
    #    pide el catálogo (¿qué programas hay?), no las brechas. Las brechas
    #    ("faltan programas", "no tienen programas") ya las capturó la regla 1.
    if "programa" in consulta_lower:
        return {
            "id": "ep_programas",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/programas",
            "score": 1.0,
        }

    # 3. Evolución temporal con indicador -> /indicadores/evolucion.
    #    se evalúa ANTES de las reglas de indicador/servicio, que
    #    antes la sombreaban con /mapa/indicadores. "¿Cómo evolucionó la tasa
    #    de desempleo?" pide la serie temporal, no el valor actual.
    es_evolucion = any(p in consulta_lower for p in _PALABRAS_EVOLUCION)
    if es_evolucion and plan.get("indicador"):
        return {
            "id": "ep_indicadores_evolucion",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/indicadores/evolucion",
            "score": 1.0,
        }

    # 4. Si el planner ya identificó un indicador específico, siempre es /mapa/indicadores.
    #    No importa si la consulta menciona además "conectividad" o "red" de pasada.
    if plan.get("indicador"):
        return {
            "id": "ep_mapa_indicadores",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/mapa/indicadores",
            "score": 1.0,
        }

    # 5. Si el servicio es uno de los que tienen indicador social (EMPLEO, SALUD_MENTAL)
    #    y no es consulta de brecha, también es /mapa/indicadores.
    if plan.get("servicio") in ("EMPLEO", "SALUD_MENTAL"):
        return {
            "id": "ep_mapa_indicadores",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/mapa/indicadores",
            "score": 1.0,
        }

    # 6. Consultas de red pura sin servicio (Fix Bug D): conectividad,
    #    señal, cobertura, etc. -> /mapa. Evita caer a la tabla SQL genérica
    #    `concentracao` cuando el plan no tiene servicio y el score de
    #    embeddings queda bajo el umbral.
    if any(p in consulta_lower for p in _PALABRAS_RED) and not plan.get("servicio"):
        return {
            "id": "ep_mapa",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/mapa",
            "score": 1.0,
        }

    return None  # sin señal clara -> vector search decide


def _build_endpoint_decision(payload: dict, plan: dict, request_id: str = "-") -> dict:
    """
    Construye los parámetros del endpoint a partir del payload (de Qdrant
    o del router determinístico) y el plan del planner.
    """
    endpoint = payload["endpoint"]
    servicio = plan.get("servicio")
    params: dict = {}

    if endpoint == "/brechas":
        params = {
            "servicio": servicio,
            "municipio": plan.get("municipio"),
            "periodo": plan.get("periodo"),  
            "income_cluster": plan.get("income_cluster"),
        }
    elif endpoint == "/mapa":
        params = {
            "periodo": plan.get("periodo", "TARDE"),
            "municipio": plan.get("municipio"),
            "fecha": plan.get("fecha"),
        }
    elif endpoint == "/mapa/indicadores":
        if servicio not in _CATEGORIAS_VALIDAS_MAPA:
            # FORMACION/MENTORIA/EXPERIENCIA no son categorias válidas
            # para /mapa/indicadores- redirigir a /brechas
            logger.warning(
                "[%s] Servicio '%s' inválido para /mapa/indicadores "
                "— redirigiendo a /brechas", request_id, servicio
            )
            # Sin mutar el payload de entrada- copia con endpoint corregido
            payload = {**payload, "endpoint": "/brechas"}
            return _build_endpoint_decision(payload, plan, request_id)
        params = {
            "categoria": servicio,
            "indicador": plan.get("indicador"),
            "municipio": plan.get("municipio"),
        }
    elif endpoint == "/indicadores/evolucion":
        params = {
            "categoria": servicio,
            "indicador": plan.get("indicador"),
            "municipio": plan.get("municipio"),
        }
    elif endpoint == "/programas":
        params = {
            "tipo": servicio,
            "municipio": plan.get("municipio"),
            "cluster": plan.get("cluster"),
            "activo": True,
        }

    # Elimina params None para no mandarlos en la query
    params = {k: v for k, v in params.items() if v is not None}

    return {
        "tipo": "endpoint",
        "metodo": payload.get("metodo", "GET"),
        "endpoint": endpoint,
        "params": params,
        "score": payload["score"],
    }


def _build_sql_decision(payload: dict | None, plan: dict | None = None) -> dict:
    if payload:
        return {
            "tipo": "sql",
            "tablas": payload.get("tablas", []),
            "schema_minimo": payload.get("schema_minimo", ""),
            "score": payload.get("score", 0.0),
        }

    servicio = (plan or {}).get("servicio")
    fallback = _SERVICIO_TABLA_FALLBACK.get(servicio)
    if fallback:
        return {"tipo": "sql", **fallback, "score": 0.0}

    # último recurso genérico, para servicios sin tabla mapeada
    return {
        "tipo": "sql",
        "tablas": ["concentracao"],
        "schema_minimo": (
            "concentracao(ecgi, cluster, municipio, day_date, periodo, "
            "n_usuarios, download_gb, congestionamento_medio, rat_type_predominante)"
        ),
        "score": 0.0,
    }


async def schema_linker(state: AgentState) -> AgentState:
    """
    Decide si el tool_caller debe llamar a un endpoint o generar SQL.
    Primero intenta un ruteo determinístico basado en lo que el planner
    ya extrajo (servicio/indicador/palabras clave), y solo si no hay
    señal clara cae a búsqueda semántica en Qdrant.
    """
    request_id = state.get("request_id", "-")
    consulta = state["consulta"]
    plan = get_plan(state)
    consulta_lower = consulta.lower()

    logger.debug("[%s] SCHEMA_LINKER | consulta=%s | plan=%s",
                 request_id, consulta,
                 json.dumps(plan, ensure_ascii=False))

    # Paso 1: router determinístico por plan (más confiable que embeddings)
    result = _route_por_plan(plan, consulta_lower)

    if result:
        logger.info("[%s] SCHEMA_LINKER | ruteo determinístico -> %s",
                    request_id, result["id"])
    else:
        # Paso 2: fallback a embeddings, separando endpoint vs sql
        partes = [consulta]
        if plan.get("servicio"):
            partes.append(f"servicio: {plan['servicio']}")
        if plan.get("indicador"):
            partes.append(f"indicador: {plan['indicador']}")
        query_enriquecida = " | ".join(partes)

        logger.debug("[%s] SCHEMA_LINKER | sin señal determinística- buscando endpoints",
                     request_id)
        result = search(query_enriquecida, top_k=1, tipo="endpoint")

        if not result:
            logger.debug("[%s] SCHEMA_LINKER | sin match de endpoint- buscando tablas SQL",
                         request_id)
            result = search(query_enriquecida, top_k=1, tipo="sql")

    if result and result["tipo"] == "endpoint":
        decision = _build_endpoint_decision(result, plan, request_id)
    else:
        decision = _build_sql_decision(result, plan)

    logger.info("[%s] SCHEMA_LINKER | tipo=%s | endpoint=%s | score=%.4f",
                request_id, decision["tipo"],
                decision.get("endpoint", "sql"), decision.get("score", 0.0))
    logger.debug("[%s] SCHEMA_LINKER | decision=%s", request_id,
                 json.dumps(decision, ensure_ascii=False, indent=2))

    return {**state, "schema_decision": decision}