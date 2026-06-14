package com.example.appbitb2g.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
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
public class IndicadoresTerritoriales {
    private Integer id; // SERIAL PK
    private String municipio;
    private String cluster; // FK semântica -> antenas.cluster
    private String categoria; // SALUD_MENTAL / EMPLEO / EDUCACION
    private String indicador; // taxa_internacao_psiquiatrica / etc
    private BigDecimal valor; // DECIMAL(15,4) -> BigDecimal para precisão exata
    private String unidad;
    private String fonte; // DATASUS / IBGE / OMS / MOCK
    private String codigoOrigem; // SIH-SUS / PNAD / GHO
    private String urlOrigem; // TEXT NULL
    private LocalDate fechaReferencia; // DATE
    private LocalDateTime createdAt; // TIMESTAMP DEFAULT NOW()
    private LocalDateTime updatedAt;
    
}
