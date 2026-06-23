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
Los campos dentro de cada elemento de `datos` son **flexibles y dependen exclusivamente de la consulta** - no hay una estructura fija. El AI Service decide qué campos incluir según la pregunta del usuario.

&gt; **Nota importante sobre `total_registros`**:
&gt; - El **servicio AI NO debe enviar este campo** (el backend lo calcula automáticamente).
&gt; - El backend recibe la respuesta del AI, calcula `total_registros = datos.size()` y lo agrega a la respuesta final que envía al frontend.

---

#### Ejemplo 1: Pregunta sobre BRECHAS DE FORMACIÓN
Pregunta: "¿Dónde faltan programas de formación para jóvenes de bajos ingresos?"
-> **Campos clave**: `programas_activos`, `severidad_brecha` (no `periodo`, no `taxa_internacao_psiquiatrica`)
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

---

#### Ejemplo 2: Pregunta sobre SALUD MENTAL (GENERAL, sin período)
Pregunta: "¿Qué regiones tienen la tasa de internación psiquiátrica más alta?"
-> **Campos clave**: `taxa_internacao_psiquiatrica` (no `periodo`, no `programas_activos`)
```json
{
  "respuesta_ia": "La región FPOLIS_NORTE tiene la tasa de internación psiquiátrica más alta del estado, con 14.2%.",
  "datos": [
    {
      "cluster": "FPOLIS_NORTE",
      "municipio": "Florianópolis",
      "n_usuarios": 8200,
      "taxa_internacao_psiquiatrica": 14.2
    }
  ],
  "fuentes": [
            { "nombre": "DATASUS", "codigo_origem": "SIH-SUS", "fecha_referencia": "2025-12-01" }
        ],
  "visualizacion_sugerida": "mapa_indicadores",
  "idioma": "es"
}
```

---

#### Ejemplo 3: Pregunta sobre SALUD MENTAL (POR PERÍODO DEL DÍA)
Pregunta: "¿Qué período del día tiene más concentración de personas en la región FPOLIS_NORTE?"
-> **Campos clave**: `periodo`, `congestionamento_medio` (no `taxa_internacao_psiquiatrica`, no `programas_activos`)
```json
{
  "respuesta_ia": "En la mañana (MANHA), la región FPOLIS_NORTE tiene la mayor concentración de personas, con 8.200 usuarios y congestión media de 0.68.",
  "datos": [
    {
      "cluster": "FPOLIS_NORTE",
      "periodo": "MANHA",
      "n_usuarios": 8200,
      "congestionamento_medio": 0.68
    }
  ],
  "fuentes": [
            { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10" }
        ],
  "visualizacion_sugerida": "grafico_barras",
  "idioma": "es"
}
```

---

#### Ejemplo 4: Pregunta sobre DATOS BÁSICOS DEL MAPA
Pregunta: "Muestra la concentración de personas y cobertura de red en SAO_JOSE_KOBRASOL"
-> **Campos clave**: `lat`, `lng`, `rat_type_predominante` (nada de salud mental ni programas)
```json
{
  "respuesta_ia": "La región SAO_JOSE_KOBRASOL tiene 12.400 usuarios y cobertura LTE predominante.",
  "datos": [
    {
      "cluster": "SAO_JOSE_KOBRASOL",
      "municipio": "São José",
      "lat": -27.5935,
      "lng": -48.6358,
      "n_usuarios": 12400,
      "congestionamento_medio": 0.72,
      "rat_type_predominante": "LTE"
    }
  ],
  "fuentes": [
            { "nombre": "Vísent CDRView v2", "codigo_origem": "tensor_concentracao", "fecha_referencia": "2026-03-10" }
        ],
  "visualizacion_sugerida": "mapa_indicadores",
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

