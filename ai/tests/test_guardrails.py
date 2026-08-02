import asyncio

from app.agent.guardrails import _sanitizar_consulta, input_guardrail, output_guardrail
from app.agent.graph import _route_after_input_guardrail
from app.services.ai_service import _es_probablemente_compuesta


def _run(coro):
    return asyncio.run(coro)


# --- _sanitizar_consulta ---

def test_sanitizar_trunca_a_500_chars():
    larga = "a" * 600
    result = _sanitizar_consulta(larga)
    assert len(result) == 500


def test_sanitizar_elimina_caracteres_de_control():
    assert _sanitizar_consulta("hola\x00mundo\x01") == "holamundo"


def test_sanitizar_conserva_nueva_linea_y_tab():
    assert _sanitizar_consulta("hola\n\tmundo") == "hola\n\tmundo"


def test_sanitizar_strip_extremos():
    assert _sanitizar_consulta("  hola  ") == "hola"


# --- input_guardrail ---

def test_input_guardrail_rechaza_vacia():
    r = _run(input_guardrail({"consulta": "  ", "request_id": "t"}))
    assert r["fuera_de_dominio"] is True
    assert "vacía" in r["respuesta_ia"]


def test_input_guardrail_rechaza_corta():
    r = _run(input_guardrail({"consulta": "ab", "request_id": "t"}))
    assert r["fuera_de_dominio"] is True


def test_input_guardrail_sanitiza_consulta_valida():
    r = _run(input_guardrail({"consulta": "  ¿tasa de desempleo?\x00  ", "request_id": "t"}))
    assert r.get("fuera_de_dominio") is None
    assert r["consulta"] == "¿tasa de desempleo?"


def test_route_after_input_guardrail_valido_a_planner():
    assert _route_after_input_guardrail({"fuera_de_dominio": False}) == "planner"


def test_route_after_input_guardrail_invalido_a_end():
    from langgraph.graph import END
    assert _route_after_input_guardrail({"fuera_de_dominio": True}) == END


# --- output_guardrail ---

def test_output_guardrail_ok_sin_advertencias():
    r = _run(output_guardrail({
        "request_id": "t",
        "tool_results": [{"cluster": "UFSC", "severidad_brecha": "ALTA"}],
        "schema_decision": {"endpoint": "/brechas"},
    }))
    assert r["datos_validos"] is True
    assert r["tool_results_meta"]["advertencias"] == []


def test_output_guardrail_resultado_vacio_es_datos_validos():
    # Solo la advertencia "resultado vacío" NO invalida (el formatter lo explica)
    r = _run(output_guardrail({
        "request_id": "t",
        "tool_results": [],
        "schema_decision": {"endpoint": "/mapa"},
    }))
    assert r["datos_validos"] is True
    assert "resultado vacío" in r["tool_results_meta"]["advertencias"]


def test_output_guardrail_tool_error_invalida():
    r = _run(output_guardrail({
        "request_id": "t",
        "tool_results": [{"a": 1}],
        "tool_error": "boom",
        "schema_decision": {"endpoint": "/mapa"},
    }))
    assert r["datos_validos"] is False


def test_output_guardrail_brechas_sin_severidad_advertido():
    r = _run(output_guardrail({
        "request_id": "t",
        "tool_results": [{"cluster": "UFSC", "programas_activos": 3}],
        "schema_decision": {"endpoint": "/brechas"},
    }))
    assert "sin campo severidad_brecha" in r["tool_results_meta"]["advertencias"][0]


def test_output_guardrail_sub_agente_con_error_advertido():
    r = _run(output_guardrail({
        "request_id": "t",
        "tool_results": [{"cluster": "UFSC"}],
        "sub_agent_results": [
            {"sub_agent_id": "agent_red", "error": "HTTP 400"},
        ],
        "schema_decision": {"endpoint": "/mapa"},
    }))
    assert r["datos_validos"] is False
    assert any("agent_red" in a for a in r["tool_results_meta"]["advertencias"])


# --- _es_probablemente_compuesta ---

def test_compuesta_detecta_relacion():
    assert _es_probablemente_compuesta("relación entre conectividad y educación") is True


def test_compuesta_detecta_y():
    assert _es_probablemente_compuesta("desempleo y conectividad en Florianópolis") is True


def test_compuesta_detecta_ademas():
    assert _es_probablemente_compuesta("además de los programas de empleo") is True


def test_simple_sin_marcadores():
    assert _es_probablemente_compuesta("tasa de desempleo en Florianópolis") is False
