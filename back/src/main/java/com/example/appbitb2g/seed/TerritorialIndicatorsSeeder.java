package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.TerritorialIndicators;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Component
@Profile("dev")
public class TerritorialIndicatorsSeeder {

    @Autowired private TerritorialIndicatorsRepository repo;

    public void seed() {
        if (repo.count() > 0) return;

        // { municipio, cluster, empleo_formal, desempleo, evasao, conclusao_medio, internacao_psiq, cobertura_basica }
        Object[][] clusters = {

            {"Florianopolis", "SC401_CORREDOR",        65.4321,  8.7654, 12.3456, 78.9012, 2.1234, 45.6789},
            {"Florianopolis", "ESTREITO_CAPOEIRAS",    60.1234,  9.8765, 14.5678, 75.4321, 2.5678, 42.3456},
            {"Florianopolis", "NORTE_ILHA",            70.9876,  7.1234, 10.9876, 82.3456, 1.9876, 48.7654},
            {"Florianopolis", "TRINDADE",              75.4321,  6.5432,  9.1234, 86.7890, 1.7654, 52.3456},
            {"Florianopolis", "UFSC",                  80.1234,  5.6789,  7.6543, 90.1234, 1.5432, 55.6789},
            {"Florianopolis", "CANASVIEIRAS",          68.7654,  8.2345, 11.4567, 79.5678, 2.0123, 47.8901},
            {"Florianopolis", "AEROPORTO_HLZ",         72.3456,  7.5678, 10.1234, 81.2345, 1.8765, 49.1234},
            {"Florianopolis", "CBD_BEIRAMAR",          78.9012,  5.9876,  8.7654, 87.6543, 1.6543, 53.4567},
            {"Florianopolis", "RESIDENCIAL_NORTE",     66.5432,  8.9012, 13.2345, 77.8901, 2.2345, 44.5678},
            {"Florianopolis", "CENTRO_HISTORICO",      73.2109,  7.3456, 10.5678, 83.1234, 1.8234, 50.3456},
            {"Florianopolis", "LAGOA_CONCEICAO",       69.4567,  8.0123, 11.8901, 80.4567, 1.9512, 48.1234},
            {"Florianopolis", "CAMPECHE",              67.8901,  8.5678, 12.6789, 78.2345, 2.0876, 46.7890},
            {"Florianopolis", "COQUEIROS",             71.2345,  7.8901, 10.3456, 82.6789, 1.9123, 49.5678},
            {"Florianopolis", "JURERE",                76.5432,  6.2345,  8.9012, 88.3456, 1.7123, 54.2345},
            {"Florianopolis", "INGLESES",              64.7890,  9.1234, 13.4567, 76.8901, 2.1890, 43.8901},
            {"Florianopolis", "VIA_EXPRESSA_CORREDOR", 74.1234,  7.0123,  9.7890, 84.5678, 1.7901, 51.6789},

            {"Sao Jose",      "SAO_JOSE_KOBRASOL",     62.3456,  9.4567, 13.8765, 76.1234, 2.3456, 41.2345},
            {"Sao Jose",      "SAO_JOSE_CENTRO",       64.1234,  8.7654, 12.3456, 77.6543, 2.2345, 43.4567},
            {"Sao Jose",      "SAO_JOSE_ROÇADO",       61.2345,  9.8765, 14.1234, 74.9876, 2.4567, 40.1234},
            {"Sao Jose",      "SAO_JOSE_BARREIROS",    63.4567,  9.2345, 13.5678, 76.7890, 2.3456, 41.8901},
            {"Sao Jose",      "ESTREITO_CAPOEIRAS",    59.8901, 10.2345, 14.9876, 74.1234, 2.4123, 39.7890},

            {"Palhoca",       "PALHOCA_CENTRO",        58.1234, 11.2345, 16.3456, 71.4567, 2.7654, 38.5678},
            {"Palhoca",       "PALHOCA_PEDRA_BRANCA",  57.6543, 11.7654, 16.7890, 70.9876, 2.8901, 37.8901},
            {"Palhoca",       "SAO_JOSE_BARREIROS",    59.2345, 10.5678, 15.4321, 72.3456, 2.5678, 39.6789},

            {"Biguacu",       "BIGUACU_BR101_NORTE",   56.9876, 12.1234, 17.2345, 70.1234, 2.9876, 36.9876},
        };

        // delta mensual acumulado sobre el valor base (índice 0 = enero, sin cambio)
        double[][] monthlyDelta = {
            // empF    desemp  evasao  conclus interp  cobrt
            {  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000 }, // ene
            {  1.2340, -0.8901, -1.5678,  0.9234, -0.2341,  2.1234 }, // feb
            {  3.4567, -1.7654, -2.8901,  2.1456, -0.4123,  4.5678 }, // mar
            {  2.1234, -2.5432, -4.1234,  3.4567, -0.6234,  3.2345 }, // abr
            {  5.6789, -1.2345, -5.6789,  4.7890, -0.8901,  6.7890 }, // may
            {  4.3456, -3.4567, -3.2345,  2.3456, -0.5678,  8.9012 }, // jun
            {  7.8901, -0.9876, -6.7890,  5.6789, -1.1234,  5.6789 }, // jul
            {  3.2345, -4.5678, -2.3456,  1.2345, -0.3456,  9.8901 }, // ago
            {  6.5678, -2.1234, -7.8901,  6.5678, -1.3456,  4.3456 }, // sep
            {  1.8901, -5.6789, -1.2345,  0.5678, -0.1234,  7.2345 }, // oct
            {  4.5678, -1.3456, -4.5678,  3.8901, -0.7890,  2.8901 }, // nov
            {  2.3456, -3.2345, -2.1234,  1.7890, -0.4567,  6.1234 }, // dic
        };

        List<TerritorialIndicators> all = new ArrayList<>();
        int seq = 1;

        for (Object[] c : clusters) {
            String municipio  = (String) c[0];
            String cluster    = (String) c[1];
            double baseEmpF   = (double) c[2];
            double baseDesemp = (double) c[3];
            double baseEvasao = (double) c[4];
            double baseConcl  = (double) c[5];
            double baseInter  = (double) c[6];
            double baseCobrt  = (double) c[7];

            for (int m = 0; m < 12; m++) {
                LocalDate ref = LocalDate.of(2024, m + 1, 1);
                double[] d = monthlyDelta[m];

                all.add(build(municipio, cluster, "EMPLEO",       "taxa_emprego_formal",          round(baseEmpF   + d[0]), "%",            String.format("MOCK-EMP-%03d", seq++), ref));
                all.add(build(municipio, cluster, "EMPLEO",       "taxa_desemprego",              round(baseDesemp + d[1]), "%",            String.format("MOCK-EMP-%03d", seq++), ref));
                all.add(build(municipio, cluster, "EDUCACION",    "evasao_escolar",               round(baseEvasao + d[2]), "%",            String.format("MOCK-EDU-%03d", seq++), ref));
                all.add(build(municipio, cluster, "EDUCACION",    "taxa_conclusao_ensino_medio",  round(baseConcl  + d[3]), "%",            String.format("MOCK-EDU-%03d", seq++), ref));
                all.add(build(municipio, cluster, "SALUD_MENTAL", "taxa_internacao_psiquiatrica", round(baseInter  + d[4]), "por 1000 hab", String.format("MOCK-SM-%03d",  seq++), ref));
                all.add(build(municipio, cluster, "SALUD_MENTAL", "cobertura_atencao_basica",     round(baseCobrt  + d[5]), "%",            String.format("MOCK-SM-%03d",  seq++), ref));
            }
        }

        repo.saveAll(all);
    }

    private double round(double value) {
        return Math.round(value * 10000.0) / 10000.0;
    }

    private TerritorialIndicators build(String municipio, String cluster, String categoria,
            String indicador, double valor, String unidad, String codigoOrigem, LocalDate ref) {
        return TerritorialIndicators.builder()
            .municipio(municipio).cluster(cluster).categoria(categoria)
            .indicador(indicador).valor(BigDecimal.valueOf(valor))
            .unidad(unidad).fonte("MOCK").codigoOrigem(codigoOrigem)
            .urlOrigem(null).fechaReferencia(ref).build();
    }
}