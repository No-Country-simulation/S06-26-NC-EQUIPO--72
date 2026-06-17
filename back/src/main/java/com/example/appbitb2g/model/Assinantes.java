package com.example.appbitb2g.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
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
@Entity(name = "assinantes")
public class Assinantes {

    @Id
    @Column(name = "assinante_hash")
    private Integer assinanteHash;  // PK Manual

    @Column(name = "home_cluster")
    private String homeCluster;

    @Column(name = "home_municipio")
    private String homeMunicipio;

    @Column(name = "income_cluster")
    private String incomeCluster; // A, B, C, D

    @Column(name = "age_group")
    private String ageGroup; // 18-24, 25-34, etc.

    @Column(name = "mobility_pattern")
    private String mobilityPattern;

    @Column(name = "flag_flagship")
    private Short flagFlagship;

}