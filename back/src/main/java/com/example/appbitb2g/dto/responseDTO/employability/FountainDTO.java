package com.example.appbitb2g.dto.responseDTO.employability;

import com.fasterxml.jackson.annotation.JsonProperty;

//  Representa una fuente de datos en las respuestas
public record FountainDTO(
    @JsonProperty("nombre") String nombre,
    @JsonProperty("codigo_origem") String codigoOrigem,
    @JsonProperty("fecha_referencia") String fechaReferencia
) {}
