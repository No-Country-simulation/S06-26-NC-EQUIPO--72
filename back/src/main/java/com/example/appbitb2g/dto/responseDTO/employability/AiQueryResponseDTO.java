package com.example.appbitb2g.dto.responseDTO.employability;

import java.util.List;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class AiQueryResponseDTO {
    String respuestaIa;
    String visualizacionSugerida;
    List<Map<String, Object>> datos; 
    List<FountainDTO> fuentes;
    Integer totalRegistros;
    String idioma;
}
