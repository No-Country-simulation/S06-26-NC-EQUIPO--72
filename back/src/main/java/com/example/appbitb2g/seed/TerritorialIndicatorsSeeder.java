package com.example.appbitb2g.seed;

import com.example.appbitb2g.model.TerritorialIndicators;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Component
@Profile("dev")
public class TerritorialIndicatorsSeeder {

    @Autowired private TerritorialIndicatorsRepository repo;

    public void seed() {
        if (repo.count() > 0) return;

        LocalDate ref = LocalDate.of(2024, 1, 1);

        repo.saveAll(List.of(
            build("Florianopolis","SC401_CORREDOR","EMPLEO","taxa_emprego_formal",65.4321,"%","MOCK-EMP-001",ref),
            build("Florianopolis","SC401_CORREDOR","EMPLEO","taxa_desemprego",8.7654,"%","MOCK-EMP-002",ref),
            build("Florianopolis","SC401_CORREDOR","EDUCACION","evasao_escolar",12.3456,"%","MOCK-EDU-001",ref),
            build("Florianopolis","SC401_CORREDOR","EDUCACION","taxa_conclusao_ensino_medio",78.9012,"%","MOCK-EDU-002",ref),
            build("Florianopolis","SC401_CORREDOR","SALUD_MENTAL","taxa_internacao_psiquiatrica",2.1234,"por 1000 hab","MOCK-SM-001",ref),
            build("Florianopolis","SC401_CORREDOR","SALUD_MENTAL","cobertura_atencao_basica",45.6789,"%","MOCK-SM-002",ref),

            build("Florianopolis","ESTREITO_CAPOEIRAS","EMPLEO","taxa_emprego_formal",60.1234,"%","MOCK-EMP-003",ref),
            build("Florianopolis","ESTREITO_CAPOEIRAS","EMPLEO","taxa_desemprego",9.8765,"%","MOCK-EMP-004",ref),
            build("Florianopolis","ESTREITO_CAPOEIRAS","EDUCACION","evasao_escolar",14.5678,"%","MOCK-EDU-003",ref),
            build("Florianopolis","ESTREITO_CAPOEIRAS","EDUCACION","taxa_conclusao_ensino_medio",75.4321,"%","MOCK-EDU-004",ref),
            build("Florianopolis","ESTREITO_CAPOEIRAS","SALUD_MENTAL","taxa_internacao_psiquiatrica",2.5678,"por 1000 hab","MOCK-SM-003",ref),
            build("Florianopolis","ESTREITO_CAPOEIRAS","SALUD_MENTAL","cobertura_atencao_basica",42.3456,"%","MOCK-SM-004",ref),

            build("Florianopolis","NORTE_ILHA","EMPLEO","taxa_emprego_formal",70.9876,"%","MOCK-EMP-005",ref),
            build("Florianopolis","NORTE_ILHA","EMPLEO","taxa_desemprego",7.1234,"%","MOCK-EMP-006",ref),
            build("Florianopolis","NORTE_ILHA","EDUCACION","evasao_escolar",10.9876,"%","MOCK-EDU-005",ref),
            build("Florianopolis","NORTE_ILHA","EDUCACION","taxa_conclusao_ensino_medio",82.3456,"%","MOCK-EDU-006",ref),
            build("Florianopolis","NORTE_ILHA","SALUD_MENTAL","taxa_internacao_psiquiatrica",1.9876,"por 1000 hab","MOCK-SM-005",ref),
            build("Florianopolis","NORTE_ILHA","SALUD_MENTAL","cobertura_atencao_basica",48.7654,"%","MOCK-SM-006",ref),

            build("Florianopolis","TRINDADE","EMPLEO","taxa_emprego_formal",75.4321,"%","MOCK-EMP-007",ref),
            build("Florianopolis","TRINDADE","EMPLEO","taxa_desemprego",6.5432,"%","MOCK-EMP-008",ref),
            build("Florianopolis","TRINDADE","EDUCACION","evasao_escolar",9.1234,"%","MOCK-EDU-007",ref),
            build("Florianopolis","TRINDADE","EDUCACION","taxa_conclusao_ensino_medio",86.7890,"%","MOCK-EDU-008",ref),
            build("Florianopolis","TRINDADE","SALUD_MENTAL","taxa_internacao_psiquiatrica",1.7654,"por 1000 hab","MOCK-SM-007",ref),
            build("Florianopolis","TRINDADE","SALUD_MENTAL","cobertura_atencao_basica",52.3456,"%","MOCK-SM-008",ref),

            build("Florianopolis","UFSC","EMPLEO","taxa_emprego_formal",80.1234,"%","MOCK-EMP-009",ref),
            build("Florianopolis","UFSC","EMPLEO","taxa_desemprego",5.6789,"%","MOCK-EMP-010",ref),
            build("Florianopolis","UFSC","EDUCACION","evasao_escolar",7.6543,"%","MOCK-EDU-009",ref),
            build("Florianopolis","UFSC","EDUCACION","taxa_conclusao_ensino_medio",90.1234,"%","MOCK-EDU-010",ref),
            build("Florianopolis","UFSC","SALUD_MENTAL","taxa_internacao_psiquiatrica",1.5432,"por 1000 hab","MOCK-SM-009",ref),
            build("Florianopolis","UFSC","SALUD_MENTAL","cobertura_atencao_basica",55.6789,"%","MOCK-SM-010",ref),

            build("Florianopolis","CANASVIEIRAS","EMPLEO","taxa_emprego_formal",68.7654,"%","MOCK-EMP-011",ref),
            build("Florianopolis","CANASVIEIRAS","EMPLEO","taxa_desemprego",8.2345,"%","MOCK-EMP-012",ref),
            build("Florianopolis","CANASVIEIRAS","EDUCACION","evasao_escolar",11.4567,"%","MOCK-EDU-011",ref),
            build("Florianopolis","CANASVIEIRAS","EDUCACION","taxa_conclusao_ensino_medio",79.5678,"%","MOCK-EDU-012",ref),
            build("Florianopolis","CANASVIEIRAS","SALUD_MENTAL","taxa_internacao_psiquiatrica",2.0123,"por 1000 hab","MOCK-SM-011",ref),
            build("Florianopolis","CANASVIEIRAS","SALUD_MENTAL","cobertura_atencao_basica",47.8901,"%","MOCK-SM-012",ref),

            build("Florianopolis","AEROPORTO_HLZ","EMPLEO","taxa_emprego_formal",72.3456,"%","MOCK-EMP-013",ref),
            build("Florianopolis","AEROPORTO_HLZ","EMPLEO","taxa_desemprego",7.5678,"%","MOCK-EMP-014",ref),
            build("Florianopolis","AEROPORTO_HLZ","EDUCACION","evasao_escolar",10.1234,"%","MOCK-EDU-013",ref),
            build("Florianopolis","AEROPORTO_HLZ","EDUCACION","taxa_conclusao_ensino_medio",81.2345,"%","MOCK-EDU-014",ref),
            build("Florianopolis","AEROPORTO_HLZ","SALUD_MENTAL","taxa_internacao_psiquiatrica",1.8765,"por 1000 hab","MOCK-SM-013",ref),
            build("Florianopolis","AEROPORTO_HLZ","SALUD_MENTAL","cobertura_atencao_basica",49.1234,"%","MOCK-SM-014",ref),

            build("Florianopolis","CBD_BEIRAMAR","EMPLEO","taxa_emprego_formal",78.9012,"%","MOCK-EMP-015",ref),
            build("Florianopolis","CBD_BEIRAMAR","EMPLEO","taxa_desemprego",5.9876,"%","MOCK-EMP-016",ref),
            build("Florianopolis","CBD_BEIRAMAR","EDUCACION","evasao_escolar",8.7654,"%","MOCK-EDU-015",ref),
            build("Florianopolis","CBD_BEIRAMAR","EDUCACION","taxa_conclusao_ensino_medio",87.6543,"%","MOCK-EDU-016",ref),
            build("Florianopolis","CBD_BEIRAMAR","SALUD_MENTAL","taxa_internacao_psiquiatrica",1.6543,"por 1000 hab","MOCK-SM-015",ref),
            build("Florianopolis","CBD_BEIRAMAR","SALUD_MENTAL","cobertura_atencao_basica",53.4567,"%","MOCK-SM-016",ref),

            build("Florianopolis","RESIDENCIAL_NORTE","EMPLEO","taxa_emprego_formal",66.5432,"%","MOCK-EMP-017",ref),
            build("Florianopolis","RESIDENCIAL_NORTE","EMPLEO","taxa_desemprego",8.9012,"%","MOCK-EMP-018",ref),
            build("Florianopolis","RESIDENCIAL_NORTE","EDUCACION","evasao_escolar",13.2345,"%","MOCK-EDU-017",ref),
            build("Florianopolis","RESIDENCIAL_NORTE","EDUCACION","taxa_conclusao_ensino_medio",77.8901,"%","MOCK-EDU-018",ref),
            build("Florianopolis","RESIDENCIAL_NORTE","SALUD_MENTAL","taxa_internacao_psiquiatrica",2.2345,"por 1000 hab","MOCK-SM-017",ref),
            build("Florianopolis","RESIDENCIAL_NORTE","SALUD_MENTAL","cobertura_atencao_basica",44.5678,"%","MOCK-SM-018",ref),

            build("Sao Jose","SAO_JOSE_KOBRASOL","EMPLEO","taxa_emprego_formal",62.3456,"%","MOCK-EMP-019",ref),
            build("Sao Jose","SAO_JOSE_KOBRASOL","EMPLEO","taxa_desemprego",9.4567,"%","MOCK-EMP-020",ref),
            build("Sao Jose","SAO_JOSE_KOBRASOL","EDUCACION","evasao_escolar",13.8765,"%","MOCK-EDU-019",ref),
            build("Sao Jose","SAO_JOSE_KOBRASOL","EDUCACION","taxa_conclusao_ensino_medio",76.1234,"%","MOCK-EDU-020",ref),
            build("Sao Jose","SAO_JOSE_KOBRASOL","SALUD_MENTAL","taxa_internacao_psiquiatrica",2.3456,"por 1000 hab","MOCK-SM-019",ref),
            build("Sao Jose","SAO_JOSE_KOBRASOL","SALUD_MENTAL","cobertura_atencao_basica",41.2345,"%","MOCK-SM-020",ref)
        ));
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