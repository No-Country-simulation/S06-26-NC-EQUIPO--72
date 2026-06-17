package com.example.appbitb2g.model;

import java.time.LocalDate;

import jakarta.persistence.*;
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
@Entity(name = "programas_sociales")
public class ProgramasSociales {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id; // SERIAL PK

    private String nombre;

    private String tipo; // FORMACION / MENTORIA / EXPERIENCIA

    private String descripcion; // TEXT

    private String municipio;

    private String cluster; // FK semántica -> antenas.cluster

    private String organizacion;

    @Column(name = "lider_referente")
    private String liderReferente;

    private Integer replicable; // SMALLINT (0 / 1)

    @Column(name = "impacto_estimado")
    private String impactoEstimado; // BAJO / MEDIO / ALTO

    @Column(name = "url_referencia")
    private String urlReferencia;

    @Column(name = "fecha_inicio")
    private LocalDate fechaInicio; // DATE

    @Column(name = "fecha_fin")
    private LocalDate fechaFin; // DATE

    private Short activo; // SMALLINT (0 / 1)
}
