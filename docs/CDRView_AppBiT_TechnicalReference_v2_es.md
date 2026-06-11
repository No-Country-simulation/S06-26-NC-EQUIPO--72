# CDRView · App BiT · Referencia Técnica v2
**CONFIDENCIAL · jun/2026**

*Technical Reference v2 — Base de Datos **Sintética** de Movilidad Urbana*

Visent · OSX Telecomunicações S/A · Junio de 2026 · CONFIDENCIAL

---

## Novedades en la Versión 2 (08/06/2026)

> **[NUEVO]** Esta versión agrega dos nuevos archivos sin modificar los anteriores. Los archivos de la v1 permanecen idénticos y válidos.

| **Archivo Nuevo** | **Descripción** |
|---|---|
| `tensor_sequencias.csv` | Secuencia ordenada de antenas visitadas por cada suscriptor en cada día, con `arrival_time` y distancia recorrida. Permite el análisis de trayectos individuales e identificación de vías urbanas. |
| `tensor_fluxo_vias.csv` | Pares de antenas consecutivas agregados con volumen de usuarios y porcentaje de flujo. Permite la visualización de corredores e identificación de cuellos de botella en vías. |

---

# 1. Introducción

Este documento es la guía técnica oficial de la base de datos disponibilizada para los participantes del Hackathon App BiT. Describe el origen, el esquema, las reglas de negocio y las buenas prácticas de consumo de cada archivo CSV entregado. Léalo íntegramente antes de comenzar el desarrollo de su aplicación.

La base es sintética — generada por un framework propietario de Visent que reproduce fielmente los patrones de comportamiento de movilidad urbana observados en redes móviles reales. En entorno de producción, estos datos serían generados por la plataforma CDRView STEP - Social Telemetry Extensible Platform a partir de CDR/IPDR de los operadores, procesados con k-anonimato y cargados en la base de datos Oracle.

## 1.1 Alianza y Contexto

| **Atributo** | **Valor** |
|---|---|
| Evento | Hackathon Soberanía Digital & App BiT |
| Período | Junio–Julio 2026 · Demo Day: 10/07/2026 |
| Socios | Visent · Wongola · Angola Cables · Oracle · PMI-SP |
| Región de estudio | Región Metropolitana de Florianópolis, SC, Brasil |
| Escala de la base | 200.000 suscriptores sintéticos · 15 días de movilidad |
| Antenas | 132 ERBs reales de Claro (Anatel) geocodificadas en la RM |
| Clústeres | 27 zonas geográficas calibradas por población IBGE 2022 |
| K-anonimato | K=3 (hackathon) · K=5 obligatorio en producción (LGPD Art. 12) |
| Formato de entrega | CSV (separador coma, codificación UTF-8) |

> **[!]** Esta base es FICTICIA. No se utilizaron datos reales de suscriptores ni de operadores. Las antenas fueron obtenidas de la base pública de Anatel. Cualquier semejanza con datos reales es coincidencia estadística del modelo generativo.

---

# 2. Arquitectura de la Base de Datos

La base está compuesta por ocho archivos CSV interrelacionados, organizados en tres capas:

| **Capa** | **Archivos** |
|---|---|
| Referencia | `antenas_flp.csv` · `assinantes.csv` |
| Movilidad bruta | `tensor_mobilidade.csv` |
| Trayectos | `tensor_sequencias.csv` [NUEVO] |
| Semántica | `tensor_concentracao.csv` · `tensor_od.csv` · `tensor_fluxo_vias.csv` [NUEVO] · `tensor_tempo_deslocamento.csv` |

## 2.1 Guía de uso por tipo de análisis

