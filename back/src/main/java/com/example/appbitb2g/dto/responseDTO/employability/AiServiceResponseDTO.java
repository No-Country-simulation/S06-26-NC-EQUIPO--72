
package com.example.appbitb2g.dto.responseDTO.employability;

import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;

//  Recibe la respuesta desde el servicio de IA
public record AiServiceResponseDTO(
    @JsonProperty("respuesta_ia") String respuesta_ia,
    @JsonProperty("datos") List<Map<String, Object>> datos,
    @JsonProperty("fuentes") List<FountainDTO> fuentes,
    @JsonProperty("visualizacion_sugerida") String visualizacion_sugerida,
    @JsonProperty("idioma") String idioma
) {}
