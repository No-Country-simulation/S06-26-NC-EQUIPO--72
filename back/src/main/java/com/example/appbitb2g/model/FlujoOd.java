package com.example.appbitb2g.model;

import jakarta.annotation.Generated;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
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
@Entity(name="flujo_od")
public class FlujoOd {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id; // SERIAL PK
    @Column(name = "cluster_origem")
    private String clusterOrigem;
    @Column(name = "cluster_destino")
    private String clusterDestino;
    @Column(name = "municipio_origem")
    private String municipioOrigem;
    @Column(name = "municipio_destino")
    private String municipioDestino;
    @Column(name = "n_usuarios")
    private Integer nUsuarios; // INT
    @Column(name = "n_viagens")
    private Integer nViagens; // INT
    @Column(name = "dist_media_km")
    private Double distMediaKm; // FLOAT (64 bits -> Double en Java)
    @Column(name = "mesmo_cluster")
    private Short mesmoCluster; // SMALLINT (0 / 1 -> Short en Java)
}
