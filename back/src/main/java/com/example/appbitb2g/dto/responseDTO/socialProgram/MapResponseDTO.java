package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.util.List;

@Schema(description = "Respuesta del mapa principal con regiones y métricas")
public record MapResponseDTO(
        @JsonProperty("regiones") List<MapRegionDTO> regiones
) {
    @Schema(description = "Detalle de una región en el mapa")
    public record MapRegionDTO(
            @Schema(description = "Clúster territorial", example = "SAO_JOSE_KOBRASOL")
            String cluster,
            @Schema(description = "Municipio", example = "São José")
            String municipio,
            @Schema(description = "Latitud", example = "-27.5935")
            Double lat,
            @Schema(description = "Longitud", example = "-48.6358")
            Double lon,
            @Schema(description = "Cantidad de usuarios", example = "12400")
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @Schema(description = "Congestión media", example = "0.72")
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            @Schema(description = "Tecnología predominante", example = "LTE")
            @JsonProperty("rat_type_predominante") String ratTypePredominante,
            @Schema(description = "Volumen descargado en GB", example = "34.5")
            @JsonProperty("download_gb") Double downloadGb,
            @Schema(description = "Período horario", example = "TARDE")
            String periodo,
            @Schema(description = "Fecha de referencia", example = "2025-12-01")
            String fecha
    ) {}
}
