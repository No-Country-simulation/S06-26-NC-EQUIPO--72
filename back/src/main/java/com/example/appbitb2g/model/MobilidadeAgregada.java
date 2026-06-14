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
public class MobilidadeAgregada {
    private Integer id; // SERIAL PK
    private String ecgi; // FK -> antenas
    private String cluster;
    private String municipio;
    private LocalDate dayDate; // DATE
    private String periodo;
    private String incomeCluster; // CHAR(1) -> String de longitud 1
    private String ageGroup; // VARCHAR(5) -> "18-24", etc.
    private String ratType; // VARCHAR(5) -> "LTE", "NR", etc.
    private Integer nSessoes; // INT
    private Double downloadBytes; // FLOAT
    private Double dropPctAvg; // FLOAT
    private Double congestionamentoAvg; // FLOAT
    
}
