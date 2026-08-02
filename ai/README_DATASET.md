# App BiT- Base de Datos v2
## CDRView · Región Metropolitana de Florianópolis · jun/2026

---

## Novedades en v2 (08/06/2026)

Se agregaron dos archivos sin modificar los anteriores:

- **tensor_sequencias.csv**- secuencia ordenada de antenas visitadas por cada suscriptor en cada día, con `arrival_time` y distancia recorrida. Permite el análisis de trayectos individuales e identificación de vías urbanas.

- **tensor_fluxo_vias.csv**- pares de antenas consecutivas agregados con volumen de usuarios y porcentaje de flujo. Permite la visualización de corredores e identificación de cuellos de botella en vías.

Los archivos de la v1 (`tensor_mobilidade`, `trajetos_comuns`, etc.) **no fueron modificados**.

---

## Contenido de esta carpeta

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| `CDRView_AppBiT_TechnicalReference.docx` | ~30 KB | **Léalo primero.** Esquema completo, glosario y consultas SQL. |
| `tensor_mobilidade.csv` | ~2,7 GB | Base principal- 16,8M eventos de 200K suscriptores en 15 días. |
| `tensor_sequencias.csv` | ~915 MB | Secuencia de antenas por suscriptor/día con arrival_time. **NUEVO** |
| `bases_hackathon_bit.zip` | ~3 MB | Todos los demás CSVs (ver lista abajo). |

### Contenido de bases_hackathon_bit.zip

| Archivo | Filas | Descripción |
|---------|-------|-------------|
| `antenas_flp.csv` | 132 | ERBs reales de Claro en la RM (fuente: Anatel) |
| `assinantes.csv` | 200.000 | Perfil demográfico de cada suscriptor |
| `tensor_concentracao.csv` | 7.920 | Concentración por antena, día y período |
| `tensor_od.csv` | ~500 | Pares Origen-Destino entre clústeres |
| `tensor_fluxo_vias.csv` | ~15.000 | Pares de antenas consecutivas con flujo. **NUEVO** |
| `tensor_tempo_deslocamento.csv` | ~460 | Distancias entre clústeres |
| `trajetos_comuns.csv` | ~500 | Pares OD k-anonimizados (K=3) |
| `sumario_kanon.csv` | 6 | Informe de conformidad de privacidad |

---

## Cuándo usar cada archivo

| Análisis | Archivo principal |
|----------|------------------|
| Mapa de calor de concentración | `tensor_concentracao.csv` |
| Flujo entre barrios / zonas | `tensor_od.csv` o `trajetos_comuns.csv` |
| Carga en vías y corredores | `tensor_fluxo_vias.csv` |
| Trayecto completo de un suscriptor | `tensor_sequencias.csv` |
| Segmentación demográfica | `assinantes.csv` |
| Análisis de calidad de red | `tensor_mobilidade.csv` |
| Tiempo promedio entre zonas | `tensor_tempo_deslocamento.csv` |

---

## Cómo configurar el entorno

### Python / pandas

```python
import pandas as pd

# Archivos pequeños- cargar completo
antenas      = pd.read_csv("antenas_flp.csv", dtype={"ecgi": str})
assinantes   = pd.read_csv("assinantes.csv")
concentracao = pd.read_csv("tensor_concentracao.csv", dtype={"ecgi": str})
od           = pd.read_csv("tensor_od.csv")
fluxo_vias   = pd.read_csv("tensor_fluxo_vias.csv", dtype={"ecgi_origem": str,
                                                             "ecgi_destino": str})

# Archivos grandes- SIEMPRE en chunks
for chunk in pd.read_csv("tensor_mobilidade.csv",
                          chunksize=500_000,
                          dtype={"ecgi": str, "assinante_hash": "int32"}):
    pass  # su procesamiento

for chunk in pd.read_csv("tensor_sequencias.csv",
                          chunksize=500_000,
                          dtype={"ecgi": str, "assinante_hash": "int32"},
                          parse_dates=["arrival_time"]):
    pass  # su procesamiento
```

