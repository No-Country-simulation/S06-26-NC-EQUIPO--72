package com.example.appbitb2g.seed;

import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import com.example.appbitb2g.model.Concentracao;
import com.example.appbitb2g.repository.ConcentracaoRepository;

@Component
@Profile("dev")
public class ConcentracaoSeeder {
    @Autowired private ConcentracaoRepository repo;
    public void seed() {
        if (repo.count() > 0)
            return;
        repo.saveAll(List.of(
    new Concentracao(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MANHA", 1367, 104305839720L / 1073741824.0, 0.348, "LTE"),
    new Concentracao(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "NOITE", 2515, 210260111898L / 1073741824.0, 0.346, "LTE"),
    new Concentracao(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", 2593, 217103516502L / 1073741824.0, 0.351, "LTE"),
    new Concentracao(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MADRUGADA", 594, 38176991396L / 1073741824.0, 0.354, "LTE"),
    new Concentracao(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MANHA", 1492, 108041863050L / 1073741824.0, 0.355, "LTE"),
    new Concentracao(null, "724050697605965", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "NOITE", 2659, 225122610638L / 1073741824.0, 0.354, "LTE"),
    new Concentracao(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "MADRUGADA", 604, 40600047533L / 1073741824.0, 0.362, "LTE"),
    new Concentracao(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", 2606, 233095668528L / 1073741824.0, 0.351, "LTE"),
    new Concentracao(null, "724050683983270", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-01"), "TARDE", 2687, 227148725099L / 1073741824.0, 0.35, "LTE"),
    new Concentracao(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", 2202, 142182103926L / 1073741824.0, 0.352, "LTE"),
    new Concentracao(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", 1815, 114270451577L / 1073741824.0, 0.346, "LTE"),
    new Concentracao(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-02"), "TARDE", 2099, 132302478708L / 1073741824.0, 0.35, "LTE"),
    new Concentracao(null, "7240501005162597", "LAGOA_CONCEICAO", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", 1841, 105505564375L / 1073741824.0, 0.353, "LTE"),
    new Concentracao(null, "7240501005162597", "LAGOA_CONCEICAO", "Florianopolis", LocalDate.parse("2026-03-02"), "TARDE", 2046, 136363090099L / 1073741824.0, 0.347, "LTE"),
    new Concentracao(null, "7240501004550410", "UFSC", "Florianopolis", LocalDate.parse("2026-03-02"), "NOITE", 2257, 156516630388L / 1073741824.0, 0.347, "LTE"),
    new Concentracao(null, "7240501005172207", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-03"), "MANHA", 1815, 110087016449L / 1073741824.0, 0.345, "LTE"),
    new Concentracao(null, "7240501005172207", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-03"), "NOITE", 1846, 114162056652L / 1073741824.0, 0.354, "LTE"),
    new Concentracao(null, "7240501005162724", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-03"), "MANHA", 1775, 105866122867L / 1073741824.0, 0.348, "LTE"),
    new Concentracao(null, "724050699925231", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-03"), "MANHA", 1804, 117528140484L / 1073741824.0, 0.346, "LTE"),
    new Concentracao(null, "724050699925231", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-03"), "TARDE", 2119, 142220275627L / 1073741824.0, 0.348, "LTE"),
    new Concentracao(null, "7240501003962715", "BIGUACU_BR101_NORTE", "Biguacu", LocalDate.parse("2026-03-03"), "TARDE", 2518, 187176392591L / 1073741824.0, 0.344, "LTE"),
    new Concentracao(null, "7240501003962715", "BIGUACU_BR101_NORTE", "Biguacu", LocalDate.parse("2026-03-03"), "MANHA", 2127, 154441661228L / 1073741824.0, 0.355, "LTE"),
    new Concentracao(null, "7240501003962715", "BIGUACU_BR101_NORTE", "Biguacu", LocalDate.parse("2026-03-03"), "NOITE", 2175, 159343522728L / 1073741824.0, 0.345, "LTE"),
    new Concentracao(null, "7240501003495238", "TRINDADE", "Florianopolis", LocalDate.parse("2026-03-03"), "TARDE", 2522, 168858843370L / 1073741824.0, 0.351, "LTE"),
    new Concentracao(null, "7240501003495238", "TRINDADE", "Florianopolis", LocalDate.parse("2026-03-03"), "NOITE", 2101, 136417442042L / 1073741824.0, 0.356, "LTE"),
    new Concentracao(null, "724050697397122", "ESTREITO_CAPOEIRAS", "Florianopolis", LocalDate.parse("2026-03-04"), "NOITE", 1686, 104625030004L / 1073741824.0, 0.344, "LTE"),
    new Concentracao(null, "724050699925282", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "NOITE", 1859, 115782327599L / 1073741824.0, 0.349, "LTE"),
    new Concentracao(null, "7240501003861722", "TRINDADE", "Florianopolis", LocalDate.parse("2026-03-04"), "TARDE", 2584, 180172013437L / 1073741824.0, 0.355, "LTE"),
    new Concentracao(null, "7240501003861722", "TRINDADE", "Florianopolis", LocalDate.parse("2026-03-04"), "MANHA", 2151, 144930437118L / 1073741824.0, 0.349, "LTE"),
    new Concentracao(null, "724050687263808", "INGLESES", "Florianopolis", LocalDate.parse("2026-03-04"), "MANHA", 1600, 99569630089L / 1073741824.0, 0.35, "LTE"),
    new Concentracao(null, "724050684142660", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "TARDE", 2122, 134267030502L / 1073741824.0, 0.347, "LTE"),
    new Concentracao(null, "724050684142660", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "NOITE", 1842, 117375228868L / 1073741824.0, 0.344, "LTE"),
    new Concentracao(null, "724050684142660", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "MANHA", 1821, 106132215013L / 1073741824.0, 0.346, "LTE"),
    new Concentracao(null, "724050699925215", "ESTREITO_CAPOEIRAS", "Sao Jose", LocalDate.parse("2026-03-04"), "MADRUGADA", 546, 25961151411L / 1073741824.0, 0.353, "LTE"),
    new Concentracao(null, "724050699925215", "ESTREITO_CAPOEIRAS", "Sao Jose", LocalDate.parse("2026-03-04"), "MANHA", 1690, 103782519386L / 1073741824.0, 0.353, "LTE"),
    new Concentracao(null, "724050699925282", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "MANHA", 1744, 107921347308L / 1073741824.0, 0.343, "LTE"),
    new Concentracao(null, "724050699925282", "SAO_JOSE_KOBRASOL", "Sao Jose", LocalDate.parse("2026-03-04"), "TARDE", 2100, 132143780187L / 1073741824.0, 0.353, "LTE"),
    new Concentracao(null, "7240501005162660", "JURERE", "Florianopolis", LocalDate.parse("2026-03-04"), "MANHA", 1618, 99592919677L / 1073741824.0, 0.351, "LTE"),
    new Concentracao(null, "724050699979439", "SAO_JOSE_CENTRO", "Sao Jose", LocalDate.parse("2026-03-05"), "MANHA", 3380, 292879531224L / 1073741824.0, 0.347, "LTE"),
    new Concentracao(null, "724050699979439", "SAO_JOSE_CENTRO", "Sao Jose", LocalDate.parse("2026-03-05"), "MADRUGADA", 1154, 81400480173L / 1073741824.0, 0.355, "LTE"),
    new Concentracao(null, "724050687263808", "INGLESES", "Florianopolis", LocalDate.parse("2026-03-05"), "MADRUGADA", 580, 27760638311L / 1073741824.0, 0.354, "LTE"),
    new Concentracao(null, "724050687263808", "INGLESES", "Florianopolis", LocalDate.parse("2026-03-05"), "TARDE", 1986, 128473042522L / 1073741824.0, 0.344, "LTE"),
    new Concentracao(null, "724050698820053", "CAMPECHE", "Florianopolis", LocalDate.parse("2026-03-05"), "NOITE", 1815, 119126834419L / 1073741824.0, 0.344, "LTE"),
    new Concentracao(null, "724050697545253", "SC401_CORREDOR", "Florianopolis", LocalDate.parse("2026-03-05"), "TARDE", 1829, 117944878561L / 1073741824.0, 0.349, "LTE"),
    new Concentracao(null, "724050697545253", "SC401_CORREDOR", "Florianopolis", LocalDate.parse("2026-03-05"), "NOITE", 1596, 97954665119L / 1073741824.0, 0.354, "LTE"),
    new Concentracao(null, "7240501005309970", "AEROPORTO_HLZ", "Florianopolis", LocalDate.parse("2026-03-05"), "MANHA", 1714, 115674103037L / 1073741824.0, 0.352, "LTE"),
    new Concentracao(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-06"), "TARDE", 2554, 165596461914L / 1073741824.0, 0.357, "LTE"),
    new Concentracao(null, "724050697342190", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-06"), "NOITE", 2191, 144431295480L / 1073741824.0, 0.345, "LTE"),
    new Concentracao(null, "724050684142457", "CBD_BEIRAMAR", "Florianopolis", LocalDate.parse("2026-03-06"), "MADRUGADA", 681, 34612641654L / 1073741824.0, 0.363, "LTE")
));

    }
}
