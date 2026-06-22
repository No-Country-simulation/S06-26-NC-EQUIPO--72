# Contratos de la AI SERVICE


## POST /consulta


Recibe una consulta en lenguaje natural. El AI Service sigue esta regla de prioridad para obtener datos:
1. **Primero**: Usa tools para llamar a endpoints existentes del backend (como `/api/brechas`, `/api/mapa`, `/api/programas`)
2. **Solo si no hay alternativa**: Realiza schema linking (vía embeddings) para identificar las tablas relevantes, genera SQL (Text-to-SQL) y lo ejecuta contra la base de datos (solo lectura)

Finalmente, retorna una respuesta estructurada con datos, fuentes y sugerencia de visualización.





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



> `visualizacion_sugerida` es una señal para el frontend sobre qué componente renderizar. Valores posibles: `mapa_brechas` / `mapa_indicadores` / `tabla_datos` / `grafico_barras`. El frontend decide si la usa o no.


### Response 422
```json
{
  "error": "CONSULTA_IRRELEVANTE",
  "mensaje": "La consulta no puede resolverse con los datos disponibles."
}
```


>&gt; Aplica cuando:
&gt; 1. El agente determina que la consulta es irrelevante (no relacionada con los datos disponibles)
&gt; 2. Las tools (endpoints del backend) no devuelven resultados
&gt; 3. El SQL generado no devuelve resultados
&gt; 4. El agente determina que la consulta no puede resolverse con el schema disponible


Historial de conversación: Pendiente por definir

---

## Documentación Relacionada
Para más detalles sobre la arquitectura de integración, ver [ARQUITECTURA_IA.md](./ARQUITECTURA_IA.md).

