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
public class FlujoOd {
    private Integer id; // SERIAL PK
    private String clusterOrigem;
    private String clusterDestino;
    private String municipioOrigem;
    private String municipioDestino;
    private Integer nUsuarios; // INT
    private Integer nViagens; // INT
    private Double distMediaKm; // FLOAT (64 bits -> Double en Java)
    private Short mesmoCluster; // SMALLINT (0 / 1 -> Short en Java)
}