| **Análisis** | **Archivo principal** |
|---|---|
| Mapa de calor de concentración | `tensor_concentracao.csv` |
| Flujo entre barrios / zonas | `tensor_od.csv` o `trajetos_comuns.csv` |
| Carga en vías y corredores | `tensor_fluxo_vias.csv` [NUEVO] |
| Trayecto completo de un suscriptor | `tensor_sequencias.csv` [NUEVO] |
| Segmentación demográfica | `assinantes.csv` |
| Análisis de calidad de red | `tensor_mobilidade.csv` |
| Tiempo promedio entre zonas | `tensor_tempo_deslocamento.csv` |

---

# 3. antenas_flp.csv — Catálogo de Antenas

132 ERBs reales de Claro en la RM de Florianópolis, extraídas del archivo oficial de Anatel y geocodificadas para los 27 clústeres de movilidad.

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `ecgi` | STRING(12) | Identificador único de la celda. **CRÍTICO:** tratar siempre como STRING. |
| `cluster` | STRING(40) | Zona geográfica de movilidad (27 zonas). |
| `municipio` | STRING(60) | Municipio real de la ERB. |
| `lat` | FLOAT(10,6) | Latitud WGS-84 en grados decimales. |
| `lon` | FLOAT(10,6) | Longitud WGS-84 en grados decimales. |

---

# 4. assinantes.csv — Perfil Demográfico

Un registro por suscriptor sintético con atributos demográficos inferidos.

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `assinante_hash` | INT32 | Identificador único anonimizado (1 a N). |
| `home_cluster` | STRING(40) | Clúster de residencia probable. |
| `home_municipio` | STRING(60) | Municipio del `home_cluster`. |
| `income_cluster` | CHAR(1) | Rango de ingresos: A (alto) B (medio-alto) C (medio) D (bajo). |
| `age_group` | STRING(5) | Rango etario: 18-24 / 25-34 / 35-44 / 45-54 / 55+ |
| `mobility_pattern` | STRING(10) | Patrón: BAIXA (1-2 antenas/día) MODERADA (2-4) INTENSA (4-8). |
| `flag_flagship` | INT8 (0/1) | 1 si el dispositivo es de gama alta. |

---

# 5. tensor_mobilidade.csv — Base Principal de Movilidad

Archivo central de la base. Cada fila representa la actividad agregada de un suscriptor en una antena durante un período del día.

> **[!]** Este archivo tiene ~12 millones de filas y 2,7 GB. Use siempre lectura en chunks. Nunca lo cargue íntegramente en memoria.

| **Atributo** | **Valor** |
|---|---|
| Filas | ~12.000.000 (200K suscriptores × 15 días × ~4 eventos/día) |
| Tamaño CSV | ~2,7 GB |
| Granularidad | suscriptor × día × antena × período × tipo de contenido |

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `assinante_hash` | INT32 | Clave del suscriptor. |
| `day_date` | DATE (ISO) | Fecha en formato YYYY-MM-DD. |
| `ecgi` | STRING(12) | Antena visitada. Tratar siempre como string. |
| `cluster` | STRING(40) | Zona geográfica (desnormalizado). |
| `municipio` | STRING(60) | Municipio de la antena (desnormalizado). |
| `rg_type` | STRING(20) | Tipo de contenido: STREAMING GAMING SOCIAL COMUNICACAO VPN OUTROS. |
| `rat_type` | STRING(5) | Tecnología: NR (5G) LTE (4G) WCDMA (3G). |
| `periodo_sessao` | STRING(12) | MADRUGADA / MANHA / TARDE / NOITE. |
| `n_sessoes` | INT32 | Cantidad de sesiones de datos en el período. |
| `dur_total_s` | INT32 | Duración total acumulada en segundos. |
| `download_bytes` | FLOAT32 | Total de bytes recibidos. |
| `upload_bytes` | FLOAT32 | Total de bytes enviados. |
| `drop_pct` | FLOAT(8,4) | Tasa de paquetes descartados [0.0–1.0]. |
| `congestionamento` | FLOAT(6,3) | Nivel de congestión de la celda [0.0–1.0]. |
| `chamadas` | INT16 | Cantidad de llamadas de voz. |
| `conversacao_seg` | INT32 | Total de segundos en conversación de voz. |
| `completamento_voz` | FLOAT(6,3) | Tasa de llamadas completadas [0.0–1.0]. |
| `mensagens` | INT16 | Cantidad de SMS enviados/recibidos. |
| `income_cluster` | CHAR(1) | Rango de ingresos del suscriptor (desnormalizado). |
| `age_group` | STRING(5) | Rango etario del suscriptor (desnormalizado). |
| `flag_flagship` | INT8 (0/1) | 1 si el dispositivo es de gama alta (desnormalizado). |

