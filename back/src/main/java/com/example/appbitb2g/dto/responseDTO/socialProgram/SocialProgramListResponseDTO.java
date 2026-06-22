package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.time.LocalDate;
import java.util.List;

@Schema(description = "Listado resumido de programas sociales")
public record SocialProgramListResponseDTO(
        @Schema(description = "Programas devueltos por la consulta")
        List<ProgramDetailRecord> programas,
        @Schema(description = "Cantidad total de programas", example = "3")
        Integer total
) {
    /**
     * Registro detallado de cada programa individual.
     */
    @Schema(description = "Detalle resumido de un programa social")
    public record ProgramDetailRecord(
            @Schema(description = "Identificador del programa", example = "1")
            Integer id,
            @Schema(description = "Nombre del programa", example = "Alfabetización Digital para Adultos Mayores")
            String nombre,
            @Schema(description = "Tipo de programa", example = "FORMACION")
            String tipo,
            @Schema(description = "Descripción del programa", example = "Clases presenciales de uso de smartphones y banca móvil.")
            String descripcion,
            @Schema(description = "Municipio", example = "Florianópolis")
            String municipio,
            @Schema(description = "Clúster territorial", example = "FLORIANOPOLIS_CENTRO")
            String cluster,
            @Schema(description = "Organización responsable", example = "Municipalidad de Florianópolis")
            String organizacion,
            @Schema(description = "Líder referente", example = "Isabela Martins")
            @JsonProperty("lider_referente") String liderReferente,
            @Schema(description = "Indicador de replicabilidad", example = "1")
            Integer replicable,
            @Schema(description = "Impacto estimado", example = "ALTO")
            @JsonProperty("impacto_estimado") String impactoEstimado,
            @Schema(description = "URL de referencia", example = "https://florianopolis.sc.gov.br/alfabetizacion")
            @JsonProperty("url_referencia") String urlReferencia,
            @Schema(description = "Fecha de inicio", type = "string", format = "date", example = "2025-02-01")
            @JsonProperty("fecha_inicio") LocalDate fechaInicio,
            @Schema(description = "Fecha de fin", type = "string", format = "date", example = "2025-12-31")
            @JsonProperty("fecha_fin") LocalDate fechaFin,
            @Schema(description = "Estado activo del programa", example = "true")
            Boolean activo
    ) {}
}
