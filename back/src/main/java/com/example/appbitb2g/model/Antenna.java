package com.example.appbitb2g.model;

import java.math.BigDecimal;

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
@Entity(name = "antenas")
public class Antenna {
    @Id
    @Column(name = "ecgi")
    private String ecgi;
    private String cluster;
    private String municipio;
    private BigDecimal lat;
    private BigDecimal lon;
    
}