---

# 6. tensor_sequencias.csv — Secuencia de Antenas por Suscriptor [NUEVO]

> **[NUEVO]** Archivo nuevo en v2. Permite el análisis de trayectos individuales, identificación de vías urbanas y cálculo de carga por corredor.

Una fila por (suscriptor, día, posición en la secuencia). Las antenas están ordenadas por período del día (MADRUGADA → MANHA → TARDE → NOITE) y, dentro de cada período, por volumen de sesiones (mayor primero). El `arrival_time` es el timestamp sintético de la primera sesión en la antena, generado dentro de la ventana del `periodo_sessao`. En producción, CDRView lo reemplaza por el timestamp real del primer CDR de la celda.

| **Atributo** | **Valor** |
|---|---|
| Filas | ~7–10 millones (200K suscriptores × 15 días × ~3 antenas/día) |
| Tamaño CSV | ~915 MB |
| Granularidad | suscriptor × día × posición en la secuencia |

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `assinante_hash` | INT32 | Identificador del suscriptor. |
| `day_date` | DATE (ISO) | Fecha en formato YYYY-MM-DD. |
| `seq_num` | INT16 | Posición en la secuencia del día (1, 2, 3...). |
| `ecgi` | STRING(12) | Antena visitada. Tratar siempre como string. |
| `cluster` | STRING(40) | Zona geográfica de la antena. |
| `municipio` | STRING(60) | Municipio de la antena. |
| `lat` | FLOAT(10,6) | Latitud de la antena. |
| `lon` | FLOAT(10,6) | Longitud de la antena. |
| `arrival_time` | DATETIME | Timestamp de la 1ª sesión en la antena (ISO 8601). Sintético en dev; real en producción vía CDRView. |
| `permanencia_seg` | INT32 | Tiempo estimado de permanencia en segundos (`dur_total_s` / `n_sessoes`). |
| `periodo_sessao` | STRING(12) | Período predominante: MADRUGADA / MANHA / TARDE / NOITE. |
| `distancia_km_anterior` | FLOAT(8,3) | Distancia Haversine desde la antena anterior en km. Cero en la primera antena del día. |
| `n_sessoes` | INT32 | Volumen de sesiones de datos en esa antena en el día. |

## 6.1 Ejemplo de uso — Trayecto de un suscriptor

```sql
SELECT seq_num, ecgi, cluster, arrival_time,
       permanencia_seg, distancia_km_anterior
FROM tensor_sequencias
WHERE assinante_hash = 12345
  AND day_date = DATE '2026-03-05'
ORDER BY seq_num;
```

## 6.2 Ejemplo de uso — Vía identificada como secuencia de antenas

```sql
-- Pares de antenas consecutivas a lo largo de la BR-101
SELECT a.seq_num, a.ecgi AS antena_entrada,
       b.ecgi AS antena_saida,
       a.cluster, b.cluster AS cluster_destino,
       a.distancia_km_anterior AS dist_trecho_km
FROM tensor_sequencias a
JOIN tensor_sequencias b
  ON  b.assinante_hash = a.assinante_hash
  AND b.day_date       = a.day_date
  AND b.seq_num        = a.seq_num + 1
WHERE a.cluster IN ('BIGUACU_BR101_NORTE','SAO_JOSE_ROCADO',
                    'SAO_JOSE_KOBRASOL','VIA_EXPRESSA_CORREDOR')
ORDER BY a.assinante_hash, a.day_date, a.seq_num;
```

