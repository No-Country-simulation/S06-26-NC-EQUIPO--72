# Contratos de la API

> Son recomendaciones. Backend y frontend pueden acordar una versión modificada del contrato.
> Este documento describe los endpoints del **backend** consumidos por el frontend.

## GET /regiones

Catálogo de clusters disponibles. Pobla los filtros del frontend.

### Response `200`

``` json
{
  "regiones": [
    {
      "cluster": "SAO_JOSE_KOBRASOL",
      "municipio": "São José",
      "lat_centroide": -27.5935,
      "lon_centroide": -48.6358,
      "n_antenas": 7
    }
  ]
}
```

------------------------------------------------------------------------

## GET /mapa

Concentración de personas y cobertura de red por región.

### Query Params

  Parámetro     Tipo                   Requerido  Valor por defecto
  ------------- --------------------- ----------- -----------------------
  `periodo`     `string`                  No      `TARDE`
  `municipio`   `string`                  No      `todos`
  `fecha`       `DATE (YYYY-MM-DD)`       No      último día disponible

### Response `200`

``` json
{
  "regiones": [
    {
      "cluster": "SAO_JOSE_KOBRASOL",
      "municipio": "São José",
      "lat": -27.5935,
      "lon": -48.6358,
      "n_usuarios": 12400,
      "congestionamento_medio": 0.72,
      "rat_type_predominante": "LTE",
      "download_gb": 34.5,
      "periodo": "TARDE",
      "fecha": "2026-03-10"
    }
  ]
}
```

------------------------------------------------------------------------

## GET /mapa/indicadores

Extiende `/mapa` con capas de indicadores territoriales.

### Query Params


| Parámetro   | Tipo     | Requerido | Descripción |
| ------------| -------- | :-------: | ----------- |
| `categoria` | `string` | Sí | `SALUD_MENTAL` / `EMPLEO` / `EDUCACION` |
| `indicador` | `string` | No | Filtra un indicador específico |
| `municipio` | `string` | No | - |

### Response `200`

``` json
{
  "regiones": [
    {
      "cluster": "SAO_JOSE_KOBRASOL",
      "municipio": "São José",
      "lat": -27.5935,
      "lon": -48.6358,
      "n_usuarios": 12400,
      "congestionamento_medio": 0.72,
      "indicadores": [
        {
          "categoria": "SALUD_MENTAL",
          "indicador": "taxa_internacao_psiquiatrica",
          "valor": 14.2,
          "unidad": "porcentaje",
          "fonte": "DATASUS",
          "fecha_referencia": "2025-12-01"
        }
      ]
    }
  ]
}
```

------------------------------------------------------------------------

## POST /datos

Endpoint principal consumido por el frontend. El backend busca contexto en la DB con los filtros recibidos, luego delega al AI Service (`POST /consulta`) que usa ese contexto + tools propias para generar la respuesta.

> **Flujo interno:** el backend consulta la DB con los `filtros` para construir contexto, luego llama al AI Service (`POST /consulta`) pasando ese contexto. El AI Service puede usar tools propias para complementar la respuesta. El frontend no interactúa con el AI Service directamente.

| Campo                     | Tipo     | Requerido | Default                 | Descripción                                                                                         |
| -------------------------- | -------- | --------- | ----------------------- | --------------------------------------------------------------------------------------------------- |
| `consulta`                 | `string` | No        | -                       | Pregunta en lenguaje natural. Si se envía, el response incluye `respuesta_ia` y `visualizacion_sugerida`. |
| `filtros.municipio`        | `string` | **Sí**    | -                       | Sin esto el backend no sabe contra qué datos buscar contexto.                                       |
| `filtros.cluster`          | `string` | No        | `todos`                 | Afina dentro del municipio.                                                                         |
| `filtros.periodo`          | `string` | No        | `TARDE`                 | Valores posibles: `MADRUGADA`, `MANHA`, `TARDE`, `NOITE`.                                           |
| `filtros.fecha_desde`      | `DATE`   | No        | `últimos 15 días`       | -                                                                                                   |
| `filtros.fecha_hasta`      | `DATE`   | No        | `último día disponible` | -                                                                                                   |
| `filtros.income_cluster`   | `string` | No        | `todos`                 | Valores posibles: `A`, `B`, `C`, `D`. Solo aplica a `mobilidade_agregada`.                         |
| `filtros.categoria`        | `string` | No        | `todas`                 | Valores posibles: `SALUD_MENTAL`, `EMPLEO`, `EDUCACION`. Determina qué trae de `indicadores_territoriales`. |
| `indicadores`              | `string[]` | No      | `todos`                 | Métricas específicas a incluir en el contexto del agente. Útil para reducir tokens.               |
| `idioma`                   | `string` | No        | `es`                    | Idioma de la respuesta del agente. En el MVP el backend puede hardcodearlo.                        |