> **Atención:** lea siempre las columnas `ecgi`, `ecgi_origem`, `ecgi_destino`
> como `str`. Pandas las convierte a float64 por defecto y corrompe el identificador.

### Oracle SQL

```sql
-- Top corredores por volumen de usuarios
SELECT ecgi_origem, cluster_origem, ecgi_destino, cluster_destino,
       n_usuarios, n_transicoes, dist_km, pct_do_cluster_origem
FROM tensor_fluxo_vias
ORDER BY n_usuarios DESC
FETCH FIRST 20 ROWS ONLY;

-- Secuencia de un suscriptor en un día específico
SELECT seq_num, ecgi, cluster, arrival_time,
       permanencia_seg, distancia_km_anterior
FROM tensor_sequencias
WHERE assinante_hash = 12345
  AND day_date = DATE '2026-03-05'
ORDER BY seq_num;
```

---

## Esquema resumido de los archivos nuevos

### tensor_sequencias.csv

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `assinante_hash` | INT | Identificador del suscriptor |
| `day_date` | DATE | Fecha (YYYY-MM-DD) |
| `seq_num` | INT | Posición en la secuencia del día (1, 2, 3...) |
| `ecgi` | STRING | Antena visitada- tratar siempre como string |
| `cluster` | STRING | Zona geográfica de la antena |
| `municipio` | STRING | Municipio de la antena |
| `lat` | FLOAT | Latitud de la antena |
| `lon` | FLOAT | Longitud de la antena |
| `arrival_time` | DATETIME | Timestamp de la 1ª sesión en la antena (ISO 8601) |
| `permanencia_seg` | INT | Tiempo estimado de permanencia en segundos |
| `periodo_sessao` | STRING | MADRUGADA / MANHA / TARDE / NOITE |
| `distancia_km_anterior` | FLOAT | Distancia Haversine desde la antena anterior (0 en la 1ª) |
| `n_sessoes` | INT | Volumen de sesiones de datos en esa antena en el día |

> `arrival_time` es sintético- generado dentro de la ventana de `periodo_sessao`
> con una distribución que favorece el inicio del período.
> En producción, CDRView lo reemplaza por el timestamp real del primer CDR de la celda.

### tensor_fluxo_vias.csv

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `ecgi_origem` | STRING | Antena de origen del desplazamiento |
| `lat_origem` | FLOAT | Latitud de la antena de origen |
| `lon_origem` | FLOAT | Longitud de la antena de origen |
| `cluster_origem` | STRING | Zona geográfica de origen |
| `municipio_origem` | STRING | Municipio de origen |
| `ecgi_destino` | STRING | Antena de destino del desplazamiento |
| `lat_destino` | FLOAT | Latitud de la antena de destino |
| `lon_destino` | FLOAT | Longitud de la antena de destino |
| `cluster_destino` | STRING | Zona geográfica de destino |
| `municipio_destino` | STRING | Municipio de destino |
| `n_usuarios` | INT | Usuarios distintos que realizaron este par |
| `n_transicoes` | INT | Total de transiciones observadas |
| `dist_km` | FLOAT | Distancia Haversine entre las antenas en km |
| `periodo_predominante` | STRING | Período más frecuente para este par |
| `pct_do_cluster_origem` | FLOAT | % de usuarios de la antena de origen hacia este destino |

---

## Períodos del día

| Código | Horario | Perfil |
|--------|---------|--------|
| `MADRUGADA` | 00h–06h | Uso bajo (8% de los eventos) |
| `MANHA` | 06h–12h | Desplazamiento al trabajo (28%) |
| `TARDE` | 12h–18h | Pico de uso (35%) |
| `NOITE` | 18h–00h | Ocio y streaming (29%) |

---

## Privacidad y K-anonimato

Base generada con **K=3** (datos sintéticos, hackathon).
En producción con datos reales: **K=5 obligatorio** (LGPD Art. 12).
El archivo `sumario_kanon.csv` documenta la conformidad.

---

*Vísent · OSX Telecomunicações S/A · Hackathon App BiT · jun/2026*  
*Alianzas: Wongola · Angola Cables · Oracle · PMI-SP*