---

# 7. tensor_fluxo_vias.csv — Flujo entre Pares de Antenas [NUEVO]

> **[NUEVO]** Archivo nuevo en v2. Es la agregación del `tensor_sequencias` por pares de antenas consecutivas. Use este archivo para visualización de corredores e identificación de cuellos de botella — no el `tensor_sequencias` directamente.

Cada fila representa un par de antenas consecutivas (origen → destino) observado en los trayectos de los suscriptores. Incluye el volumen de usuarios, el número de transiciones y el porcentaje de flujo de la antena de origen que va hacia esa antena de destino.

| **Atributo** | **Valor** |
|---|---|
| Filas | ~15.000 pares de antenas |
| Tamaño CSV | ~2,6 MB |
| Granularidad | par de antenas consecutivas (`ecgi_origem`, `ecgi_destino`) |
| Uso primario | Visualización de vías · carga de corredores · cuellos de botella |

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `ecgi_origem` | STRING(12) | Antena de origen del desplazamiento. Tratar como string. |
| `lat_origem` | FLOAT(10,6) | Latitud de la antena de origen. |
| `lon_origem` | FLOAT(10,6) | Longitud de la antena de origen. |
| `cluster_origem` | STRING(40) | Zona geográfica de origen. |
| `municipio_origem` | STRING(60) | Municipio de origen. |
| `ecgi_destino` | STRING(12) | Antena de destino del desplazamiento. Tratar como string. |
| `lat_destino` | FLOAT(10,6) | Latitud de la antena de destino. |
| `lon_destino` | FLOAT(10,6) | Longitud de la antena de destino. |
| `cluster_destino` | STRING(40) | Zona geográfica de destino. |
| `municipio_destino` | STRING(60) | Municipio de destino. |
| `n_usuarios` | INT32 | Usuarios distintos que realizaron este par de antenas. |
| `n_transicoes` | INT32 | Total de transiciones observadas en este par. |
| `dist_km` | FLOAT(8,3) | Distancia Haversine real entre las dos antenas en km. |
| `periodo_predominante` | STRING(12) | Período del día más frecuente para este par. |
| `pct_do_cluster_origem` | FLOAT(6,1) | % de usuarios de la antena de origen que van hacia esta antena de destino. |

## 7.1 Ejemplo de uso — Top corredores por volumen

```sql
SELECT ecgi_origem, cluster_origem,
       ecgi_destino, cluster_destino,
       n_usuarios, n_transicoes,
       dist_km, pct_do_cluster_origem
FROM tensor_fluxo_vias
ORDER BY n_usuarios DESC
FETCH FIRST 20 ROWS ONLY;
```

## 7.2 Ejemplo de uso — Cuellos de botella: antenas con muchas entradas

```sql
SELECT ecgi_destino, cluster_destino,
       SUM(n_usuarios)    AS total_usuarios_entrada,
       SUM(n_transicoes)  AS total_transicoes,
       COUNT(*)           AS n_origenes_distintos,
       AVG(dist_km)       AS dist_media_km
FROM tensor_fluxo_vias
GROUP BY ecgi_destino, cluster_destino
ORDER BY total_usuarios_entrada DESC
FETCH FIRST 15 ROWS ONLY;
```

## 7.3 Visualización React/Leaflet sugerida

El `tensor_fluxo_vias.csv` es el archivo ideal para la capa de flujos en el mapa. Cada fila se convierte en un segmento de línea entre `(lat_origem, lon_origem)` y `(lat_destino, lon_destino)`, con:

- **Grosor** proporcional a `n_transicoes`
- **Color** en gradiente verde→amarillo→rojo por `n_usuarios`, o por `dist_km` para destacar corredores de larga distancia
- **Popup** con `n_usuarios`, `n_transicoes`, `dist_km`, `pct_do_cluster_origem`

