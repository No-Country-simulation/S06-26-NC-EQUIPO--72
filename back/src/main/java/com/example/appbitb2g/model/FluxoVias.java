package com.example.appbitb2g.model;
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
@Entity(name = "fluxo_vias")
public class FluxoVias {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id; // SERIAL PK

    @Column(name = "ecgi_origem")
    private String ecgiOrigem; // FK -> antenas

    @Column(name = "ecgi_destino")
    private String ecgiDestino; // FK -> antenas

    @Column(name = "cluster_origem")
    private String clusterOrigem;

    @Column(name = "cluster_destino")
    private String clusterDestino;

    @Column(name = "n_usuarios")
    private Integer nUsuarios;

    @Column(name = "n_transicoes")
    private Integer nTransicoes;

    @Column(name = "dist_km")
    private Double distKm;

    @Column(name = "periodo_predominante")
    private String periodoPredominante;

    @Column(name = "pct_do_cluster_origem")
    private Double pctDoClusterOrigem;
}
   
 