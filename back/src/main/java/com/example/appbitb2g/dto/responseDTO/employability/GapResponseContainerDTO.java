package com.example.appbitb2g.dto.responseDTO.employability;



import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GapResponseContainerDTO {

    private List<BrechaDetailDTO> brechas;
    private CriterioDTO criterio;

   
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BrechaDetailDTO {
        private String cluster;
        private String municipio;

        @JsonProperty("n_usuarios")
        private Integer nUsuarios;

        @JsonProperty("congestionamento_medio")
        private Double congestionamentoMedio;

        @JsonProperty("rat_type_predominante")
        private String ratTypePredominante;

        @JsonProperty("indicador_social")
        private IndicadorSocialDTO indicadorSocial;

        @JsonProperty("programas_activos")
        private Integer programasActivos;

        @JsonProperty("severidad_brecha")
        private String severidadBrecha;
    }


    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class IndicadorSocialDTO {
        private String categoria;
        private String indicador;
        private Double valor;
        private String unidad;
    }


    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CriterioDTO {
        private String servicio;
        private String logica;

        @JsonProperty("umbral_congestionamento")
        private Double umbralCongestionamento;
    }
}