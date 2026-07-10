package com.example.appbitb2g.dto.requestDTO.socialProgram;

import java.time.LocalDate;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Schema(description = "Datos para crear o actualizar un programa social")
public class SocialProgramRequestDTO {

    @Schema(description = "Nombre del programa", example = "Alfabetización Digital para Adultos Mayores")
    private String nombre;

    @Schema(description = "Tipo de programa", example = "FORMACION")
    private String tipo; // FORMACION / MENTORIA / EXPERIENCIA

    @Schema(description = "Descripción del programa", example = "Curso presencial de uso de smartphones y banca móvil.")
    private String descripcion; // TEXT

    @Schema(description = "Municipio donde aplica el programa", example = "Florianópolis")
    private String municipio;

    @Schema(description = "Clúster asociado al programa", example = "FLORIANOPOLIS_CENTRO")
    private String cluster;

    @Schema(description = "Organización responsable", example = "Municipalidad de Florianópolis")
    private String organizacion;

    @Schema(description = "Líder o referente", example = "Isabela Martins")
    private String liderReferente;

    @Schema(description = "Indicador de replicabilidad", example = "1")
    private Integer replicable; // SMALLINT (0 / 1)

    @Schema(description = "Impacto estimado", example = "ALTO")
    private String impactoEstimado; // BAJO / MEDIO / ALTO

    @Schema(description = "URL de referencia", example = "https://florianopolis.sc.gov.br/alfabetizacion")
    private String urlReferencia;

    @Schema(description = "Fecha de inicio", type = "string", format = "date", example = "2025-02-01")
    private LocalDate fechaInicio; // DATE

    @Schema(description = "Fecha de fin", type = "string", format = "date", example = "2025-12-31")
    private LocalDate fechaFin; // DATE

    @Schema(description = "Estado activo del programa", example = "true")
    private Boolean activo;

}