---

# 8. tensor_concentracao.csv — Concentración por Antena

Agrega el `tensor_mobilidade` por (antena, día, período). Archivo ideal para mapas de calor, análisis de picos de tráfico y detección de hotspots.

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `ecgi` | STRING(12) | Identificador de la antena. |
| `cluster` | STRING(40) | Zona geográfica. |
| `municipio` | STRING(60) | Municipio. |
| `day_date` | DATE (ISO) | Fecha del registro. |
| `periodo` | STRING(12) | MADRUGADA / MANHA / TARDE / NOITE. |
| `n_usuarios` | INT32 | Usuarios distintos activos en esa antena/día/período. |
| `n_sessoes` | INT32 | Total de sesiones acumuladas. |
| `download_bytes` | INT64 | Total de bytes descargados. |
| `upload_bytes` | INT64 | Total de bytes enviados. |
| `dur_media_s` | INT32 | Duración promedio por sesión en segundos. |
| `drop_pct_medio` | FLOAT(8,4) | Promedio de la tasa de descarte de paquetes. |
| `congestionamento_medio` | FLOAT(6,3) | Promedio del nivel de congestión. |
| `chamadas_total` | INT32 | Total de llamadas de voz. |
| `mensagens_total` | INT32 | Total de SMS. |
| `lat` | FLOAT(10,6) | Latitud de la antena. |
| `lon` | FLOAT(10,6) | Longitud de la antena. |

---

# 9. tensor_od.csv — Matriz Origen-Destino por Clúster

Pares de desplazamiento agregados entre clústeres de movilidad. Base para construcción de matrices O-D y análisis de flujos entre zonas urbanas.

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `cluster_origem` | STRING(40) | Zona de origen. |
| `municipio_origem` | STRING(60) | Municipio de origen. |
| `lat_origem` | FLOAT(10,6) | Latitud del centroide de origen. |
| `lon_origem` | FLOAT(10,6) | Longitud del centroide de origen. |
| `cluster_destino` | STRING(40) | Zona de destino. |
| `municipio_destino` | STRING(60) | Municipio de destino. |
| `lat_destino` | FLOAT(10,6) | Latitud del centroide de destino. |
| `lon_destino` | FLOAT(10,6) | Longitud del centroide de destino. |
| `mesmo_cluster` | INT8 (0/1) | 1 si origen == destino. |
| `n_usuarios` | INT32 | Usuarios distintos en el par (>= K-anonimato). |
| `n_viagens` | INT32 | Total de viajes observados. |
| `dist_media_km` | FLOAT(8,3) | Distancia Haversine promedio en km. |
| `periodo_predominante` | STRING(12) | Período más frecuente para este par. |

---

# 10. tensor_tempo_deslocamento.csv — Distancias Inter-clúster

Estadísticas de distancia para desplazamientos inter-clúster. Permite calcular tiempos promedio y construir isocronas de accesibilidad.

| **Campo** | **Tipo** | **Descripción** |
|---|---|---|
| `cluster_origem` | STRING(40) | Zona de origen. |
| `cluster_destino` | STRING(40) | Zona de destino. |
| `mesmo_cluster` | INT8 | Siempre 0 en este tensor. |
| `n_observacoes` | INT32 | Número de desplazamientos observados. |
| `dist_media_km` | FLOAT(8,3) | Distancia Haversine promedio en km. |
| `dist_p25_km` | FLOAT(8,3) | Percentil 25 de la distancia. |
| `dist_p75_km` | FLOAT(8,3) | Percentil 75 de la distancia. |
| `periodo_predominante` | STRING(12) | Período más frecuente. |

---

# 11. trajetos_comuns.csv — Pares OD K-Anonimizados

