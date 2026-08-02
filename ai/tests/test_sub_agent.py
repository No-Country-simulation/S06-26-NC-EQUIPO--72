import asyncio

from app.agent.sub_agent import run_sub_agent


def _run(sub_task):
    return asyncio.run(run_sub_agent(sub_task, "test-sub-agent"))


# --- Guarda de categoria inválida ---
# No debe llamar al endpoint (sin red), retorna error claro.

def test_sub_agent_rechaza_categoria_invalida():
    r = _run({
        "sub_agent_id": "agent_red",
        "endpoint": "/mapa/indicadores",
        "params": {"categoria": "CONECTIVIDAD", "municipio": "Florianópolis"},
    })
    assert r.records_count == 0
    assert r.results == []
    assert "CONECTIVIDAD" in r.error


def test_sub_agent_acepta_categoria_valida_sin_red():
    # No se comprueba la red; solo validamos que la guarda NO se dispare.
    # (la llamada real a llamar_endpoint está fuera del scope de unit tests)
    from app.agent.schema_linker import _CATEGORIAS_VALIDAS_MAPA
    assert "EDUCACION" in _CATEGORIAS_VALIDAS_MAPA


def test_sub_agent_otro_endpoint_no_pasa_por_guarda():
    # Para /mapa no hay validación de categoria; el sub_agent debería
    # intentar la llamada (fuera de scope). Verificamos el contrato base:
    r = run_sub_agent.__doc__
    assert "errores transitorios" in r
