import logging

from app.agent.merge import _merge_join


def test_join_exacto_cruza_campos():
    a = [{"cluster": "A", "n_usuarios": 100}, {"cluster": "B", "n_usuarios": 200}]
    b = [{"cluster": "A", "taxa_desemprego": 0.1}, {"cluster": "B", "taxa_desemprego": 0.2}]
    merged = _merge_join(a, b, "cluster")
    assert len(merged) == 2
    assert merged[0]["n_usuarios"] == 100
    assert merged[0]["taxa_desemprego"] == 0.1
    assert merged[1]["taxa_desemprego"] == 0.2
    assert set(merged[0]) == {"cluster", "n_usuarios", "taxa_desemprego"}


def test_join_a_prioridad_sobre_b_en_campos_iguales():
    a = [{"cluster": "A", "n_usuarios": 100}]
    b = [{"cluster": "A", "n_usuarios": 999, "extra": 1}]
    merged = _merge_join(a, b, "cluster")
    assert merged[0]["n_usuarios"] == 100  # A gana
    assert merged[0]["extra"] == 1          # B enriquece


def test_sin_match_en_b_se_incluye_con_datos_de_a():
    a = [{"cluster": "A"}, {"cluster": "C"}]
    b = [{"cluster": "A", "x": 1}]
    merged = _merge_join(a, b, "cluster")
    assert len(merged) == 2
    assert merged[1]["cluster"] == "C"
    assert "x" not in merged[1]


def test_join_key_inexistente_en_b_devuelve_a_sin_merge(caplog):
    a = [{"cluster": "A"}]
    b = [{"otra": "x"}]
    with caplog.at_level(logging.ERROR):
        merged = _merge_join(a, b, "cluster")
    assert merged == a
    assert "join_key" in caplog.text


def test_join_key_inexistente_en_a_devuelve_a():
    a = [{"otro": "y"}]
    b = [{"cluster": "A"}]
    assert _merge_join(a, b, "cluster") == a


def test_fuente_b_vacia_devuelve_a():
    a = [{"cluster": "A"}]
    assert _merge_join(a, [], "cluster") == a


def test_ambas_vacias_devuelve_vacio():
    assert _merge_join([], [], "cluster") == []


def test_join_multiple_se_puede_encadenar():
    a = [{"cluster": "A", "n": 1}]
    b = [{"cluster": "A", "x": 2}]
    c = [{"cluster": "A", "y": 3}]
    merged = _merge_join(_merge_join(a, b, "cluster"), c, "cluster")
    assert merged == [{"cluster": "A", "x": 2, "n": 1, "y": 3}]
