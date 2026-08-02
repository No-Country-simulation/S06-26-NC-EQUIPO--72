from app.agent.resumir import (
    _limpiar_para_formatter,
    _detectar_tipo_datos,
    _construir_contexto_formatter,
)
from app.services.ai_service import _detectar_idioma


# --- _limpiar_para_formatter ---

def test_limpiar_elimina_campos_internos():
    datos = [
        {"cluster": "UFSC", "ecgi": "123", "id": 5, "created_at": "2024-01-01"},
        {"cluster": "TRINDADE", "codigo_origem": "PNAD"},
    ]
    limpios = _limpiar_para_formatter(datos)
    assert limpios[0] == {"cluster": "UFSC"}
    assert limpios[1] == {"cluster": "TRINDADE"}


def test_limpiar_no_muta_original():
    datos = [{"cluster": "UFSC", "ecgi": "123"}]
    _limpiar_para_formatter(datos)
    assert datos[0] == {"cluster": "UFSC", "ecgi": "123"}


def test_limpiar_lista_vacia():
    assert _limpiar_para_formatter([]) == []


# --- _detectar_tipo_datos ---

def test_detectar_brechas_sociales():
    assert _detectar_tipo_datos([{"cluster": "X", "severidad_brecha": "ALTA"}]) == "brechas_sociales"


def test_detectar_indicadores_territoriales():
    assert _detectar_tipo_datos([{"cluster": "X", "indicadores": []}]) == "indicadores_territoriales"


def test_detectar_red_pura():
    assert _detectar_tipo_datos([{"cluster": "X", "rat_type_predominante": "LTE"}]) == "datos_red_pura"


def test_detectar_programas_sociales():
    assert _detectar_tipo_datos([{"tipo": "FORMACION", "organizacion": "ONG"}]) == "programas_sociales"


def test_detectar_sin_datos():
    assert _detectar_tipo_datos([]) == "sin_datos"


def test_detectar_generales():
    assert _detectar_tipo_datos([{"foo": "bar"}]) == "datos_generales"


# --- _construir_contexto_formatter ---

def test_contexto_incluye_feedback_de_reflexion():
    state = {
        "consulta": "¿tasa?", "idioma": "es",
        "tool_results": [{"cluster": "UFSC", "valor": 5}],
        "query_type": "simple",
        "reflection_feedback": "Mencioná valores",
        "schema_decision": {"endpoint": "/mapa/indicadores"},
    }
    ctx = _construir_contexto_formatter(state, state["tool_results"], False)
    assert "ATENCIÓN- mejorar estos aspectos: Mencioná valores" in ctx
    assert "Tipo de datos: datos_generales" in ctx


def test_contexto_sin_feedback_primera_generacion():
    state = {"consulta": "¿tasa?", "idioma": "es", "tool_results": []}
    ctx = _construir_contexto_formatter(state, [], False)
    assert "Primera generación- sin feedback previo" in ctx
    assert "Hay datos disponibles: NO" in ctx


# --- _detectar_idioma  ---

def test_idioma_explicito_pt_se_respeta():
    assert _detectar_idioma("hola que tal", "pt") == "pt"


def test_idioma_explicito_en_se_respeta():
    assert _detectar_idioma("hola", "en") == "en"


def test_idioma_es_con_texto_espanol():
    assert _detectar_idioma("¿Cuál es la tasa de desempleo?", "es") == "es"


def test_idioma_es_con_texto_portugues_autodetecta():
    assert _detectar_idioma("Qual a taxa de desemprego em Florianópolis?", "es") == "pt"


def test_idioma_default_es_si_no_se_detecta():
    assert _detectar_idioma("???", "es") == "es"
