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
@Entity(name = "movilidade_agregada")
public class MobilidadeAgregada {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Id autoincremental
    private Integer id; // SERIAL PK

    private String ecgi; // FK -> antenas

    private String cluster;
    private String municipio;

    @Column(name = "day_date")
    private LocalDate dayDate; // DATE
    private String periodo;

    @Column(name = "income_cluster")
    private String incomeCluster; // CHAR(1) -> String de longitud 1

    @Column(name = "age_group")
    private String ageGroup; // VARCHAR(5) -> "18-24", etc.
    @Column(name = "rat_type")
    private String ratType; // VARCHAR(5) -> "LTE", "NR", etc.

    @Column(name = "n_sessoes")
    private Integer nSessoes; // INT

    @Column(name = "download_bytes")
    private Double downloadBytes; // FLOAT

    @Column(name = "drop_pct_avg")
    private Double dropPctAvg; // FLOAT

    @Column(name = "congestionamento_avg")
    private Double congestionamentoAvg; // FLOAT
    
}
