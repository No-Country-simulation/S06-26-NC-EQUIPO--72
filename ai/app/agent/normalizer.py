import logging
import re
import unicodedata
import difflib

# Lista canónica de municipios válidos
MUNICIPIOS = ["Florianópolis", "São José", "Palhoça", "Biguaçu"]

# Lista canónica de los 23 clusters válidos
CLUSTERS = [
    "AEROPORTO_HLZ", "CAMPECHE", "CANASVIEIRAS", "CBD_BEIRAMAR", "CENTRO_HISTORICO",
    "COQUEIROS", "ESTREITO_CAPOEIRAS", "INGLESES", "JURERE", "LAGOA_CONCEICAO",
    "NORTE_ILHA", "RESIDENCIAL_NORTE", "SC401_CORREDOR", "TRINDADE", "UFSC",
    "VIA_EXPRESSA_CORREDOR", "SAO_JOSE_CENTRO", "SAO_JOSE_KOBRASOL", "SAO_JOSE_ROÇADO",
    "PALHOCA_CENTRO", "PALHOCA_PEDRA_BRANCA", "SAO_JOSE_BARREIROS", "BIGUACU_BR101_NORTE",
]

# Indicadores válidos reales- deben coincidir EXACTO con TerritorialIndicatorsSeeder.
# El planner puede alucinar variantes en español (ej. "taxa_empleo_formal" en vez de
# "taxa_emprego_formal"), así que se validan acá igual que municipio/cluster.
INDICADORES_VALIDOS = [
    "taxa_emprego_formal", "taxa_desemprego",
    "evasao_escolar", "taxa_conclusao_ensino_medio",
    "taxa_internacao_psiquiatrica", "cobertura_atencao_basica",
]


def _normalizar_texto(s: str) -> str:
    """Quita acentos y pasa a minúsculas para comparar sin importar tildes/mayúsculas."""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", sin_acentos).strip().lower()


def _fuzzy_match(valor: str, opciones: list[str], cutoff: float = 0.6) -> str | None:
    """
    Busca la opción canónica más parecida a `valor` usando distancia de edición.
    Devuelve None si no hay match suficientemente bueno (evita corregir a lo pavote).
    """
    if not valor:
        return None
    valor_norm = _normalizar_texto(valor)
    mapa_norm_a_original = {_normalizar_texto(o): o for o in opciones}

    # Match exacto primero (más rápido y sin falsos positivos)
    if valor_norm in mapa_norm_a_original:
        return mapa_norm_a_original[valor_norm]

    candidatos = difflib.get_close_matches(
        valor_norm, mapa_norm_a_original.keys(), n=1, cutoff=cutoff
    )
    if candidatos:
        return mapa_norm_a_original[candidatos[0]]

    # Fallback de contención: si el valor es substring significativo de UNA
    # única opción canónica (ej. "rocado" -> SAO_JOSE_ROÇADO), matchear.
    # Solo si es inequívoco- si hay más de una opción que lo contiene,
    # es ambiguo y se devuelve None para no corregir a lo pavote.
    coincidencias = [
        original
        for norm, original in mapa_norm_a_original.items()
        if len(valor_norm) >= 5 and valor_norm in norm
    ]
    if len(coincidencias) == 1:
        return coincidencias[0]

    return None


def normalizar_plan(plan: dict) -> dict:
    """
    Corrige de forma determinística (sin LLM) los campos municipio, cluster e indicador
    del plan contra las listas canónicas, tolerando typos y variantes de tildes/idioma.

    Esto evita que cada nodo del pipeline (planner, text-to-sql) tenga que
    "adivinar" el nombre correcto por su cuenta con resultados inconsistentes.
    """
    plan = dict(plan)

    municipio = plan.get("municipio")
    if municipio:
        corregido = _fuzzy_match(municipio, MUNICIPIOS)
        if corregido:
            plan["municipio"] = corregido
        # Si no hay match confiable, se deja como vino - mejor no forzar
        # una corrección incorrecta. El text-to-sql lo va a tratar como
        # texto libre y probablemente no matchee nada (0 filas, no un error).

    cluster = plan.get("cluster")
    if cluster:
        corregido = _fuzzy_match(cluster, CLUSTERS)
        if corregido:
            plan["cluster"] = corregido

    # El indicador es el campo donde el LLM más se equivoca (traduce "emprego" a
    # "empleo", o inventa uno cuando la consulta era genérica). Acá usamos un
    # cutoff más alto (0.75) que en municipio/cluster: para este campo es mejor
    # descartar (null -> trae todos los indicadores de la categoría) que dejar
    # pasar un nombre que no existe en la base y filtrar silenciosamente a 0 filas.
    indicador = plan.get("indicador")
    if indicador:
        if indicador in INDICADORES_VALIDOS:
            pass  # ya es válido, no tocar
        else:
            corregido = _fuzzy_match(indicador, INDICADORES_VALIDOS, cutoff=0.75)
            plan["indicador"] = corregido  # None si no hay match confiable

    return plan