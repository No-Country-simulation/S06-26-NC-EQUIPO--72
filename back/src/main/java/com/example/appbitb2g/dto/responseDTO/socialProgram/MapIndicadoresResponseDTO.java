package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.math.BigDecimal;
import java.util.List;

/**
 * Record inmutable que define la estructura exacta del contrato JSON
 * exigido por el Frontend para GET /mapa/indicadores.
 */
public record MapIndicadoresResponseDTO(
        @JsonProperty("regiones") List<RegionIndicadorRecord> regiones

 ){

    /**
     * Record anidado para representar cada región en el mapa.
     */

    public record RegionIndicadorRecord(
            String cluster,
            String municipio,
            Double lat,
            Double lon,
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            List<IndicadorDetalleRecord> indicadores
    ) {}

    /**
     * Record anidado para representar el desglose detallado de un indicador territorial.
     */

    public record IndicadorDetalleRecord(
            String categoria,
            String indicador,
            BigDecimal valor,
            String unidad,
            @JsonProperty("fonte") String fonte,
            @JsonProperty("fecha_referencia") String fechaReferencia
    ) {}
}
