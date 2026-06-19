package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record RegionResponseDTO(
        @JsonProperty("regiones") List<RegionRecord> regiones
) {

    public record RegionRecord(
            String cluster,
            String municipio,
            @JsonProperty("lat_centroide") Double latCentroide,
            @JsonProperty("lon_centroide") Double lonCentroide,
            @JsonProperty("n_antenas") Integer nAntenas
    ) {}
}
