from app.agent.normalizer import normalizar_plan


def test_municipio_exacto_normalizado():
    plan = normalizar_plan({"municipio": "São José"})
    assert plan["municipio"] == "São José"


def test_municipio_minuscula_corregido():
    plan = normalizar_plan({"municipio": "sao jose"})
    assert plan["municipio"] == "São José"


def test_municipio_typo_corregido():
    plan = normalizar_plan({"municipio": "Sao José"})
    assert plan["municipio"] == "São José"


def test_municipio_invalido_se_deja_sin_forzar():
    plan = normalizar_plan({"municipio": "Río de Janeiro"})
    assert plan["municipio"] == "Río de Janeiro"


def test_cluster_normalizado():
    plan = normalizar_plan({"cluster": "kobrasol"})
    assert plan["cluster"] == "SAO_JOSE_KOBRASOL"


def test_cluster_con_acento():
    plan = normalizar_plan({"cluster": "Roçado"})
    assert plan["cluster"] == "SAO_JOSE_ROÇADO"


def test_indicador_valido_no_se_toca():
    plan = normalizar_plan({"indicador": "taxa_emprego_formal"})
    assert plan["indicador"] == "taxa_emprego_formal"


def test_indicador_espanol_corregido():
    plan = normalizar_plan({"indicador": "taxa_empleo_formal"})
    assert plan["indicador"] == "taxa_emprego_formal"


def test_indicador_desconocido_se_descarta():
    plan = normalizar_plan({"indicador": "algo_inventado"})
    assert plan["indicador"] is None


def test_plan_vacio_no_rompe():
    assert normalizar_plan({}) == {}


def test_no_muta_el_plan_original():
    original = {"municipio": "sao jose"}
    normalizar_plan(original)
    assert original["municipio"] == "sao jose"


# --- Estabilidad: inferencia de servicio + override FOD ---

def test_servicio_inferido_desde_indicador():
    plan = normalizar_plan({"indicador": "cobertura_atencao_basica"})
    assert plan["servicio"] == "SALUD_MENTAL"


def test_servicio_inferido_desde_consulta_educacion():
    plan = normalizar_plan({"municipio": "São José"}, "¿Cómo está la educación en São José?")
    assert plan["servicio"] == "EDUCACION"


def test_servicio_no_se_sobrescribe_si_ya_existe():
    plan = normalizar_plan({"servicio": "MENTORIA"}, "programas de empleo")
    assert plan["servicio"] == "MENTORIA"


def test_fod_revertido_con_senal_de_dominio():
    plan = normalizar_plan({"fuera_de_dominio": True}, "¿Cómo está la conectividad en la región?")
    assert plan["fuera_de_dominio"] is False


def test_fod_no_se_toca_sin_senal_de_dominio():
    plan = normalizar_plan({"fuera_de_dominio": True}, "¿Cuánto es 2+2?")
    assert plan["fuera_de_dominio"] is True
    plan2 = normalizar_plan({"fuera_de_dominio": True}, "Contame un chiste")
    assert plan2["fuera_de_dominio"] is True
