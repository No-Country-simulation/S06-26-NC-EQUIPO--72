package com.example.appbitb2g.dto.responseDTO.territorialIndicator;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.util.List;

/**
 * Record inmutable que define la estructura exacta del contrato JSON
 * exigido por el Frontend para GET /indicadores/evolucion.
 */
@Schema(description = "Respuesta con la evolución temporal de un indicador territorial")
public record IndicadorEvolucionResponseDTO(
        @Schema(description = "Nombre del indicador", example = "taxa_emprego_formal")
        String indicador,
        @Schema(description = "Categoría del indicador", example = "EMPLEO")
        String categoria,
        @Schema(description = "Evolución temporal del indicador")
        List<EvolucionDetalleRecord> evolucion
) {

    /**
     * Record anidado para representar un punto de datos en la evolución temporal.
     */
    @Schema(description = "Detalle de un punto de datos en la evolución")
    public record EvolucionDetalleRecord(
            @Schema(description = "Fecha de referencia", example = "2024-01-01")
            @JsonProperty("fecha_referencia") String fechaReferencia,
            @Schema(description = "Valor promedio del indicador en esa fecha", example = "63.45")
            @JsonProperty("valor_promedio") BigDecimal valorPromedio
    ) {}

}
