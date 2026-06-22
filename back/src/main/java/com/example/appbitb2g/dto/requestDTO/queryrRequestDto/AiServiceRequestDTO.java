
package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

//  Envia la consulta y el idioma al servicio de IA
public record AiServiceRequestDTO(
    String consulta,
    String idioma
) {}
