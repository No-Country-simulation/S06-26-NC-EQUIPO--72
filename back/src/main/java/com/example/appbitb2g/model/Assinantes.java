package com.example.appbitb2g.model;

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
public class Assinantes {
    private Integer assinanteHash;  // PK Manual
    private String homeCluster;

    private String homeMunicipio;

    private String incomeCluster; // A, B, C, D

    private String ageGroup; // 18-24, 25-34, etc.

    private String mobilityPattern;

    private Short flagFlagship;

}