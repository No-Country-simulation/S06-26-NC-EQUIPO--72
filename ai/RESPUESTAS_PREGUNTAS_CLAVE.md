# Respuestas Directas a las 3 Preguntas Clave del Desafío

---

## Introducción
Este análisis usa el **dataset CDRView** para responder las preguntas clave del proyecto. Se incluyen:
- Resultados concretos del dataset
- Limitaciones del dataset
- Datos externos que complementan la información

---

---

## Pregunta 1: ¿Dónde hay concentración de personas pero cobertura de red precaria?

### Criterios usados:
| Criterio | Valor |
|----------|-------|
| Alta concentración | ≥ 1,839 usuarios (percentil 60) |
| Congestión alta | ≥ 0.3503 (percentil 70) |
| Drop alto | ≥ 0.0686 (percentil 70) |
| Tecnología precaria | WCDMA (3G) predominante |

### Zonas Prioritarias Encontradas (7):
| Cluster               | Municipio     | Usuarios Promedio | Congestión Promedio | Drop Promedio | Tecnología Predominante |
|-----------------------|---------------|-------------------|---------------------|---------------|------------------------|
| CENTRO_HISTORICO      | Florianopolis | 4,104.07          | 0.3498              | 0.0686        | LTE                    |
| SAO_JOSE_BARREIROS    | Palhoca       | 3,404.55          | 0.3506              | 0.0686        | LTE                    |
| COQUEIROS             | Florianopolis | 3,346.88          | 0.3504              | 0.0686        | LTE                    |
| PALHOCA_CENTRO        | Palhoca       | 3,077.32          | 0.3506              | 0.0688        | LTE                    |
| SAO_JOSE_CENTRO       | Sao Jose      | 2,951.19          | 0.3498              | 0.0687        | LTE                    |
| PALHOCA_PEDRA_BRANCA  | Palhoca       | 2,239.39          | 0.3505              | 0.0687        | LTE                    |
| TRINDADE              | Florianopolis | 1,873.69          | 0.3504              | 0.0685        | LTE                    |


---

## Pregunta 2: ¿Qué regiones tienen más personas en horario laboral pero menos empleo formal registrado?

### Limitación clave del dataset:
**NO hay datos de empleo formal en el CDRView**. El dataset solo muestra **concentración de personas en horario laboral**.

### TOP 15 Zonas con Mayor Concentración en Horario Laboral (MANHA + TARDE):
| Cluster               | Municipio     | Usuarios Promedio | Máximo Usuarios |
|-----------------------|---------------|-------------------|-----------------|
| CENTRO_HISTORICO      | Florianopolis | 4,923.10          | 5,929           |
| SAO_JOSE_BARREIROS    | Palhoca       | 4,077.87          | 4,957           |
| COQUEIROS             | Florianopolis | 4,011.13          | 4,836           |
| PALHOCA_CENTRO        | Palhoca       | 3,670.60          | 4,432           |
| SAO_JOSE_CENTRO       | Sao Jose      | 3,513.12          | 4,233           |
| PALHOCA_PEDRA_BRANCA  | Palhoca       | 2,672.58          | 3,268           |
| UFSC                  | Florianopolis | 2,298.31          | 2,852           |
| TRINDADE              | Florianopolis | 2,236.56          | 2,749           |
| BIGUACU_BR101_NORTE   | Biguacu       | 2,205.18          | 2,747           |
| CBD_BEIRAMAR          | Florianopolis | 2,198.97          | 2,746           |
| CANASVIEIRAS          | Florianopolis | 2,192.13          | 2,656           |
| RESIDENCIAL_NORTE     | Florianopolis | 2,067.03          | 2,582           |
| VIA_EXPRESSA_CORREDOR | Florianopolis | 2,048.37          | 2,502           |
| SAO_JOSE_KOBRASOL     | Sao Jose      | 1,884.73          | 2,328           |
| CAMPECHE              | Florianopolis | 1,867.82          | 2,336           |

### Datos Externos Necesarios para Completar la Respuesta:
Para encontrar zonas con **alta concentración laboral pero bajo empleo formal**, necesitas combinar estos datos con:
1. **Censo Económico (IBGE)**: Tasa de empleo formal por zona
2. **Registro Nacional de Empresas (CNPJ)**: Densidad de empresas formales
3. **Seguro de Desempleo**: Datos de personas en desempleo formal
4. **Encuestas de Hogares**: Ingresos y situación laboral

---

## Pregunta 3: ¿Dónde falta infraestructura de conectividad antes de que lleguen los programas sociales?

### Zonas Prioritarias (mismas que la pregunta 1, ordenadas por necesidad):
1. **CENTRO_HISTORICO** (Florianopolis)
2. **SAO_JOSE_BARREIROS** (Palhoca)
3. **COQUEIROS** (Florianopolis)
4. **PALHOCA_CENTRO** (Palhoca)
5. **SAO_JOSE_CENTRO** (Sao Jose)
6. **PALHOCA_PEDRA_BRANCA** (Palhoca)
7. **TRINDADE** (Florianopolis)


---

## Conclusión Final

| Pregunta | ¿Se puede responder con el dataset? | Detalle |
|----------|-------------------------------------|---------|
| 1        |  Sí, completamente | El dataset tiene todos los datos necesarios |
| 2        |  Parcialmente | Tiene concentración laboral, pero necesita datos externos de empleo formal |
| 3        |  Sí, completamente | Se pueden priorizar zonas usando la pregunta 1 como base |

---

## Archivos Generados
1. **`data_resultado/zonas_prioritarias_pregunta1.csv`**: Zonas con alta concentración y mala cobertura
2. **`data_resultado/concentracion_laboral_pregunta2.csv`**: Concentración en horario laboral por cluster
3. **`data_resultado/zonas_programas_sociales_pregunta3.csv`**: Zonas prioritarias para programas sociales