package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record MapResponseDTO(
        @JsonProperty("regiones") List<MapRegionDTO> regiones
) {
    public record MapRegionDTO(
            String cluster,
            String municipio,
            Double lat,
            Double lon,
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            @JsonProperty("rat_type_predominante") String ratTypePredominante,
            @JsonProperty("download_gb") Double downloadGb,
            String periodo,
            String fecha
    ) {}
}
