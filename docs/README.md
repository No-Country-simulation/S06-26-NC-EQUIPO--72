## Resumen de cobertura - Endpoints por servicio

| Servicio | Endpoints |
| --------- | --------- |
| **Formaciones** | `GET /mapa/indicadores?categoria=EDUCACION`<br>`GET /programas?tipo=FORMACION`<br>`GET /brechas?servicio=FORMACION` |
| **Empleabilidad** | `POST /datos` (agente IA — contexto vía `filtros.categoria=EMPLEO`)<br>`GET /brechas?servicio=EMPLEO` |
| **Experiencias estructurantes** | `GET /programas?tipo=EXPERIENCIA`<br>`POST /programas` / `PUT /programas/:id` / `DELETE /programas/:id` |
| **Mentorías** | `GET /programas?tipo=MENTORIA`<br>`GET /brechas?servicio=MENTORIA`<br>`POST /programas` / `PUT /programas/:id` / `DELETE /programas/:id` |
| **Salud Mental** | `GET /mapa/indicadores?categoria=SALUD_MENTAL`<br>`GET /brechas?servicio=SALUD_MENTAL` |

---

# Pipeline de ingestión - Vísent CDRView

El dataset **Vísent** es el núcleo del producto. Antes de levantar el servidor, los CSVs deben estar cargados en la DB.

El orden importa por las FKs:

| Orden | Archivo | Tabla |
| ------ | ---------------------- | ---------------------- |
| 1 | `antenas.csv` | `antenas` |
| 2 | `assinantes.csv` | `assinantes` |
| 3 | `tensor_concentracao` | `concentracao` |
| 4 | `tensor_mobilidade` | `mobilidade_agregada` *(chunks de 500k filas)* |
| 5 | `tensor_od` | `flujo_od` |
| 6 | `tensor_fluxo_vias` | `fluxo_vias` |

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

---

# Seeder de `indicadores_territoriales` - MVP vs Producción

`indicadores_territoriales` es la capa que unifica datos externos (salud mental, empleo y educación) con el mismo formato, independientemente de la fuente.

## MVP - Seeder CSV con datos mock

- `fonte = 'MOCK'`
- Estructura idéntica a producción
- Se carga una vez antes de levantar el servidor

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
