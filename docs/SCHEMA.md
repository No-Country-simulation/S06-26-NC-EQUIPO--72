## Schema inicial basado en: [CDRView_AppBiT_TechnicalReference_v2_es](CDRView_AppBiT_TechnicalReference_v2_es.md)

las siguientes tablas cubren los servicios de formaciones y empleabilidad
```sql
antenas
ecgi          VARCHAR(12)   PK   -- siempre string, nunca numeric
cluster       VARCHAR(40)
municipio     VARCHAR(60)
lat           DECIMAL(10,6)
lon           DECIMAL(10,6)
```

```sql
assinantes
assinante_hash   INT          PK
home_cluster     VARCHAR(40)
home_municipio   VARCHAR(60)
income_cluster   CHAR(1)      -- A / B / C / D
age_group        VARCHAR(5)   -- 18-24 / 25-34 / 35-44 / 45-54 / 55+
mobility_pattern VARCHAR(10)  -- BAIXA / MODERADA / INTENSA
flag_flagship    SMALLINT     -- 0 / 1
```

```sql
concentracao
id             SERIAL        PK
ecgi           VARCHAR(12)   FK -> antenas
cluster        VARCHAR(40)
municipio      VARCHAR(60)
day_date       DATE
periodo        VARCHAR(12)   -- MADRUGADA / MANHA / TARDE / NOITE
n_usuarios     INT
download_gb    FLOAT
congestionamento_medio  FLOAT
rat_type_predominante   VARCHAR(5)  -- NR / LTE / WCDMA
```

```sql
mobilidade_agregada
id             SERIAL        PK
ecgi           VARCHAR(12)   FK -> antenas
cluster        VARCHAR(40)
municipio      VARCHAR(60)
day_date       DATE
periodo        VARCHAR(12)
income_cluster CHAR(1)
age_group      VARCHAR(5)
rat_type       VARCHAR(5)
n_sessoes      INT
download_bytes FLOAT
drop_pct_avg   FLOAT
congestionamento_avg  FLOAT
```

```sql
flujo_od
id                  SERIAL       PK
cluster_origem      VARCHAR(40)
cluster_destino     VARCHAR(40)
municipio_origem    VARCHAR(60)
municipio_destino   VARCHAR(60)
n_usuarios          INT
n_viagens           INT
dist_media_km       FLOAT
mesmo_cluster       SMALLINT     -- 0 / 1
```

```sql
fluxo_vias
id                  SERIAL       PK
ecgi_origem         VARCHAR(12)  FK -> antenas
ecgi_destino        VARCHAR(12)  FK -> antenas
cluster_origem      VARCHAR(40)
cluster_destino     VARCHAR(40)
n_usuarios          INT
n_transicoes        INT
dist_km             FLOAT
periodo_predominante VARCHAR(12)
pct_do_cluster_origem FLOAT
```



detalle: no agrego tensor secuencias al schema porque no aporta informacion relevante, dado que los 5 servicios (formaciones, empleabilidad, salud mental, etc.) todos operan a nivel de zona y no de trayecto individual. Además, pesa una banda.
En caso de que el front quiera agregar trayectos individuales en el mapa se podria agregar (hablarlo con jonathan porque está fuera del scope)

las siguientes tablas cubren los servicios de salud mental, mentorias y experiencias estructurales:

Tablas de dominio

```sql
programas_sociales
id                  SERIAL        PK
nombre              VARCHAR(150)
tipo                VARCHAR(30)   -- FORMACION / MENTORIA / EXPERIENCIA
descripcion         TEXT
municipio           VARCHAR(60)
cluster             VARCHAR(40)   -- FK semántica -> antenas.cluster
organizacion        VARCHAR(150)
lider_referente     VARCHAR(150)  NULL   -- relevante para tipo EXPERIENCIA
replicable          SMALLINT      NULL   -- 0 / 1, relevante para tipo EXPERIENCIA
impacto_estimado    VARCHAR(10)   NULL   -- BAJO / MEDIO / ALTO
url_referencia      VARCHAR(255)  NULL
fecha_inicio        DATE
fecha_fin           DATE          NULL
activo              SMALLINT      -- 0 / 1
```

```sql
indicadores_territoriales
id                  SERIAL          PK
municipio           VARCHAR(60)
cluster             VARCHAR(40)     -- FK semántica -> antenas.cluster
categoria           VARCHAR(30)     -- SALUD_MENTAL / EMPLEO / EDUCACION
indicador           VARCHAR(100)    -- taxa_internacao_psiquiatrica / taxa_emprego_formal / etc
valor               DECIMAL(15,4)
unidad              VARCHAR(30)
fonte               VARCHAR(50)     -- DATASUS / IBGE / OMS / MOCK
codigo_origem       VARCHAR(100)    -- SIH-SUS / PNAD / GHO
url_origem          TEXT            NULL
fecha_referencia    DATE
created_at          TIMESTAMP       DEFAULT NOW()
updated_at          TIMESTAMP       DEFAULT NOW()
```

## Fundamentos
El dataset Vísent CDRView provee datos de movilidad y cobertura de red a nivel de antena y zona geográfica. Los 5 servicios del producto operan todos a nivel de región, por eso el schema refleja esa granularidad.

### Por qué dos tipos de tablas de dominio?
programas_sociales es cargada por el gestor público porque no hay fuente pública estructurada que consolide iniciativas de mentoría, experiencias comunitarias y programas de formación por municipio. El gestor municipal es la única fuente de verdad para eso.

indicadores_territoriales nunca la carga el gestor a mano. Son datos estadísticos poblacionales que deben venir de fuentes oficiales (DATASUS, IBGE, OMS). En el MVP se carga con seeders (fonte = 'MOCK'). En caso de que vayamos bien con el tiempo se reemplaza con un pipeline ETL.