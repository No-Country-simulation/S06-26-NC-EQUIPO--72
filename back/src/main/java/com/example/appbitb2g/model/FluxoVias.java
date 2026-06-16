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
public class FluxoVias {

    private Integer id; // SERIAL PK
    private String ecgiOrigem; // FK -> antenas
    private String ecgiDestino; // FK -> antenas
    private String clusterOrigem;
    private String clusterDestino;
    private Integer nUsuarios; // INT
    private Integer nTransicoes; // INT
    private Double distKm; // FLOAT
    private String periodoPredominante; // VARCHAR(12)
    private Double pctDoClusterOrigem; // FLOAT
}
   
 