package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@Schema(description = "Filtro auxiliar para consultas de brechas")
public class GapFilterDTO {
    @Schema(description = "Servicio a analizar", example = "FORMACION")
    String servicio;
    @Schema(description = "Municipio para filtrar", example = "São José")
    String municipio;
    @Schema(description = "Clúster opcional para la consulta", example = "SAO_JOSE_KOBRASOL")
    String cluster;
}
