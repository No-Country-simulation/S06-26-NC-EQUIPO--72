package com.example.appbitb2g.model;

import java.time.LocalDate;

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
import jakarta.persistence.OneToMany;
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
@Entity(name="concentracao")
public class Concentracao {
    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id; // SERIAL PK
    private String ecgi; // FK -> antenas
    private String cluster;
    private String municipio;
    @Column(name = "day_date")
    private LocalDate dayDate; // DATE
  
    private String periodo; // MADRUGADA / MANHA / TARDE
    @Column(name = "n_usuarios")
    private Integer nUsuarios; // INT
    @Column(name = "download_gb")
    private Double downloadGb; // FLOAT
    @Column(name = "congestionamento_medio")
    private Double congestionamentoMedio; // FLOAT
   
    @Column(name = "rat_type_predominante")
    private String ratTypePredominante; // NR / LTE / WCDMA
}
