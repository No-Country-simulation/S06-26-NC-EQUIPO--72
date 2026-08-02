from app.agent.graph import (
    _route_after_planner,
    _route_after_classifier,
    _route_after_task_decomposer,
    _route_after_tool_caller,
    _aplicar_correccion_react,
    _gate_reflexion,
    _route_after_reflector,
)
from app.agent.schema_linker import (
    _build_endpoint_decision,
    _route_por_plan,
)
from app.core.config import settings
from langgraph.graph import END


# --- _route_after_planner (graph.py) ---

def test_route_after_planner_ood():
    assert _route_after_planner({"plan": {"fuera_de_dominio": True}}) == "fuera_de_dominio"


def test_route_after_planner_en_dominio():
    assert _route_after_planner({"plan": {"fuera_de_dominio": False}}) == "query_classifier"


def test_route_after_planner_sin_plan():
    assert _route_after_planner({"plan": {}}) == "query_classifier"


# --- _route_after_classifier / _route_after_task_decomposer ---

def test_route_after_classifier_compuesta():
    assert _route_after_classifier({"query_type": "compuesta"}) == "task_decomposer"


def test_route_after_classifier_simple():
    assert _route_after_classifier({"query_type": "simple"}) == "schema_linker"


def test_route_after_classifier_sin_tipo_default_simple():
    assert _route_after_classifier({}) == "schema_linker"


def test_route_after_task_decomposer_ok():
    assert _route_after_task_decomposer({"query_type": "compuesta"}) == "parallel_executor"


def test_route_after_task_decomposer_revertido_a_simple():
    assert _route_after_task_decomposer({"query_type": "simple"}) == "schema_linker"


# --- _route_por_plan (schema_linker.py) ---

def test_route_brecha_siempre_gana():
    r = _route_por_plan({"servicio": "EMPLEO"}, "¿dónde faltan programas de empleo?")
    assert r["endpoint"] == "/brechas"


def test_route_no_tienen_programas_a_brechas():
    # eval_004: "no tienen programas" es señal de brecha 
    r = _route_por_plan({"servicio": "EMPLEO"}, "¿qué zonas de Biguaçu no tienen programas de empleo?")
    assert r["endpoint"] == "/brechas"


def test_route_programas_a_catalogo():
    # eval_014: "programas de formación" sin señal de brecha -> catálogo /programas
    r = _route_por_plan({"servicio": "FORMACION"}, "¿qué programas de formación hay en Florianópolis?")
    assert r["endpoint"] == "/programas"


def test_route_programas_sociales_a_catalogo():
    # eval_013: "programas sociales" sin servicio -> catálogo /programas
    r = _route_por_plan({"municipio": "São José"}, "¿qué programas sociales hay en São José?")
    assert r["endpoint"] == "/programas"


def test_route_indicador_a_mapa_indicadores():
    r = _route_por_plan(
        {"servicio": "EMPLEO", "indicador": "taxa_desemprego"},
        "tasa de desempleo en Trindade",
    )
    assert r["endpoint"] == "/mapa/indicadores"


def test_route_servicio_social_a_mapa_indicadores():
    r = _route_por_plan({"servicio": "SALUD_MENTAL"}, "salud mental en Florianópolis")
    assert r["endpoint"] == "/mapa/indicadores"


def test_route_red_pura_sin_servicio_a_mapa():
    r = _route_por_plan({"servicio": None}, "¿cómo está la conectividad en Trindade?")
    assert r["endpoint"] == "/mapa"


def test_route_servicio_social_con_palabra_red_sigue_a_indicadores():
    # regla 3 (servicio social) se evalúa antes que la 4 (red pura, Fix Bug D)
    r = _route_por_plan({"servicio": "EMPLEO"}, "¿cómo está la conectividad en Trindade?")
    assert r["endpoint"] == "/mapa/indicadores"


def test_route_evolucion_qued_sombreada_por_indicador():
    # las consultas de evolución temporal YA NO son sombreadas por la
    # regla 2 (indicador -> /mapa/indicadores). Gana la regla 5 -> /indicadores/evolucion.
    r = _route_por_plan(
        {"servicio": "EMPLEO", "indicador": "taxa_desemprego"},
        "¿cómo evolucionó el desempleo?",
    )
    assert r["endpoint"] == "/indicadores/evolucion"


def test_route_indicador_sin_evolucion_sigue_a_mapa_indicadores():
    # Sin señales de evolución, un indicador puntual sigue yendo a /mapa/indicadores
    r = _route_por_plan(
        {"servicio": "EMPLEO", "indicador": "taxa_desemprego"},
        "¿cuál es la tasa de desempleo en São José?",
    )
    assert r["endpoint"] == "/mapa/indicadores"


