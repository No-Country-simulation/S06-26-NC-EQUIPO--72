package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDate;
import java.util.List;

public record SocialProgramListResponseDTO(
        List<ProgramDetailRecord> programas,
        Integer total
) {
    /**
     * Registro detallado de cada programa individual.
     */
    public record ProgramDetailRecord(
            Integer id,
            String nombre,
            String tipo,
            String descripcion,
            String municipio,
            String cluster,
            String organizacion,
            @JsonProperty("lider_referente") String liderReferente,
            Integer replicable,
            @JsonProperty("impacto_estimado") String impactoEstimado,
            @JsonProperty("url_referencia") String urlReferencia,
            @JsonProperty("fecha_inicio") LocalDate fechaInicio,
            @JsonProperty("fecha_fin") LocalDate fechaFin,
            Boolean activo
    ) {}
}
