package com.example.appbitb2g.model;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

import org.hibernate.annotations.ManyToAny;

import jakarta.annotation.Generated;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
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
@Entity
@Table(name = "indicadores_territoriales")
public class TerritorialIndicators {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id; // SERIAL PK
    private String municipio;
    private String cluster; // FK semântica -> antenas.cluster
    private String categoria; // SALUD_MENTAL / EMPLEO / EDUCACION
    private String indicador; // taxa_internacao_psiquiatrica / etc
    private BigDecimal valor; // DECIMAL(15,4) -> BigDecimal para precisão exata
    private String unidad;
    private String fonte; // DATASUS / IBGE / OMS / MOCK
    @Column(name = "codigo_origem")
    private String codigoOrigem; // SIH-SUS / PNAD / GHO
    @Column(name = "url_origem")
    private String urlOrigem; // TEXT NULL
    @Column(name = "fecha_referencia")
    private LocalDate fechaReferencia; // DATE
    @Column(name = "created_at")
    private LocalDateTime createdAt; // TIMESTAMP DEFAULT NOW()
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

}
