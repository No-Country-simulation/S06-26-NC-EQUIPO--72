import logging
import json
from app.agent.state import AgentState
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
    "sin programa", "sin cobertura", "sin oferta",
)


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

    # 2. Si el planner ya identificó un indicador específico, siempre es /mapa/indicadores.
    #    No importa si la consulta menciona además "conectividad" o "red" de pasada.
    if plan.get("indicador"):
        return {
            "id": "ep_mapa_indicadores",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/mapa/indicadores",
            "score": 1.0,
        }

    # 3. Si el servicio es uno de los que tienen indicador social (EMPLEO, SALUD_MENTAL)
    #    y no es consulta de brecha, también es /mapa/indicadores.
    if plan.get("servicio") in ("EMPLEO", "SALUD_MENTAL"):
        return {
            "id": "ep_mapa_indicadores",
            "tipo": "endpoint",
            "metodo": "GET",
            "endpoint": "/mapa/indicadores",
            "score": 1.0,
        }

    return None  # sin señal clara -> vector search decide


def _build_endpoint_decision(payload: dict, plan: dict) -> dict:
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
            "periodo": plan.get("periodo", "TARDE"),
            "income_cluster": plan.get("income_cluster"),
        }
    elif endpoint == "/mapa":
        params = {
            "periodo": plan.get("periodo", "TARDE"),
            "municipio": plan.get("municipio"),
            "fecha": plan.get("fecha"),
        }
    elif endpoint == "/mapa/indicadores":
        # categoria usa los mismos valores que servicio para SALUD_MENTAL/EMPLEO/EDUCACION
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
    consulta = state["consulta"]
    plan = state.get("plan", {})
    consulta_lower = consulta.lower()

    print("\n" + "="*80, flush=True)
    print("=== TEST SCHEMA LINKING Y EMBEDDINGS ===", flush=True)
    print(f"Consulta: {consulta}", flush=True)
    print(f"Plan del planner: {json.dumps(plan, ensure_ascii=False, indent=2)}", flush=True)

    # Paso 1: router determinístico por plan (más confiable que embeddings)
    result = _route_por_plan(plan, consulta_lower)

    if result:
        print(f"\nRuteo determinístico por plan -> {result['id']}", flush=True)
    else:
        # Paso 2: fallback a embeddings, separando endpoint vs sql
        partes = [consulta]
        if plan.get("servicio"):
            partes.append(f"servicio: {plan['servicio']}")
        if plan.get("indicador"):
            partes.append(f"indicador: {plan['indicador']}")
        query_enriquecida = " | ".join(partes)

        print("\nSin señal determinística. Buscando entre ENDPOINTS...", flush=True)
        result = search(query_enriquecida, top_k=1, tipo="endpoint")

        if not result:
            print("Sin match de endpoint. Buscando entre TABLAS SQL...", flush=True)
            result = search(query_enriquecida, top_k=1, tipo="sql")

    print("\nResultado del schema linker:", flush=True)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    else:
        print("No se encontró ningún resultado (fallback a SQL genérico)", flush=True)

    if result and result["tipo"] == "endpoint":
        decision = _build_endpoint_decision(result, plan)
    else:
        decision = _build_sql_decision(result, plan)

    print("\nDecisión final del schema linker:", flush=True)
    print(json.dumps(decision, ensure_ascii=False, indent=2), flush=True)
    print("="*80 + "\n", flush=True)

    logger.info("Schema linker decision: %s", decision)
    return {**state, "schema_decision": decision}