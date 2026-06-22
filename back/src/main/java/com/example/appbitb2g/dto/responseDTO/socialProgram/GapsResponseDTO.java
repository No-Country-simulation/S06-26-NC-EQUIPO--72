package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.util.List;

@Schema(description = "Respuesta con brechas territoriales y criterio técnico")
public record GapsResponseDTO(
        @JsonProperty("brechas") List<BrechaDetalleRecord> brechas,
        @JsonProperty("criterio") CriterioRecord criterio
) {
    /**
     * Representa la información detallada de la brecha calculada en un clúster.
     */
    @Schema(description = "Detalle de una brecha territorial")
    public record BrechaDetalleRecord(
            @Schema(description = "Clúster territorial", example = "BIGUACU_BR101_NORTE")
            String cluster,
            @Schema(description = "Municipio", example = "Biguaçu")
            String municipio,
            @Schema(description = "Cantidad de usuarios", example = "9800")
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @Schema(description = "Congestión media", example = "0.81")
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            @Schema(description = "Tipo de red predominante", example = "WCDMA")
            @JsonProperty("rat_type_predominante") String ratTypePredominante,
            @Schema(description = "Indicador social asociado")
            @JsonProperty("indicador_social") IndicadorSocialRecord indicadorSocial,
            @Schema(description = "Cantidad de programas activos", example = "0")
            @JsonProperty("programas_activos") Integer programasActivos,
            @Schema(description = "Severidad de la brecha", example = "ALTA")
            @JsonProperty("severidad_brecha") String severidadBrecha
    ) {}

    /**
     * Representa el desglose del indicador social asociado al clúster analizado.
     */
    @Schema(description = "Indicador social asociado a la brecha")
    public record IndicadorSocialRecord(
            @Schema(description = "Categoría del indicador", example = "SALUD_MENTAL")
            String categoria,
            @Schema(description = "Nombre del indicador", example = "taxa_internacao_psiquiatrica")
            String indicador,
            @Schema(description = "Valor del indicador", example = "17.4")
            BigDecimal valor, // Mantiene la precisión decimal exacta (ej: 17.4)
            @Schema(description = "Unidad de medida", example = "porcentaje")
            String unidad
    ) {}

    /**
     * Contiene las reglas del criterio técnico de corte de congestión de red.
     */
    @Schema(description = "Criterio técnico utilizado para evaluar la brecha")
    public record CriterioRecord(
            @Schema(description = "Servicio evaluado", example = "SALUD_MENTAL")
            String servicio,
            @Schema(description = "Lógica de evaluación", example = "congestionamento_medio > 0.6 AND programas_activos = 0")
            String logica,
            @Schema(description = "Umbral de congestión", example = "0.6")
            @JsonProperty("umbral_congestionamento") Double umbralCongestionamento
    ) {}
}