def test_route_evolucion_sin_indicador_cae_a_mapa_indicadores():
    # La regla de evolución requiere indicador (plan 11.1). Sin indicador,
    # un servicio social con palabra "evolucionó" cae a /mapa/indicadores.
    r = _route_por_plan(
        {"servicio": "EMPLEO"},
        "¿cómo evolucionó el empleo en el último año?",
    )
    assert r["endpoint"] == "/mapa/indicadores"


def test_route_sin_senal_devuelve_none():
    assert _route_por_plan({}, "cuéntame sobre la ciudad") is None


# --- _build_endpoint_decision / Bug E (schema_linker.py) ---

def test_categoria_invalida_redirige_a_brechas():
    payload = {"endpoint": "/mapa/indicadores", "metodo": "GET", "score": 1.0}
    dec = _build_endpoint_decision(payload, {"servicio": "FORMACION", "municipio": "São José"})
    assert dec["endpoint"] == "/brechas"
    assert dec["params"]["servicio"] == "FORMACION"


def test_categoria_valida_mantiene_endpoint():
    payload = {"endpoint": "/mapa/indicadores", "metodo": "GET", "score": 1.0}
    dec = _build_endpoint_decision(
        payload, {"servicio": "EMPLEO", "indicador": "taxa_desemprego"}
    )
    assert dec["endpoint"] == "/mapa/indicadores"
    assert dec["params"]["categoria"] == "EMPLEO"


def test_categoria_invalida_no_muta_el_payload():
    payload = {"endpoint": "/mapa/indicadores", "metodo": "GET", "score": 1.0}
    _build_endpoint_decision(payload, {"servicio": "EXPERIENCIA"})
    assert payload["endpoint"] == "/mapa/indicadores"


def test_brechas_params_filtra_none():
    payload = {"endpoint": "/brechas", "metodo": "GET", "score": 1.0}
    dec = _build_endpoint_decision(payload, {"servicio": "MENTORIA"})
    assert dec["params"] == {"servicio": "MENTORIA"}


def test_evolucion_params_categoria_indicador_municipio():
    # /indicadores/evolucion recibe categoria/indicador/municipio
    payload = {"endpoint": "/indicadores/evolucion", "metodo": "GET", "score": 1.0}
    dec = _build_endpoint_decision(
        payload,
        {"servicio": "EMPLEO", "indicador": "taxa_desemprego", "municipio": "Florianópolis"},
    )
    assert dec["endpoint"] == "/indicadores/evolucion"
    assert dec["params"] == {
        "categoria": "EMPLEO",
        "indicador": "taxa_desemprego",
        "municipio": "Florianópolis",
    }


def test_evolucion_params_filtra_none():
    payload = {"endpoint": "/indicadores/evolucion", "metodo": "GET", "score": 1.0}
    dec = _build_endpoint_decision(payload, {"servicio": "EMPLEO"})
    assert dec["params"] == {"categoria": "EMPLEO"}


# --- _route_after_tool_caller / ReAct  ---

def test_react_retry_datos_vacios_simple():
    # Datos vacíos + retries disponibles + simple -> razonar ajuste
    state = {"tool_results": [], "react_retry_count": 0, "query_type": "simple"}
    assert _route_after_tool_caller(state) == "react_reasoner"


def test_react_con_datos_no_retry():
    assert _route_after_tool_caller(
        {"tool_results": [{"a": 1}], "react_retry_count": 0, "query_type": "simple"}
    ) == "output_guardrail"


def test_react_agotado_no_retry():
    # react_retry_count == max_retries_llm -> no más reintentos
    state = {
        "tool_results": [],
        "react_retry_count": settings.max_retries_llm,
        "query_type": "simple",
    }
    assert _route_after_tool_caller(state) == "output_guardrail"


def test_react_sin_contador_default_0():
    # Sin campo react_retry_count en estado -> se asume 0 (primer intento)
    state = {"tool_results": [], "query_type": "simple"}
    assert _route_after_tool_caller(state) == "react_reasoner"


def test_react_no_aplica_a_compuestas():
    # Las consultas compuestas manejan errores en parallel_executor, no ReAct
    state = {"tool_results": [], "react_retry_count": 0, "query_type": "compuesta"}
    assert _route_after_tool_caller(state) == "output_guardrail"


# --- _aplicar_correccion_react ---

