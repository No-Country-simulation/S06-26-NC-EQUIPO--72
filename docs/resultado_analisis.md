# Resultado de Análisis - Dataset Vísent CDRView v2


# Resumen ejecutivo

Se auditaron los 6 archivos del dataset Vísent necesarios para el MVP (`antenas_flp.csv`, `assinantes.csv`, `tensor_concentracao.csv`, `tensor_od.csv`, `tensor_fluxo_vias.csv`, `tensor_mobilidade.csv`) mediante un script de auditoría programática (`analisis.py`).

Se identificaron **4 hallazgos**:

* 3 discrepancias entre la documentación (schema y contratos) y los datos reales.
* 1 anomalía de datos confirmada con causa raíz identificada.

> **Nota:** `tensor_sequencias.csv` no fue auditado por decisión de scope, ya que no aporta valor a los 5 servicios del MVP, que operan a nivel de zona y no de trayecto individual.

---

# Volúmenes reales por archivo

| Archivo                 | Filas reales | Columnas reales | Estado                                      |
| ----------------------- | -----------: | --------------: | ------------------------------------------- |
| antenas_flp.csv         |          132 |               5 | ✅ Sin anomalías                             |
| assinantes.csv          |      200.000 |               7 | ✅ Sin anomalías                             |
| tensor_concentracao.csv |        7.920 |              16 | ✅ Sin anomalías (requiere transformación)   |
| tensor_od.csv           |          506 |              13 | ⚠️ 44 nulos - causa identificada            |
| tensor_fluxo_vias.csv   |       17.292 |              15 | ✅ Sin anomalías                             |
| tensor_mobilidade.csv   |   16.798.060 |              29 | ✅ Sin anomalías (requiere mapeo de nombres) |

---

# Hallazgo 1 - Discrepancia en cantidad de clusters

El `schema_db.md` documenta:

> "validarse en la capa de aplicación contra los 27 clusters válidos"

(en `programas_sociales` e `indicadores_territoriales`).

La auditoría real de `antenas_flp.csv` (132 antenas) muestra **23 clusters únicos**, no 27:

```
SC401_CORREDOR
ESTREITO_CAPOEIRAS
NORTE_ILHA
TRINDADE
UFSC
CANASVIEIRAS
AEROPORTO_HLZ
CBD_BEIRAMAR
RESIDENCIAL_NORTE
SAO_JOSE_KOBRASOL
LAGOA_CONCEICAO
CAMPECHE
SAO_JOSE_CENTRO
PALHOCA_PEDRA_BRANCA
SAO_JOSE_ROÇADO
INGLESES
VIA_EXPRESSA_CORREDOR
COQUEIROS
BIGUACU_BR101_NORTE
JURERE
PALHOCA_CENTRO
SAO_JOSE_BARREIROS
CENTRO_HISTORICO
```

Distribuidos en **4 municipios**:

* Florianopolis
* Sao Jose
* Palhoca
* Biguacu

## Acción requerida

- [x] Corregir el número en `schema_db.md`

---



# Hallazgo 2 - Inconsistencia de acentos entre contratos y datos reales

Los ejemplos en `API_CONTRATOS.md` utilizan:

* São José
* Biguaçu

Los datos reales en `antenas_flp.csv` contienen:

* Sao Jose
* Biguacu

## Impacto

Si el backend realiza comparación exacta:

```sql
WHERE municipio = 'São José'
```

nunca coincidirá con los datos reales.

## Acción requerida

Decisión de equipo:

* normalizar acentos durante la ingestión (agregar tildes/cedillas), o
* implementar matching insensible a acentos en los filtros del backend.

---

# Hallazgo 3 - Columnas descartables en tensor_mobilidade.csv

El CSV posee **29 columnas** y se comtemplaban **12 columnas**.
Se descartan las siguientes columnas para el MVP:

