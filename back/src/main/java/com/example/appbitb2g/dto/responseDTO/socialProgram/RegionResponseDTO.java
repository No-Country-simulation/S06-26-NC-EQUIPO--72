package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.util.List;

@Schema(description = "Listado de regiones disponibles para visualización geográfica")
public record RegionResponseDTO(
        @JsonProperty("regiones") List<RegionRecord> regiones
) {

    @Schema(description = "Detalle geográfico de una región")
    public record RegionRecord(
            @Schema(description = "Clúster territorial", example = "FLORIANOPOLIS_CENTRO")
            String cluster,
            @Schema(description = "Municipio", example = "Florianópolis")
            String municipio,
            @Schema(description = "Latitud del centroide", example = "-27.5969")
            @JsonProperty("lat_centroide") BigDecimal latCentroide,
            @Schema(description = "Longitud del centroide", example = "-48.5495")
            @JsonProperty("lon_centroide") BigDecimal lonCentroide,
            @Schema(description = "Cantidad de antenas", example = "18")
            @JsonProperty("n_antenas") Integer nAntenas
    ) {}
}
