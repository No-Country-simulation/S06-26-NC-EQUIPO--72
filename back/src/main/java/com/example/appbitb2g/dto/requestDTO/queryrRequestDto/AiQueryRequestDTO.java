package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;


//  Recibe la consulta y el idioma desde el front
public record AiQueryRequestDTO(
    String consulta,
    String idioma
) {}
