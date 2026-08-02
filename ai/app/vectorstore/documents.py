# Documentos a indexar: descripciones semánticas de endpoints y tablas.
# Cada texto está redactado para capturar la intención de las consultas
# que ese endpoint/tabla puede resolver, no solo el nombre técnico.

ENDPOINT_DOCUMENTS = [
    {
        "id": "ep_brechas",
        "tipo": "endpoint",
        "metodo": "GET",
        "endpoint": "/brechas",
        "params_disponibles": ["servicio", "municipio", "periodo", "income_cluster"],
        "texto": (
            "Zonas geográficas donde hay alta concentración de personas pero ningún programa social activo. "
            "Detecta brechas y carencias en formación técnica, mentoría, experiencias estructurales, "
            "empleo y salud mental por cluster y municipio. "
            "El filtro 'servicio' es OBLIGATORIO: FORMACION, MENTORIA, EXPERIENCIA, EMPLEO o SALUD_MENTAL. "
            "Calcula severidad de brecha combinando congestión de red, usuarios activos y ausencia de programas. "
            "Identifica dónde faltan programas, qué regiones tienen mayor desatención, "
            "zonas sin oferta para jóvenes de bajos ingresos (income D), "
            "clusters con alta demanda y cero programas activos, "
            "áreas vulnerables sin cobertura de servicios sociales en Florianópolis, São José, Palhoça y Biguaçu. "
            "Filtra por segmento de ingresos: A (alto), B (medio-alto), C (medio), D (bajo). "
            "Filtra por período del día: MADRUGADA, MANHA, TARDE, NOITE. "
            "Cubre 23 clusters distribuidos en 4 municipios de la RM de Florianópolis. "
            "ESTREITO_CAPOEIRAS es inter-municipal (Florianópolis y São José). "
            "SAO_JOSE_BARREIROS pertenece administrativamente a Palhoça."
        ),
    },
    {
        "id": "ep_mapa",
        "tipo": "endpoint",
        "metodo": "GET",
        "endpoint": "/mapa",
        "params_disponibles": ["periodo", "municipio", "fecha"],
        "texto": (
            "Solo datos de red móvil y tráfico de antenas, sin indicadores sociales. "
            "Concentración de personas y cobertura de red móvil por región geográfica. "
            "Muestra cuántos usuarios hay en cada zona, nivel de congestión de red, "
            "tecnología predominante (NR=5G, LTE=4G, WCDMA=3G), volumen de descarga en GB. "
            "Útil para mapas de calor de densidad poblacional, calidad de conectividad por zona, "
            "comparar períodos del día, detectar hotspots de tráfico de red. "
            "No incluye datos de empleo, salud mental ni educación. "
            "Cubre 132 antenas ERB reales de Claro en 23 clusters de la RM de Florianópolis. "
            "Filtra por período: MADRUGADA (00h-06h), MANHA (06h-12h, desplazamiento laboral), "
            "TARDE (12h-18h, pico de uso), NOITE (18h-00h, ocio y streaming)."
        ),
    },
    {
        "id": "ep_mapa_indicadores",
        "tipo": "endpoint",
        "metodo": "GET",
        "endpoint": "/mapa/indicadores",
        "params_disponibles": ["categoria", "indicador", "municipio"],
        "texto": (
            "Nivel de empleo, tasa de empleo formal, desempleo, situación laboral por zona. "
            "El filtro 'categoria' es OBLIGATORIO (SALUD_MENTAL, EMPLEO o EDUCACION). "
            "El filtro 'indicador' es OPCIONAL: sin especificarlo, devuelve TODOS los "
            "indicadores de esa categoría para la zona. Solo se usa cuando el usuario pide "
            "un valor puntual y específico, nunca para preguntas genéricas como 'nivel de "
            "empleo' o 'situación laboral'. "
            "Indicadores sociales y territoriales: salud mental (tasa de internación "
            "psiquiátrica, cobertura de atención básica), empleo (tasa de empleo formal, "
            "tasa de desempleo), educación (evasión escolar, tasa de conclusión de "
            "secundaria) por municipio o cluster. "
            "Responde preguntas como cuál es el nivel de empleo en una región, "
            "qué tan alto es el desempleo en una zona, cómo está la situación laboral, "
            "cuál es la tasa de internación psiquiátrica, indicadores de salud mental por área. "
            "Combina estos indicadores con datos de conectividad de red cuando es relevante. "
            "Útil para correlacionar cobertura de red con indicadores sociales, "
            "ver qué regiones tienen alto desempleo y baja conectividad simultáneamente, "
            "analizar vulnerabilidad social por cluster o municipio."
        ),
    },
    {
        "id": "ep_programas",
        "tipo": "endpoint",
        "metodo": "GET",
        "endpoint": "/programas",
        "params_disponibles": ["tipo", "municipio", "cluster", "activo"],
        "texto": (
            "Catálogo de programas sociales activos: formación técnica, mentoría y experiencias estructurales. "
            "Lista iniciativas disponibles por municipio y zona. "
            "Útil para saber qué programas existen, cuáles están activos, "
            "qué organización los gestiona, cuáles son replicables, "
            "programas de empleo, educación o salud mental disponibles en una región."
        ),
    },
    {
        "id": "ep_indicadores_evolucion",
        "tipo": "endpoint",
        "metodo": "GET",
        "endpoint": "/indicadores/evolucion",
        "params_disponibles": ["categoria", "indicador", "municipio"],
        "texto": (
            "Evolución histórica y tendencia temporal de un indicador social. "
            "Cómo cambió un indicador mes a mes o año a año. "
            "Responde: ¿el desempleo bajó el último año?, ¿cómo evolucionó la "
            "tasa de internación psiquiátrica?, ¿cuál es la tendencia del empleo "
            "formal en Florianópolis? "
            "El filtro 'categoria' es OBLIGATORIO (SALUD_MENTAL, EMPLEO o EDUCACION). "
            "El filtro 'indicador' es OBLIGATORIO para la serie de un indicador puntual. "
            "Devuelve serie temporal con fecha_referencia y valor_promedio."
        ),
    },
]