```
chamadas
conversacao_seg
completamento_voz
cong_voz
mensagens
completamento_sms
cong_sms
upload_bytes
dur_total_s
rg_streaming
rg_game
rg_social
rg_comunicacao
rg_outros
rg_type
flag_flagship
```

## Justificación

Estas columnas representan métricas de:

* voz
* SMS
* tipo de tráfico de datos

Podrían utilizarse como proxy indirecto de empleabilidad o uso (por ejemplo, `rg_comunicacao` alto en horario laboral).

Sin embargo, el proyecto ya resuelve esa necesidad mediante datos oficiales (`indicadores_territoriales` provenientes de IBGE, DATASUS y OMS), que resultan más confiables que un proxy inferido de patrones de uso móvil.

## Conclusión

El schema actual de `mobilidade_agregada` está correctamente dimensionado y no requiere ampliaciones.

---

# Hallazgo 4 - Dato corrupto confirmado en tensor_od.csv

## Síntoma inicial

* 22 valores nulos en `municipio_origem`
* 22 valores nulos en `municipio_destino`

Total:

**44 valores nulos sobre 506 filas.**

## Análisis realizado

### Distribución de `mesmo_cluster`

```
{0: 44}
```

Descarta la hipótesis de que el problema corresponda a pares del mismo cluster.

### Desglose

* 22 filas con `municipio_origem` nulo
* 22 filas con `municipio_destino` nulo
* 0 filas con ambos nulos simultáneamente

### Patrón identificado

El **100%** de las filas con valores nulos involucran el cluster:

```
SAO_JOSE_ROÇADO
```

como origen o destino.

Verificación:

> Filas con nulo que involucran SAO_JOSE_ROÇADO: **44 de 44**

Además, todas esas filas contienen coordenadas:

```
0.0, 0.0
```

en lugar de valores reales.

## Verificación de causa raíz

Se confirmó que `antenas_flp.csv` sí contiene información correcta para ese cluster:

* 7 antenas registradas
* municipio: `Sao Jose`
* coordenadas reales válidas

Ejemplo:

```
lat = -27.567222
lon = -48.617175
```

Esto descarta que el cluster esté mal definido en el dataset.

## Causa probable

Falla de encoding o lookup durante la generación de `tensor_od.csv` por parte de Vísent, posiblemente relacionada con el carácter especial **ç**, ya que es el único cluster que lo contiene.

## Solución validada

Durante el pipeline de ingestión de `flujo_od`:

* realizar un JOIN contra `antenas.cluster`
* recuperar municipio, latitud y longitud reales de `SAO_JOSE_ROÇADO`
* ignorar los valores `NULL` y `0.0` presentes en el CSV

Esta solución no depende de una corrección del dataset original.

---

# Columnas extra no documentadas

`tensor_od.csv` contiene cinco columnas adicionales:

* lat_origem
* lon_origem
* lat_destino
* lon_destino
* periodo_predominante

No representan una anomalía.

Podrían incorporarse al schema si futuros servicios requieren coordenadas exactas o visualización en mapas.

---

# Transformaciones requeridas para el pipeline de ingestión


| Schema | CSV |
| ------------------------------ | ----------------------------- |
| periodo                        | periodo_sessao                |
| congestionamento_avg           | congestionamento              |
| drop_pct_avg                   | drop_pct                      |



## concentracao

```text
download_gb = download_bytes / 1e9

rat_type_predominante =
    moda(rat_type)
    agrupando tensor_mobilidade
    por (ecgi, day_date, periodo)
```

## mobilidade_agregada

```text
periodo = periodo_sessao

congestionamento_avg = congestionamento

drop_pct_avg = drop_pct

```

## flujo_od

```text
Para cluster_origem o cluster_destino = SAO_JOSE_ROÇADO:

JOIN contra antenas

Recuperar:
- municipio
- lat
- lon

en lugar de insertar los valores NULL / 0.0 del CSV.
```