Versión pública y k-anonimizada de los pares Origen-Destino. Esquema idéntico al `tensor_od.csv` con filtro de privacidad K=3 ya aplicado. Recomendado para aplicaciones que necesiten demostrar conformidad con la LGPD.

> **[✓]** Este archivo YA está k-anonimizado (K=3). Puede usarse en aplicaciones públicas sin restricciones adicionales de privacidad.

---

# 12. Clústeres Geográficos — Referencia

Los 27 clústeres representan zonas funcionales de la RM calibradas por densidad poblacional IBGE 2022.

| **Clúster** | **Municipio** | **Lat** | **Lon** | **Perfil** |
|---|---|---|---|---|
| CBD_BEIRAMAR | Florianópolis | -27.5954 | -48.5480 | Centro corporativo |
| CENTRO_HISTORICO | Florianópolis | -27.5970 | -48.5482 | Turismo / servicios |
| TRINDADE | Florianópolis | -27.6011 | -48.5320 | Residencial universitario |
| UFSC | Florianópolis | -27.5969 | -48.5500 | Campus universitario |
| COQUEIROS | Florianópolis | -27.5820 | -48.5700 | Residencial clase A |
| ESTREITO_CAPOEIRAS | Florianópolis | -27.5880 | -48.5850 | Corredor comercial |
| AEROPORTO_HLZ | Florianópolis | -27.6700 | -48.5470 | Aeropuerto / logística |
| CAMPECHE | Florianópolis | -27.6800 | -48.4800 | Expansión sur |
| LAGOA_CONCEICAO | Florianópolis | -27.6050 | -48.4600 | Turismo / ocio |
| JURERE | Florianópolis | -27.4400 | -48.5000 | Alto estándar balneario |
| CANASVIEIRAS | Florianópolis | -27.4250 | -48.4700 | Turismo masivo |
| INGLESES | Florianópolis | -27.4350 | -48.3950 | Residencial norte |
| NORTE_ILHA | Florianópolis | -27.4800 | -48.4500 | Expansión norte |
| RESIDENCIAL_NORTE | Florianópolis | -27.5420 | -48.5000 | Residencial expansión |
| SC401_CORREDOR | Florianópolis | -27.5600 | -48.5180 | Corredor SC-401 |
| SAO_JOSE_CENTRO | São José | -27.6100 | -48.6180 | Centro de São José |
| SAO_JOSE_BARREIROS | São José | -27.6450 | -48.6500 | Residencial sur SJ |
| SAO_JOSE_KOBRASOL | São José | -27.5950 | -48.6300 | Comercio SJ |
| SAO_JOSE_ROCADO | São José | -27.5700 | -48.6500 | Industrial SJ |
| PALHOCA_CENTRO | Palhoça | -27.6450 | -48.6700 | Centro de Palhoça |
| PALHOCA_PEDRA_BRANCA | Palhoça | -27.6250 | -48.6900 | Expansión Palhoça |
| PALHOCA_BR101_SUL | Palhoça | -27.6800 | -48.7000 | Corredor BR-101 Sur |
| BIGUACU_BR101_NORTE | Biguaçu | -27.4950 | -48.6550 | Corredor BR-101 Norte |
| VIA_EXPRESSA_CORREDOR | Florianópolis | -27.6200 | -48.5800 | Vía Expresa |
| SANTO_AMARO | Santo Amaro | -27.7100 | -48.7800 | Interior sur |
| GOV_CELSO_RAMOS | Gov. C. Ramos | -27.3200 | -48.5550 | Litoral norte |
| ANTONIO_CARLOS | Antônio Carlos | -27.5300 | -48.7400 | Hortifrutícola / rural |

---

# 13. Guía de Lectura — Python / pandas

## 13.1 Archivos grandes (streaming)