### Request
```json
{
  "consulta": "¿Dónde faltan programas de formación para jóvenes de bajos ingresos?",
  "filtros": {
    "municipio": "São José",
    "cluster": "SAO_JOSE_KOBRASOL",
    "periodo": "MANHA",
    "fecha_desde": "2026-03-01",
    "fecha_hasta": "2026-03-15",
    "income_cluster": "D",
    "categoria": "SALUD_MENTAL"
  },
  "indicadores": ["n_usuarios", "congestionamento_medio", "taxa_internacao_psiquiatrica"],
  "idioma": "es"
}
```




### Response
```json
{
  "respuesta_ia": "En SAO_JOSE_KOBRASOL hay 8.200 personas con cobertura WCDMA precaria y ningún programa activo.",
  "visualizacion_sugerida": "mapa_brechas",
  "datos": [
    {
      "cluster": "SAO_JOSE_KOBRASOL",
      "periodo": "MANHA",
      "n_usuarios": 8200,
      "congestionamento_medio": 0.68,
      "taxa_internacao_psiquiatrica": 14.2
    }
  ],
  "fuentes": [
    { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10" },
    { "nombre": "DATASUS", "codigo_origem": "SIH-SUS", "fecha_referencia": "2025-12-01" }
  ],
  "total_registros": 1,
  "idioma": "es"
}
```

### Response `400` - municipio ausente

```json
{
  "error": "FILTRO_REQUERIDO",
  "mensaje": "El campo 'filtros.municipio' es obligatorio."
}
```

### Response `422` - consulta irrelevante

> Solo aplica cuando se envió `consulta`. El backend intercepta el 422 del AI Service y lo reenvía al frontend con este formato.

```json
{
  "error": "CONSULTA_IRRELEVANTE",
  "mensaje": "La consulta no puede resolverse con los datos disponibles."
}
```
------------------------------------------------------------------------

## GET /brechas

Cruza datos Vísent con indicadores_territoriales y programas_sociales para identificar zonas con demanda sin oferta.El agente  IA lo consume directamente para responder preguntas como "dónde faltan programas de mentoría?" sin encadenar múltiples llamadas a /datos

> **Nota:** el parámetro `servicio` en `/brechas` y `categoria` en `/mapa/indicadores` comparten los mismos valores (`SALUD_MENTAL` / `EMPLEO` / `EDUCACION`). Son nombres distintos porque representan conceptos distintos: `categoria` refiere al tipo de indicador territorial, `servicio` refiere al servicio social que el agente analiza para detectar brechas.

### Query Params

| Parámetro   | Tipo     | Requerido | Descripción |
| ------------| -------- | :-------: | ----------- |
| `servicio`  | `string` | Sí | `SALUD_MENTAL` / `MENTORIA` / `EXPERIENCIA` / `FORMACION` / `EMPLEO` |
| `municipio` | `string` | No | Filtra por municipio |
| `periodo`   | `string` | No | Default: `TARDE` |
| `income_cluster` | `string` | No | `todos` | `A` / `B` / `C` / `D`. Filtra por segmento de ingresos en `mobilidade_agregada`. |

### Response `200`

``` json
{
  "brechas": [
    {
      "cluster": "BIGUACU_BR101_NORTE",
      "municipio": "Biguaçu",
      "n_usuarios": 9800,
      "congestionamento_medio": 0.81,
      "rat_type_predominante": "WCDMA",
      "indicador_social": {
        "categoria": "SALUD_MENTAL",
        "indicador": "taxa_internacao_psiquiatrica",
        "valor": 17.4,
        "unidad": "porcentaje"
      },
      "programas_activos": 0,
      "severidad_brecha": "ALTA"
    }
  ],
  "criterio": {
    "servicio": "SALUD_MENTAL",
    "logica": "congestionamento_medio > 0.6 AND programas_activos = 0",
    "umbral_congestionamento": 0.6
  }
}
```

> `severidad_brecha` combina concentración de personas + calidad de red + ausencia de programas. El umbral `congestionamento_medio` > 0.6 es el valor default - puede ajustarse por configuración del backend.

------------------------------------------------------------------------

## GET /programas

### Query Params

| Parámetro   | Tipo      | Requerido | Descripción |
| ------------| --------- | :-------: | ----------- |
| `tipo`      | `string`  | No | `FORMACION` / `MENTORIA` / `EXPERIENCIA` |
| `municipio` | `string`  | No | - |
| `cluster`   | `string`  | No | - |
| `activo`    | `boolean` | No | Default: `true` |

