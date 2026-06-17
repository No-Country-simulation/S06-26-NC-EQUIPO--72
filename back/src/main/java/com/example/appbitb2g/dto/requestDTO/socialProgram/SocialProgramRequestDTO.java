package com.example.appbitb2g.dto.requestDTO.socialProgram;

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
public class SocialProgramRequestDTO {
    private String nombre;

    private String tipo; // FORMACION / MENTORIA / EXPERIENCIA

    private String descripcion; // TEXT

    private String municipio;

    private String cluster;

    private String organizacion;

    private String liderReferente;

    private Integer replicable; // SMALLINT (0 / 1)

    private String impactoEstimado; // BAJO / MEDIO / ALTO

    private String urlReferencia;

    private LocalDate fechaInicio; // DATE

    private LocalDate fechaFin; // DATE

    private boolean activo;

}