```python
import pandas as pd

# tensor_mobilidade y tensor_sequencias: siempre en chunks
for chunk in pd.read_csv('tensor_mobilidade.csv',
                          chunksize=500_000,
                          dtype={'ecgi': str, 'assinante_hash': 'int32'}):
    pass

for chunk in pd.read_csv('tensor_sequencias.csv',
                          chunksize=500_000,
                          dtype={'ecgi': str, 'assinante_hash': 'int32'},
                          parse_dates=['arrival_time']):
    pass
```

## 13.2 Archivos pequeños (carga completa)

```python
antenas      = pd.read_csv('antenas_flp.csv', dtype={'ecgi': str})
assinantes   = pd.read_csv('assinantes.csv')
concentracao = pd.read_csv('tensor_concentracao.csv', dtype={'ecgi': str})
od           = pd.read_csv('tensor_od.csv')
fluxo_vias   = pd.read_csv('tensor_fluxo_vias.csv',
                            dtype={'ecgi_origem': str, 'ecgi_destino': str})
```

> **[!] CRÍTICO:** lea siempre las columnas `ecgi`, `ecgi_origem`, `ecgi_destino` como `str`. Pandas las convierte a float64 por defecto y corrompe el identificador.

---

# Anexo A — Consultas SQL Analíticas

Las consultas a continuación son ejemplos para Oracle Database. Se asume que los CSVs fueron cargados en las tablas correspondientes.

> **[i]** Recomendación: cree un esquema individual por equipo (ej: `TEAM01`) y persista los resultados intermedios en tablas de trabajo.

## A.1 Top 10 antenas por usuarios — mañana

```sql
SELECT ecgi, cluster, municipio,
       SUM(n_usuarios)             AS total_usuarios,
       SUM(download_bytes)/1e9     AS download_gb,
       AVG(congestionamento_medio) AS cong_medio
FROM tensor_concentracao
WHERE periodo = 'MANHA'
GROUP BY ecgi, cluster, municipio
ORDER BY total_usuarios DESC
FETCH FIRST 10 ROWS ONLY;
```

## A.2 Matriz O-D completa — flujos inter-clúster

```sql
SELECT cluster_origem, cluster_destino,
       SUM(n_usuarios) AS usuarios, SUM(n_viagens) AS viajes,
       AVG(dist_media_km) AS dist_km
FROM tensor_od
WHERE mesmo_cluster = 0
GROUP BY cluster_origem, cluster_destino
ORDER BY usuarios DESC;
```

## A.3 Top corredores por flujo de antenas [NUEVO]

```sql
SELECT ecgi_origem, cluster_origem,
       ecgi_destino, cluster_destino,
       n_usuarios, n_transicoes,
       dist_km, pct_do_cluster_origem
FROM tensor_fluxo_vias
ORDER BY n_usuarios DESC
FETCH FIRST 20 ROWS ONLY;
```

## A.4 Cuellos de botella: antenas con mayor convergencia de flujo [NUEVO]

```sql
SELECT ecgi_destino, cluster_destino,
       SUM(n_usuarios)   AS total_entrada,
       SUM(n_transicoes) AS total_transicoes,
       COUNT(*)          AS n_origenes
FROM tensor_fluxo_vias
GROUP BY ecgi_destino, cluster_destino
ORDER BY total_entrada DESC
FETCH FIRST 15 ROWS ONLY;
```

## A.5 Trayecto de un suscriptor en un día [NUEVO]

```sql
SELECT seq_num, ecgi, cluster,
       arrival_time, permanencia_seg, distancia_km_anterior
FROM tensor_sequencias
WHERE assinante_hash = 12345
  AND day_date = DATE '2026-03-05'
ORDER BY seq_num;
```

## A.6 Tiempo promedio hasta el Aeropuerto

```sql
SELECT cluster_origem, n_observacoes,
       dist_media_km, dist_p25_km, dist_p75_km
FROM tensor_tempo_deslocamento
WHERE cluster_destino = 'AEROPORTO_HLZ'
ORDER BY dist_media_km ASC;
```

## A.7 Perfil de consumo por rango de ingresos y tecnología

