
package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

import io.swagger.v3.oas.annotations.media.Schema;

//  Envia la consulta y el idioma al servicio de IA
@Schema(description = "Solicitud interna que se envía al servicio de IA")
public record AiServiceRequestDTO(
    @Schema(description = "Texto de la consulta", example = "¿Cuáles son las brechas de formación en São José?")
    String consulta,
    @Schema(description = "Idioma de la consulta", example = "es")
    String idioma
) {}
