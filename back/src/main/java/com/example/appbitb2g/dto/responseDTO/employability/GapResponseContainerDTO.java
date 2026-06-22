package com.example.appbitb2g.dto.responseDTO.employability;



import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Contenedor alternativo de brechas y criterio técnico")
public class GapResponseContainerDTO {

    @Schema(description = "Listado de brechas calculadas")
    private List<BrechaDetailDTO> brechas;
    @Schema(description = "Criterio técnico aplicado para el cálculo")
    private CriterioDTO criterio;

   
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Detalle de una brecha territorial")
    public static class BrechaDetailDTO {
        @Schema(description = "Clúster territorial", example = "BIGUACU_BR101_NORTE")
        private String cluster;
        @Schema(description = "Municipio", example = "Biguaçu")
        private String municipio;

        @JsonProperty("n_usuarios")
        @Schema(description = "Cantidad de usuarios", example = "9800")
        private Integer nUsuarios;

        @JsonProperty("congestionamento_medio")
        @Schema(description = "Congestión media", example = "0.81")
        private Double congestionamentoMedio;

        @JsonProperty("rat_type_predominante")
        @Schema(description = "Tipo de red predominante", example = "WCDMA")
        private String ratTypePredominante;

        @JsonProperty("indicador_social")
        @Schema(description = "Indicador social asociado")
        private IndicadorSocialDTO indicadorSocial;

        @JsonProperty("programas_activos")
        @Schema(description = "Programas activos", example = "0")
        private Integer programasActivos;

        @JsonProperty("severidad_brecha")
        @Schema(description = "Severidad de la brecha", example = "ALTA")
        private String severidadBrecha;
    }


    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Indicador social relacionado a la brecha")
    public static class IndicadorSocialDTO {
        @Schema(description = "Categoría del indicador", example = "SALUD_MENTAL")
        private String categoria;
        @Schema(description = "Nombre del indicador", example = "taxa_internacao_psiquiatrica")
        private String indicador;
        @Schema(description = "Valor numérico del indicador", example = "17.4")
        private Double valor;
        @Schema(description = "Unidad de medida", example = "porcentaje")
        private String unidad;
    }


    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "Criterio técnico usado para clasificar la brecha")
    public static class CriterioDTO {
        @Schema(description = "Servicio evaluado", example = "SALUD_MENTAL")
        private String servicio;
        @Schema(description = "Lógica aplicada", example = "congestionamento_medio > 0.6 AND programas_activos = 0")
        private String logica;

        @JsonProperty("umbral_congestionamento")
        @Schema(description = "Umbral de congestión", example = "0.6")
        private Double umbralCongestionamento;
    }
}