### Response `200`

``` json
{
  "programas": [
    {
      "id": 1,
      "nombre": "Jóvenes Tech Norte",
      "tipo": "FORMACION",
      "municipio": "Florianópolis",
      "cluster": "FPOLIS_NORTE",
      "organizacion": "Prefeitura Municipal",
      "lider_referente": null,
      "replicable": null,
      "impacto_estimado": "ALTO",
      "fecha_inicio": "2026-01-15",
      "fecha_fin": null,
      "activo": true
    }
  ],
  "total": 1
}
```

------------------------------------------------------------------------

## POST /programas

### Request

``` json
{
  "nombre": "Mentoría Digital Norte",
  "tipo": "MENTORIA",
  "descripcion": "Programa de mentoría para jóvenes de 18-24 en zona norte",
  "municipio": "Florianópolis",
  "cluster": "FPOLIS_NORTE",
  "organizacion": "Secretaria Municipal de Educação",
  "lider_referente": "María González",
  "replicable": 1,
  "impacto_estimado": "MEDIO",
  "url_referencia": "https://prefeitura.florianopolis.sc.gov.br/mentoria",
  "fecha_inicio": "2026-07-01",
  "fecha_fin": null
}
```

### Response `201`

``` json
{
  "id": 42,
  "mensaje": "Programa registrado correctamente."
}
```

------------------------------------------------------------------------

## PUT /programas/:id

Edición de un programa existente. Todos los campos son opcionales, solo se actualizan los enviados.

### Request
```json
{
  "impacto_estimado": "ALTO",
  "fecha_fin": "2026-12-31"
}
```

### Response `200`
```json
{
  "id": 42,
  "mensaje": "Programa actualizado correctamente."
}
```

### Response `404`
```json
{
  "error": "PROGRAMA_NO_ENCONTRADO",
  "mensaje": "No existe un programa con el id indicado."
}
```

------------------------------------------------------------------------

## DELETE /programas/:id

Desactiva un programa.

### Response `200`

``` json
{
  "id": 42,
  "mensaje": "Programa desactivado correctamente."
}
```


### Response `404`

``` json
{
  "error": "PROGRAMA_NO_ENCONTRADO",
  "mensaje": "No existe un programa con el id indicado."
}
```

------------------------------------------------------------------------

## GET /alertas (opcional)
Alertas automáticas cuando un indicador supera o cae por debajo de un umbral configurable. Corresponde a la funcionalidad opcional definida en el proyecto.

### Query Params

| Parámetro    | Tipo     | Requerido | Descripción |
| ------------ | -------- | :-------: | ----------- |
| `indicador`  | `string` | Sí | - |
| `umbral`     | `number` | Sí | - |
| `comparador` | `string` | No | `LT` / `GT` (Default: `LT`) |

### Response `200`

``` json
{
  "alertas": [
    {
      "cluster": "BIGUACU_BR101_NORTE",
      "municipio": "Biguaçu",
      "indicador": "congestionamento_medio",
      "valor_actual": 0.82,
      "umbral": 0.7,
      "severidad": "ALTA"
    }
  ]
}
```

### Response `200`

``` json
{
  "alertas": [],
  "mensaje": "No se encontraron alertas para los criterios dados."
}
```


------------------------------------------------------------------------

# Pendientes (fuera del MVP)

- Exportación PDF
- Gestión de indicadores territoriales (carga manual por el gestor)
- Soporte multilingüe
- `agrupar_por` en `POST /datos`
- Historial de conversación en el AI Service (stateful vs stateless - pendiente de decisión de arquitectura)
- ETL por fuente para `indicadores_territoriales` (DATASUS / IBGE / OMS) - en MVP se usa seeder mock
- `tensor_sequencias` en el pipeline - coordinar con Jonathan si el front incorpora trayectos individuales en el mapa (fuera del scope actual)
- `GET /alertas` - funcionalidad opcional, no incluida en el MVP

# Errores generales

## Response `400` - filtro con valor inválido
```json
{
  "error": "FILTRO_INVALIDO",
  "mensaje": "El valor de 'periodo' debe ser MADRUGADA / MANHA / TARDE / NOITE."
}
```

## Response `400` - campo obligatorio ausente
```json
{
  "error": "FILTRO_REQUERIDO",
  "mensaje": "El campo 'filtros.municipio' es obligatorio."
}
```

## Response `404` - sin resultados
```json
{
  "error": "SIN_RESULTADOS",
  "mensaje": "No se encontraron datos para los filtros aplicados."
}
```

## Response `500` - error interno
```json
{
  "error": "ERROR_INTERNO",
  "mensaje": "Error al procesar la consulta."
}
```
