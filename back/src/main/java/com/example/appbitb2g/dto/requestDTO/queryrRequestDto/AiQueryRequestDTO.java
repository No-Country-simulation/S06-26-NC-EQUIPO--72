package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

import io.swagger.v3.oas.annotations.media.Schema;

//  Recibe la consulta y el idioma desde el front
@Schema(description = "Solicitud para enviar una consulta al servicio de IA")
public record AiQueryRequestDTO(
    @Schema(description = "Texto de la consulta del usuario", example = "¿Cuáles son las brechas de formación en São José?")
    String consulta,
    @Schema(description = "Idioma esperado por el servicio", example = "es")
    String idioma
) {}
