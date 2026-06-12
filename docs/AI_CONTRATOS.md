# Contratos de la AI SERVICE

## POST /consulta
Recibe una consulta en lenguaje natural y retorna respuesta estructurada con datos, fuentes y sugerencia de visualización.

### Request
```json
{
  "consulta": "¿Dónde faltan programas de formación para jóvenes de bajos ingresos?",
  "filtros": {
    "municipio": "Florianópolis",
    "periodo": "MANHA"
  },
  "idioma": "es"
}
```


### Response 200
```json
{
  "respuesta": "En la región FPOLIS_NORTE hay 8.200 personas en horario laboral con cobertura WCDMA precaria y ningún programa de formación activo. Es la zona de mayor brecha para jóvenes de income D.",
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
    { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao" },
    { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_mobilidade" }
  ],
  "visualizacion_sugerida": "mapa_brechas",
  "idioma": "es"
}
```

> `visualizacion_sugerida` es una señal para el frontend sobre qué componente renderizar. Valores posibles: `mapa_brechas` / `mapa_indicadores` / `tabla_datos` / `grafico_barras`. El frontend decide si la usa o no.


### Response 422
```json
{
  "error": "CONSULTA_IRRELEVANTE",
  "mensaje": "La consulta no puede resolverse con los datos disponibles."
}
```

Historial de conversación: Pendiente por definir
