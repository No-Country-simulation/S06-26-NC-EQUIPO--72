package com.example.appbitb2g.dto.responseDTO.employability;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

//  Representa una fuente de datos en las respuestas
@Schema(description = "Fuente de datos citada en la respuesta de IA")
public record FountainDTO(
    @Schema(description = "Nombre de la fuente", example = "IBGE")
    @JsonProperty("nombre") String nombre,
    @Schema(description = "Código de origen", example = "ibge_2025")
    @JsonProperty("codigo_origem") String codigoOrigem,
    @Schema(description = "Fecha de referencia", example = "2025-12-01")
    @JsonProperty("fecha_referencia") String fechaReferencia
) {}