def test_react_correccion_con_nuevo_endpoint():
    decision = {"tipo": "endpoint", "metodo": "GET", "endpoint": "/brechas", "params": {"servicio": "EMPLEO"}}
    reasoning = {"nuevo_endpoint": "/mapa/indicadores", "nuevos_params": {"categoria": "EMPLEO"}}
    nueva = _aplicar_correccion_react(decision, reasoning)
    assert nueva["endpoint"] == "/mapa/indicadores"
    assert nueva["tipo"] == "endpoint"
    assert nueva["params"] == {"categoria": "EMPLEO"}


def test_react_correccion_elimina_params_none():
    # httpx no omite None (envía "clave=" vacío) -> se filtran (mismo criterio schema_linker)
    decision = {"tipo": "endpoint", "metodo": "GET", "endpoint": "/programas", "params": {"tipo": "FORMACION"}}
    reasoning = {"nuevos_params": {"tipo": "FORMACION", "municipio": None}}
    nueva = _aplicar_correccion_react(decision, reasoning)
    assert nueva["params"] == {"tipo": "FORMACION"}


def test_react_correccion_solo_params_sin_endpoint():
    decision = {"tipo": "endpoint", "metodo": "GET", "endpoint": "/mapa", "params": {"periodo": "TARDE"}}
    reasoning = {"nuevos_params": {"periodo": "NOITE"}}
    nueva = _aplicar_correccion_react(decision, reasoning)
    assert nueva["endpoint"] == "/mapa"
    assert nueva["tipo"] == "endpoint"
    assert nueva["params"] == {"periodo": "NOITE"}


def test_react_correccion_endpoint_para_decision_sql():
    # Si el reasoner propone un endpoint para una decisión SQL, el tipo cambia a endpoint
    decision = {"tipo": "sql", "tablas": ["concentracao"], "schema_minimo": "..."}
    reasoning = {"nuevo_endpoint": "/mapa", "nuevos_params": {"municipio": "Florianópolis"}}
    nueva = _aplicar_correccion_react(decision, reasoning)
    assert nueva["tipo"] == "endpoint"
    assert nueva["endpoint"] == "/mapa"
    # Fix eval_007/028: la decisión SQL no traía 'metodo' -> tool_caller
    # crasheaba con KeyError. Al pasar a endpoint se setea GET.
    assert nueva.get("metodo") == "GET"
    assert nueva["params"] == {"municipio": "Florianópolis"}


def test_react_correccion_sin_cambios_mantiene_decision():
    decision = {"tipo": "endpoint", "metodo": "GET", "endpoint": "/mapa", "params": {}}
    reasoning = {"nuevo_endpoint": None, "nuevos_params": None}
    nueva = _aplicar_correccion_react(decision, reasoning)
    assert nueva == decision


# --- _gate_reflexion / _route_after_reflector ---

def test_gate_reflexion_buena_respuesta_omite():
    # Datos + respuesta larga + sin retry previo -> NO reflexionar
    state = {
        "tool_results": [{"a": 1}],
        "respuesta_ia": "x" * 120,
        "reflection_retry_count": 0,
    }
    assert _gate_reflexion(state) is False


def test_gate_reflexion_datos_vacios():
    assert _gate_reflexion({"tool_results": [], "respuesta_ia": "x" * 120}) is True


def test_gate_reflexion_respuesta_corta():
    assert _gate_reflexion({"tool_results": [{"a": 1}], "respuesta_ia": "corto"}) is True


def test_gate_reflexion_tool_error():
    state = {"tool_results": [{"a": 1}], "respuesta_ia": "x" * 120, "tool_error": "boom"}
    assert _gate_reflexion(state) is True


def test_gate_reflexion_ya_retryo_siempre_evalua():
    # Tras un retry siempre se re-evalúa (aunque la respuesta sea buena)
    state = {
        "tool_results": [{"a": 1}],
        "respuesta_ia": "x" * 120,
        "reflection_retry_count": 1,
    }
    assert _gate_reflexion(state) is True


def test_route_after_reflector_score_bueno_termina():
    assert _route_after_reflector({"reflection_score": 0.95}) == END


def test_route_after_reflector_score_pobre_retry():
    # score < min y hay presupuesto (retry_count < max) -> volver al formatter
    state = {
        "reflection_score": 0.3,
        "reflection_retry_count": 0,
        "request_id": "t",
    }
    assert _route_after_reflector(state) == "formatter"


def test_route_after_reflector_retry_agotado_termina():
    # Retries agotados (count == max) -> nunca más retry (regla count < max)
    state = {
        "reflection_score": 0.3,
        "reflection_retry_count": settings.reflector_max_retries,
        "request_id": "t",
    }
    assert _route_after_reflector(state) == END


def test_route_after_reflector_sin_score_default_termina():
    # Sin reflexión previa -> score default 1.0 -> termina
    assert _route_after_reflector({}) == END
