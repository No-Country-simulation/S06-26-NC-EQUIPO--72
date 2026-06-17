package com.example.appbitb2g.dto.responseDTO.socialProgram;

import java.time.LocalDate;

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
public class SocialProgramResponseDTO {

    private Integer id;
    private String mensaje;

    @Getter
    @Setter
    @AllArgsConstructor
    @NoArgsConstructor
    @Builder
    public static class ProgramDetail {
        private Integer id;
        private String nombre;
        private String tipo;
        private String descripcion;
        private String municipio;
        private String cluster;
        private String organizacion;
        private String liderReferente;
        private Integer replicable;
        private String impactoEstimado;
        private String urlReferencia;
        private LocalDate fechaInicio;
        private LocalDate fechaFin;
    }

}