TABLE_DOCUMENTS = [
    {
        "id": "tbl_concentracao",
        "tipo": "sql",
        "tablas": ["concentracao"],
        "schema_minimo": (
            "concentracao(ecgi VARCHAR, cluster VARCHAR, municipio VARCHAR, "
            "day_date DATE, periodo VARCHAR, n_usuarios INT, "
            "download_gb FLOAT, congestionamento_medio FLOAT, rat_type_predominante VARCHAR)"
        ),
        "texto": (
            "Datos crudos de concentración de red por antena y período horario. "
            "Serie temporal de usuarios, descargas y congestión por día. "
            "Útil para análisis históricos, tendencias temporales, "
            "comparar períodos específicos, evolución de métricas de red en el tiempo."
        ),
    },
    {
        "id": "tbl_indicadores",
        "tipo": "sql",
        "tablas": ["indicadores_territoriales"],
        "schema_minimo": (
            "indicadores_territoriales(municipio VARCHAR, cluster VARCHAR, "
            "categoria VARCHAR, indicador VARCHAR, valor DECIMAL, "
            "unidad VARCHAR, fonte VARCHAR, fecha_referencia DATE)"
        ),
        "texto": (
            "Métricas estadísticas poblacionales por zona: salud mental, empleo y educación. "
            "Datos de DATASUS, IBGE y OMS. "
            "Útil para consultas específicas sobre indicadores individuales, "
            "valores exactos de un indicador en una zona, comparar fuentes estadísticas."
        ),
    },
    {
        "id": "tbl_mobilidade",
        "tipo": "sql",
        "tablas": ["mobilidade_agregada"],
        "schema_minimo": (
            "mobilidade_agregada(ecgi VARCHAR, cluster VARCHAR, municipio VARCHAR, "
            "day_date DATE, periodo VARCHAR, income_cluster CHAR, "
            "age_group VARCHAR, rat_type VARCHAR, n_sessoes INT, drop_pct_avg FLOAT)"
        ),
        "texto": (
            "Patrones de movilidad segmentados por demografía: edad, nivel de ingresos y tecnología de red. "
            "Útil para analizar comportamiento de segmentos específicos, "
            "jóvenes de bajos ingresos, adultos mayores, comparar grupos demográficos por zona."
        ),
    },
    {
        "id": "tbl_flujo_od",
        "tipo": "sql",
        "tablas": ["flujo_od"],
        "schema_minimo": (
            "flujo_od(cluster_origem VARCHAR, cluster_destino VARCHAR, "
            "municipio_origem VARCHAR, municipio_destino VARCHAR, "
            "n_usuarios INT, n_viagens INT, dist_media_km FLOAT)"
        ),
        "texto": (
            "Flujos de desplazamiento de personas entre zonas geográficas. "
            "Origen y destino de viajes, distancia media, cantidad de usuarios que se mueven entre clusters. "
            "Útil para entender movilidad interurbana, patrones de desplazamiento, "
            "zonas que reciben o expulsan personas."
        ),
    },
]

ALL_DOCUMENTS = ENDPOINT_DOCUMENTS + TABLE_DOCUMENTS