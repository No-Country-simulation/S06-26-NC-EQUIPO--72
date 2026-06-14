package com.example.appbitb2g.model;

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
public class ProgramasSociales {
    private Integer id; // SERIAL PK
    private String nombre;
    private String tipo; // FORMACION / MENTORIA / EXPERIENCIA
    private String descripcion;
    private String municipio;
    private String cluster; // FK semántica -> antenas.cluster
    private String organizacion;
    private String liderReferente; // VARCHAR(150) NULL
    private Short replicable; // SMALLINT NULL (0 / 1)
    private String impactoEstimado; // BAJO / MEDIO / ALTO
    private String urlReferencia; // VARCHAR(255) NULL
    private LocalDate fechaInicio; // DATE
    private LocalDate fechaFin; // DATE NULL
    private Short activo;
}