```sql
SELECT a.income_cluster, m.rat_type,
       COUNT(DISTINCT m.assinante_hash) AS usuarios,
       SUM(m.download_bytes)/1e9        AS download_gb,
       AVG(m.drop_pct)                  AS tasa_drop
FROM tensor_mobilidade m
JOIN assinantes a ON a.assinante_hash = m.assinante_hash
GROUP BY a.income_cluster, m.rat_type
ORDER BY a.income_cluster, m.rat_type;
```

## A.8 Flujo de entrada y salida por municipio

```sql
SELECT municipio_destino AS municipio, 'ENTRADA' AS tipo,
       SUM(n_usuarios) AS usuarios
FROM tensor_od
WHERE municipio_origem != municipio_destino
GROUP BY municipio_destino
UNION ALL
SELECT municipio_origem, 'SALIDA', SUM(n_usuarios)
FROM tensor_od
WHERE municipio_origem != municipio_destino
GROUP BY municipio_origem
ORDER BY municipio, tipo;
```

## A.9 Hotspots de congestión

```sql
SELECT cluster, municipio, periodo,
       AVG(congestionamento_medio) AS cong_medio,
       SUM(n_usuarios)             AS usuarios
FROM tensor_concentracao
WHERE congestionamento_medio > 0.6
GROUP BY cluster, municipio, periodo
ORDER BY cong_medio DESC
FETCH FIRST 20 ROWS ONLY;
```

## A.10 Crear tabla de trabajo por equipo

```sql
CREATE TABLE TEAM01.fluxo_corredor_br101 AS
SELECT *
FROM tensor_fluxo_vias
WHERE cluster_origem IN ('BIGUACU_BR101_NORTE','SAO_JOSE_ROCADO',
                         'SAO_JOSE_KOBRASOL','VIA_EXPRESSA_CORREDOR')
   OR cluster_destino IN ('BIGUACU_BR101_NORTE','SAO_JOSE_ROCADO',
                          'SAO_JOSE_KOBRASOL','VIA_EXPRESSA_CORREDOR');

CREATE INDEX idx_fv_orig ON TEAM01.fluxo_corredor_br101(ecgi_origem);
```

---

# Anexo B — Glosario

| **Término** | **Definición** |
|---|---|
| CDR | Call Detail Record — registro de evento de red generado por el operador. |
| ECGI | E-UTRAN Cell Global Identifier — identificador único de celda (MCC+MNC+CellID). |
| ERB | Estação Rádio Base — torre de telecomunicaciones con una o más celdas. |
| K-anonimato | Técnica de privacidad: cada registro es indistinguible de al menos K-1 otros. |
| LGPD | Lei Geral de Proteção de Dados (Ley 13.709/2018). Regula los datos personales en Brasil. |
| NR | New Radio — tecnología 5G (3GPP Release 15+). |
| LTE | Long Term Evolution — tecnología 4G. |
| WCDMA | Wideband CDMA — tecnología 3G. |
| Clúster | Zona geográfica funcional de la RM (27 zonas, calibradas por IBGE 2022). |
| Tensor OD | Origen-Destino — flujos de desplazamiento entre zonas geográficas. |
| Tensor Fluxo Vias | Pares de antenas consecutivas con volumen de usuarios — nuevo en v2. |
| Tensor Sequencias | Secuencia ordenada de antenas por suscriptor/día — nuevo en v2. |
| arrival_time | Timestamp de la primera sesión de datos en la antena en el día. |
| IPDR | IP Detail Record — registro de sesión de datos en redes móviles. |
| CDRView | Plataforma de analytics de Visent para CDR/IPDR a escala carrier class. |
| STEP | Social Telemetry Extensible Platform — módulo CDRView para vectorización de comportamiento. |

---

*Visent · OSX Telecomunicações S/A · Hackathon App BiT · jun/2026 · CONFIDENCIAL*
