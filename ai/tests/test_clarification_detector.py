from app.agent.graph import (
    _evaluar_señales_deterministicas,
    _merece_evaluacion_llm,
    _integrar_respuesta_al_plan,
)
from app.agent.state import es_consulta_corta_ambigua


# --- _evaluar_señales_deterministicas ---

def test_detector_servicios_multiplos():
    decision = _evaluar_señales_deterministicas(
        {"fuera_de_dominio": False},
        "¿Cómo están la mentoría y la formación en São José?",
        {},
    )
    assert decision is not None
    assert decision.necesita_clarificacion
    assert "2 tipos" in decision.pregunta
    assert "Mentoria" in decision.opciones
    assert "Formacion" in decision.opciones
    assert "Todos por separado" in decision.opciones


def test_detector_servicios_segun_planner():
    decision = _evaluar_señales_deterministicas(
        {"fuera_de_dominio": False, "servicio": "MENTORIA"},
        "¿Cómo están la mentoría y la formación?",
        {},
    )
    assert decision is not None
    assert decision.necesita_clarificacion


def test_detector_cluster_intermunicipal_sin_municipio():
    decision = _evaluar_señales_deterministicas(
        {"cluster": "ESTREITO_CAPOEIRAS", "municipio": None},
        "¿Qué brechas hay en ESTREITO_CAPOEIRAS?",
        {},
    )
    assert decision is not None
    assert decision.necesita_clarificacion
    assert "Florianópolis" in decision.opciones
    assert "São José" in decision.opciones


def test_detector_cluster_con_municipio_no_dispara():
    decision = _evaluar_señales_deterministicas(
        {"cluster": "ESTREITO_CAPOEIRAS", "municipio": "Florianópolis"},
        "¿Qué brechas hay en ESTREITO_CAPOEIRAS Florianópolis?",
        {},
    )
    assert decision is None


def test_detector_consulta_corta_sin_filtros():
    decision = _evaluar_señales_deterministicas(
        {"fuera_de_dominio": False},
        "¿Qué hay?",
        {},
    )
    assert decision is not None
    assert decision.necesita_clarificacion
    assert "RM de Florianópolis" in decision.pregunta


def test_detector_consulta_clara_sin_ambiguedad():
    decision = _evaluar_señales_deterministicas(
        {"fuera_de_dominio": False, "servicio": "MENTORIA", "municipio": "São José"},
        "¿Qué mentorías hay en São José?",
        {},
    )
    assert decision is None


def test_detector_consulta_larga_sin_filtros_no_corta():
    decision = _evaluar_señales_deterministicas(
        {"fuera_de_dominio": False},
        "¿Qué zonas de la región tienen más problemas de inclusión social?",
        {},
    )
    assert decision is None


# --- _merece_evaluacion_llm ---

def test_merece_evaluacion_llm_corta_sin_servicio():
    assert _merece_evaluacion_llm({}, "¿Qué zonas tienen problemas?")


def test_merece_evaluacion_llm_temporal_ambiguo():
    assert _merece_evaluacion_llm({"servicio": "EMPLEO"}, "¿Qué zonas del último mes tienen problemas?")


def test_no_merece_evaluacion_llm_clara():
    assert not _merece_evaluacion_llm(
        {"servicio": "MENTORIA", "municipio": "São José"},
        "¿Qué mentorías hay en São José este año?",
    )


# --- _integrar_respuesta_al_plan ---

def test_integrar_respuesta_servicio():
    plan = _integrar_respuesta_al_plan({}, "mentoría", {})
    assert plan["servicio"] == "MENTORIA"


def test_integrar_respuesta_formacion():
    plan = _integrar_respuesta_al_plan({}, "formación técnica", {})
    assert plan["servicio"] == "FORMACION"


def test_integrar_respuesta_salud_mental():
    plan = _integrar_respuesta_al_plan({}, "salud mental", {})
    assert plan["servicio"] == "SALUD_MENTAL"


def test_integrar_respuesta_sobrescribe_servicio_existente():
    # Corrección 3: la respuesta del gestor es autoritativa y sobrescribe
    # lo que el planner infirió (con 2+ servicios el planner "elige" uno).
    plan = _integrar_respuesta_al_plan({"servicio": "MENTORIA"}, "empleo", {})
    assert plan["servicio"] == "EMPLEO"


def test_integrar_respuesta_municipio_normaliza():
    plan = _integrar_respuesta_al_plan({}, "sao jose", {})
    assert plan["municipio"] == "São José"


def test_integrar_respuesta_ambas_limpia_servicio():
    plan = _integrar_respuesta_al_plan({"servicio": "MENTORIA"}, "ambas", {})
    assert plan["servicio"] is None


def test_integrar_respuesta_agrega_contexto_a_razon():
    plan = _integrar_respuesta_al_plan({"razon": "previo"}, "mentoría en Florianópolis", {})
    assert "respuesta_gestor" in plan["razon"]


def test_integrar_respuesta_sin_match_deja_contexto():
    plan = _integrar_respuesta_al_plan({}, "lo que haya", {})
    assert plan.get("servicio") is None
    assert "lo que haya" in plan["razon"]


# --- es_consulta_corta_ambigua (state.py) ---

def test_corta_ambigua_no_es_ruido():
    assert es_consulta_corta_ambigua({"consulta": "qué hay"})


def test_corta_ruido_no_es_ambigua():
    assert not es_consulta_corta_ambigua({"consulta": "hola"})


def test_corta_larga_no_es_ambigua():
    assert not es_consulta_corta_ambigua({"consulta": "qué mentorías hay disponibles hoy"})


def test_corta_matematica_no_es_ambigua():
    assert not es_consulta_corta_ambigua({"consulta": "¿Cuánto es 2+2?"})


def test_corta_chiste_no_es_ambigua():
    assert not es_consulta_corta_ambigua({"consulta": "contame un chiste"})


def test_corta_clima_no_es_ambigua():
    assert not es_consulta_corta_ambigua({"consulta": "clima hoy"})


def test_corta_donde_esta_si_es_ambigua():
    assert es_consulta_corta_ambigua({"consulta": "dónde está"})
