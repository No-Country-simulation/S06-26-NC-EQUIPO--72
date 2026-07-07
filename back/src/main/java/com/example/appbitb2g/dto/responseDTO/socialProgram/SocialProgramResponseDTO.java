package com.example.appbitb2g.dto.responseDTO.socialProgram;

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
@Schema(description = "Respuesta base para operaciones sobre programas sociales")
public class SocialProgramResponseDTO {

    @Schema(description = "Identificador del programa", example = "1")
    private Integer id;
    @Schema(description = "Mensaje de estado de la operación", example = "Programa registrado correctamente.")
    private String mensaje;

    @Getter
    @Setter
    @AllArgsConstructor
    @NoArgsConstructor
    @Builder
    @Schema(description = "Detalle de un programa social")
    public static class ProgramDetail {
        @Schema(description = "Identificador del programa", example = "1")
        private Integer id;
        @Schema(description = "Nombre del programa", example = "Alfabetización Digital para Adultos Mayores")
        private String nombre;
        @Schema(description = "Tipo de programa", example = "FORMACION")
        private String tipo;
        @Schema(description = "Descripción del programa", example = "Clases presenciales de uso de smartphones.")
        private String descripcion;
        @Schema(description = "Municipio", example = "Florianópolis")
        private String municipio;
        @Schema(description = "Clúster territorial", example = "FLORIANOPOLIS_CENTRO")
        private String cluster;
        @Schema(description = "Organización responsable", example = "Municipalidad de Florianópolis")
        private String organizacion;
        @Schema(description = "Líder referente", example = "Isabela Martins")
        private String liderReferente;
        @Schema(description = "Indicador de replicabilidad", example = "1")
        private Integer replicable;
        @Schema(description = "Impacto estimado", example = "ALTO")
        private String impactoEstimado;
        @Schema(description = "URL de referencia", example = "https://florianopolis.sc.gov.br/alfabetizacion")
        private String urlReferencia;
        @Schema(description = "Fecha de inicio", type = "string", format = "date", example = "2025-02-01")
        private LocalDate fechaInicio;
        @Schema(description = "Fecha de fin", type = "string", format = "date", example = "2025-12-31")
        private LocalDate fechaFin;
        private Integer total;
    }

}
