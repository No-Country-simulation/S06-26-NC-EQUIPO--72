# Contratos de la AI SERVICE


## POST /consulta


Recibe una consulta en lenguaje natural. El AI Service realiza schema linking (vía embeddings) para identificar las tablas relevantes, genera SQL (Text-to-SQL), lo ejecuta contra la base de datos y retorna una respuesta estructurada con datos, fuentes y sugerencia de visualización.


> **Nota:** el AI Service no recibe filtros estructurados. Toda la inferencia de contexto (municipio, cluster, periodo, categoría, etc.) se hace a partir del texto de la consulta.


### Request
```json
{
  "consulta": "¿Dónde faltan programas de formación para jóvenes de bajos ingresos?",
  "idioma": "es"
}
```


### Response 200
```json
{
  "respuesta_ia": "En la región FPOLIS_NORTE hay 8.200 personas en horario laboral con cobertura WCDMA precaria y ningún programa de formación activo. Es la zona de mayor brecha para jóvenes de income D.",
  "datos": [
    {
      "cluster": "FPOLIS_NORTE",
      "municipio": "Florianópolis",
      "n_usuarios": 8200,
      "congestionamento_medio": 0.81,
      "programas_activos": 0,
      "severidad_brecha": "ALTA"
    }
  ],
  "fuentes": [
            { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10" },
            { "nombre": "DATASUS", "codigo_origem": "SIH-SUS", "fecha_referencia": "2025-12-01" }
        ],
  "visualizacion_sugerida": "mapa_brechas",
  "idioma": "es"
}
```


> `respuesta_ia` (antes `respuesta`) — renombrado para ser consistente con el contrato de `POST /datos` (backend↔frontend), que ya usa este nombre de campo.
>
> `visualizacion_sugerida` es una señal para el frontend sobre qué componente renderizar. Valores posibles: `mapa_brechas` / `mapa_indicadores` / `tabla_datos` / `grafico_barras`. El frontend decide si la usa o no.


### Response 422
```json
{
  "error": "CONSULTA_IRRELEVANTE",
  "mensaje": "La consulta no puede resolverse con los datos disponibles."
}
```


> Aplica cuando el SQL generado no devuelve resultados, o cuando el agente determina que la consulta no puede resolverse con el schema disponible.


Historial de conversación: Pendiente por definir

