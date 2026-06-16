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
public class Concentracao {
    private Integer id; // SERIAL PK
    private String ecgi; // FK -> antenas
    private String cluster;
    private String municipio;
    private LocalDate dayDate; // DATE
    private String periodo; // MADRUGADA / MANHA / TARDE / NOITE
    private Integer nUsuarios; // INT
    private Double downloadGb; // FLOAT
    private Double congestionamentoMedio; // FLOAT
    private String ratTypePredominante; // NR / LTE / WCDMA
    
}
