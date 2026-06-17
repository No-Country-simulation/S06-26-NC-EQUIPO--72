package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.util.List;

public record GapsResponseDTO(
        @JsonProperty("brechas") List<BrechaDetalleRecord> brechas,
        @JsonProperty("criterio") CriterioRecord criterio
) {
    /**
     * Representa la información detallada de la brecha calculada en un clúster.
     */
    public record BrechaDetalleRecord(
            String cluster,
            String municipio,
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            @JsonProperty("rat_type_predominante") String ratTypePredominante,
            @JsonProperty("indicador_social") IndicadorSocialRecord indicadorSocial,
            @JsonProperty("programas_activos") Integer programasActivos,
            @JsonProperty("severidad_brecha") String severidadBrecha
    ) {}

    /**
     * Representa el desglose del indicador social asociado al clúster analizado.
     */
    public record IndicadorSocialRecord(
            String categoria,
            String indicador,
            BigDecimal valor, // Mantiene la precisión decimal exacta (ej: 17.4)
            String unidad
    ) {}

    /**
     * Contiene las reglas del criterio técnico de corte de congestión de red.
     */
    public record CriterioRecord(
            String servicio,
            String logica,
            @JsonProperty("umbral_congestionamento") Double umbralCongestionamento
    ) {}
}
