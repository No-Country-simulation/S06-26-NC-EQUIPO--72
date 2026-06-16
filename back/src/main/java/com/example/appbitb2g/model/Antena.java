package com.example.appbitb2g.model;

import java.math.BigDecimal;

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
public class Antena {

private String ecgi;           //siempre string, nunca numeric
private String cluster;       
private String municipio;     
private BigDecimal lat;         
private BigDecimal lon;         
    
}
