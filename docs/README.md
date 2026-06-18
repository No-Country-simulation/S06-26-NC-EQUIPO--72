## Resumen de cobertura - Endpoints por servicio

| Servicio | Endpoints |
| --------- | --------- |
| **Formaciones** | `GET /mapa/indicadores?categoria=EDUCACION`<br>`GET /programas?tipo=FORMACION`<br>`GET /brechas?servicio=FORMACION` |
| **Empleabilidad** | `POST /datos` (agente IA — interpreta la consulta en lenguaje natural vía Text-to-SQL, sin filtros explícitos del frontend)<br>`GET /brechas?servicio=EMPLEO` |
| **Experiencias estructurantes** | `GET /programas?tipo=EXPERIENCIA`<br>`POST /programas` / `PUT /programas/:id` / `DELETE /programas/:id` |
| **Mentorías** | `GET /programas?tipo=MENTORIA`<br>`GET /brechas?servicio=MENTORIA`<br>`POST /programas` / `PUT /programas/:id` / `DELETE /programas/:id` |
| **Salud Mental** | `GET /mapa/indicadores?categoria=SALUD_MENTAL`<br>`GET /brechas?servicio=SALUD_MENTAL` |

---
> `POST /datos` es el endpoint del agente IA. Aparece listado en Empleabilidad porque es el servicio piloto del MVP, pero el agente puede resolver consultas en lenguaje natural sobre cualquiera de los 5 servicios usando sus tools (`GET /brechas`, `GET /mapa`, `GET /programas`, etc.).


# Pipeline de ingestión - Vísent CDRView

El dataset **Vísent** es el núcleo del producto. Antes de levantar el servidor, los CSVs deben estar cargados en la DB.

El orden importa por las FKs:

| Orden | Archivo CSV | Tabla |
| ------ | ---------------------- | ---------------------- |
| 1 | `antenas_flp.csv` | `antenas` |
| 2 | `assinantes.csv` | `assinantes` |
| 3 | `tensor_concentracao.csv` | `concentracao` |
| 4 | `tensor_mobilidade.csv` | `mobilidade_agregada` *(chunks de 500k filas)* |
| 5 | `tensor_od.csv` | `flujo_od` |
| 6 | `tensor_fluxo_vias.csv` | `fluxo_vias` |

> **Importante**
>
> `ecgi`, `ecgi_origem` y `ecgi_destino` deben leerse siempre como `string`.
>
> NOTA: Pandas los convierte a `float64` por defecto y corrompe el identificador.

> **Nota**
>
> `tensor_mobilidade` pesa aproximadamente **2.7 GB**. Leer siempre en **chunks de 500k filas**. Ver ejemplo en `README_DATASET.md`.

> **Fuera del alcance del MVP**
>
> `tensor_sequencias` no se ingesta, ya que opera a nivel de suscriptor individual, granularidad que ninguno de los 5 servicios necesita.

> **Otros archivos del dataset no incluidos en el MVP**
>
> - `sumario_kanon.csv`: es metadata de auditoría de k-anonimato (parámetros K, cobertura, pares OD), no un dataset de registros. No requiere tabla destino.
> - `trajetos_comuns.csv`: esquema redundante con `tensor_od.csv` para este caso de uso (misma información, ya k-anonimizada). No se ingesta por duplicidad.
> - `tensor_tempo_deslocamento.csv`: ninguno de los 5 servicios del MVP requiere tiempos/isocronas de desplazamiento entre zonas. Queda fuera de alcance.

---

## Orden completo para preparar el entorno

1. Pipeline Vísent (6 archivos en el orden de la tabla anterior)
2. Seeder de `indicadores_territoriales` (ver sección siguiente)
3. Levantar el servidor

---

# Seeder de `indicadores_territoriales` - MVP vs Producción

`indicadores_territoriales` es la capa que unifica datos externos (salud mental, empleo y educación) con el mismo formato, independientemente de la fuente.

## MVP - Seeder CSV con datos mock

- `fonte = 'MOCK'`
- Estructura idéntica a producción
- Se carga una vez antes de levantar el servidor
- **El seeder debe ser idempotente:** ejecutarlo más de una vez no debe duplicar registros. Implementar con `INSERT ... ON CONFLICT DO NOTHING` o equivalente según el motor de DB.

## Producción - ETL por fuente

Cada fuente tiene una estructura distinta. El ETL la normaliza al formato de `indicadores_territoriales`.

### DATASUS (SIH-SUS)

```text
internacoes_psiquiatricas / municipio / ano
        ↓ ETL
categoria = SALUD_MENTAL
indicador = taxa_internacao_psiquiatrica
fonte = DATASUS
codigo_origem = SIH-SUS
```

### IBGE (PNAD Contínua)

```text
taxa_emprego / municipio / ano
        ↓ ETL
categoria = EMPLEO
indicador = taxa_emprego_formal
fonte = IBGE
codigo_origem = PNAD
```

### OMS (GHO)

```text
internet_access / country / year
        ↓ ETL
categoria = EDUCACION
indicador = acceso_internet
fonte = OMS
codigo_origem = GHO
```

El backend y la IA no cambian entre MVP y producción. Solo cambia quién alimenta la tabla: **seeder CSV en el MVP, ETL programado en producción**.
