package com.example.appbitb2g.seed;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import com.example.appbitb2g.model.Antenna;
import com.example.appbitb2g.model.Assinantes;
import com.example.appbitb2g.repository.AssinantesRepository;

import lombok.AllArgsConstructor;

@Component
@Profile("dev")

public class AssinantesSeeder {
    @Autowired private AssinantesRepository repo;

    public void seed() {
        if (repo.count() > 0)
            return;

        repo.saveAll(List.of(
    new Assinantes(1, "CBD_BEIRAMAR", "Florianópolis", "C", "25-34", "INTENSA", (short) 0),
    new Assinantes(2, "SAO_JOSE_BARREIROS", "São José", "B", "55+", "MODERADA", (short) 1),
    new Assinantes(3, "LAGOA_CONCEICAO", "Florianópolis", "C", "55+", "INTENSA", (short) 0),
    new Assinantes(4, "CAMPECHE", "Florianópolis", "A", "18-24", "INTENSA", (short) 0),
    new Assinantes(5, "CENTRO_HISTORICO", "Florianópolis", "C", "45-54", "BAIXA", (short) 0),
    new Assinantes(6, "SANTO_AMARO", "Santo Amaro da Imperatriz", "B", "25-34", "MODERADA", (short) 0),
    new Assinantes(7, "COQUEIROS", "Florianópolis", "D", "55+", "MODERADA", (short) 0),
    new Assinantes(8, "PALHOCA_CENTRO", "Palhoça", "C", "18-24", "BAIXA", (short) 0),
    new Assinantes(9, "SAO_JOSE_ROCADO", "São José", "D", "35-44", "BAIXA", (short) 1),
    new Assinantes(10, "ESTREITO_CAPOEIRAS", "Florianópolis", "D", "35-44", "MODERADA", (short) 0),
    new Assinantes(11, "SC401_CORREDOR", "Florianópolis", "D", "55+", "MODERADA", (short) 0),
    new Assinantes(12, "PALHOCA_BR101_SUL", "Palhoça", "C", "35-44", "MODERADA", (short) 1),
    new Assinantes(13, "CENTRO_HISTORICO", "Florianópolis", "B", "25-34", "MODERADA", (short) 1),
    new Assinantes(14, "SAO_JOSE_BARREIROS", "São José", "C", "55+", "BAIXA", (short) 1),
    new Assinantes(15, "PALHOCA_BR101_SUL", "Palhoça", "D", "18-24", "BAIXA", (short) 0),
    new Assinantes(16, "CENTRO_HISTORICO", "Florianópolis", "C", "35-44", "INTENSA", (short) 0),
    new Assinantes(17, "PALHOCA_CENTRO", "Palhoça", "D", "45-54", "BAIXA", (short) 1),
    new Assinantes(18, "SAO_JOSE_BARREIROS", "São José", "D", "45-54", "BAIXA", (short) 0),
    new Assinantes(19, "CAMPECHE", "Florianópolis", "C", "45-54", "INTENSA", (short) 0),
    new Assinantes(20, "ESTREITO_CAPOEIRAS", "Florianópolis", "B", "25-34", "MODERADA", (short) 1),
    new Assinantes(21, "SAO_JOSE_KOBRASOL", "São José", "A", "25-34", "INTENSA", (short) 1),
    new Assinantes(22, "TRINDADE", "Florianópolis", "B", "45-54", "INTENSA", (short) 0),
    new Assinantes(23, "CBD_BEIRAMAR", "Florianópolis", "C", "18-24", "BAIXA", (short) 0),
    new Assinantes(24, "SAO_JOSE_CENTRO", "São José", "C", "55+", "INTENSA", (short) 0),
    new Assinantes(25, "SC401_CORREDOR", "Florianópolis", "B", "25-34", "MODERADA", (short) 0),
    new Assinantes(26, "UFSC", "Florianópolis", "B", "25-34", "BAIXA", (short) 0),
    new Assinantes(27, "TRINDADE", "Florianópolis", "C", "18-24", "BAIXA", (short) 0),
    new Assinantes(28, "ESTREITO_CAPOEIRAS", "Florianópolis", "C", "55+", "MODERADA", (short) 0),
    new Assinantes(29, "TRINDADE", "Florianópolis", "A", "35-44", "MODERADA", (short) 0),
    new Assinantes(30, "PALHOCA_CENTRO", "Palhoça", "D", "45-54", "MODERADA", (short) 0),
    new Assinantes(31, "UFSC", "Florianópolis", "C", "45-54", "INTENSA", (short) 0),
    new Assinantes(32, "RESIDENCIAL_NORTE", "Florianópolis", "C", "45-54", "INTENSA", (short) 0),
    new Assinantes(33, "SANTO_AMARO", "Santo Amaro da Imperatriz", "C", "45-54", "INTENSA", (short) 0),
    new Assinantes(34, "TRINDADE", "Florianópolis", "D", "25-34", "MODERADA", (short) 1),
    new Assinantes(35, "CENTRO_HISTORICO", "Florianópolis", "D", "18-24", "INTENSA", (short) 0),
    new Assinantes(36, "UFSC", "Florianópolis", "D", "55+", "MODERADA", (short) 0),
    new Assinantes(37, "CBD_BEIRAMAR", "Florianópolis", "B", "45-54", "MODERADA", (short) 1),
    new Assinantes(38, "JURERE", "Florianópolis", "C", "45-54", "BAIXA", (short) 0),
    new Assinantes(39, "AEROPORTO_HLZ", "Florianópolis", "C", "45-54", "MODERADA", (short) 0),
    new Assinantes(40, "ESTREITO_CAPOEIRAS", "Florianópolis", "D", "25-34", "MODERADA", (short) 0),
    new Assinantes(41, "COQUEIROS", "Florianópolis", "C", "55+", "BAIXA", (short) 0),
    new Assinantes(42, "VIA_EXPRESSA_CORREDOR", "Florianópolis", "B", "25-34", "MODERADA", (short) 1),
    new Assinantes(43, "TRINDADE", "Florianópolis", "D", "55+", "MODERADA", (short) 0),
    new Assinantes(44, "TRINDADE", "Florianópolis", "D", "45-54", "INTENSA", (short) 0),
    new Assinantes(45, "UFSC", "Florianópolis", "D", "55+", "MODERADA", (short) 0),
    new Assinantes(46, "LAGOA_CONCEICAO", "Florianópolis", "C", "35-44", "BAIXA", (short) 0),
    new Assinantes(47, "INGLESES", "Florianópolis", "A", "55+", "MODERADA", (short) 0),
    new Assinantes(48, "CANASVIEIRAS", "Florianópolis", "C", "18-24", "BAIXA", (short) 0)
));
    }
}
