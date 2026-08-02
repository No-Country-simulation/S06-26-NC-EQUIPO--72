from app.agent.graph import _extraer_json_con_fallback


def test_json_limpio():
    plan = _extraer_json_con_fallback('{"servicio": "EMPLEO"}')
    assert plan["servicio"] == "EMPLEO"


def test_json_con_fences_markdown():
    raw = '```json\n{"servicio": "EMPLEO"}\n```'
    assert _extraer_json_con_fallback(raw)["servicio"] == "EMPLEO"


def test_json_con_texto_previo_y_posterior():
    raw = 'Claro, aquí tienes: {"servicio": "EMPLEO", "municipio": "São José"} espero que ayude'
    plan = _extraer_json_con_fallback(raw)
    assert plan["servicio"] == "EMPLEO"
    assert plan["municipio"] == "São José"


def test_json_con_trailing_comma_cae_a_plan_vacio_seguro():
    plan = _extraer_json_con_fallback('{"servicio": "EMPLEO",}')
    assert plan["fuera_de_dominio"] is False
    assert plan["servicio"] is None
    assert "fallback" in plan["razon"]


def test_garbage_devuelve_plan_vacio_seguro():
    plan = _extraer_json_con_fallback("esto no es JSON")
    assert plan["fuera_de_dominio"] is False
    assert plan["servicio"] is None
    assert plan["razon"] == "fallback por error de parseo"


def test_fuera_de_dominio_se_preserva():
    plan = _extraer_json_con_fallback('{"fuera_de_dominio": true, "razon": "matemática"}')
    assert plan["fuera_de_dominio"] is True
    assert plan["razon"] == "matemática"


def test_nunca_lanza_excepcion():
    for raw in ("", None, "```", "{", "[]", "{]", "{\"a\": 1", "<html>hola</html>"):
        try:
            result = _extraer_json_con_fallback(raw)
            assert isinstance(result, dict)
        except Exception:
            raise AssertionError(f"lanzó excepción para input: {raw!r}")
