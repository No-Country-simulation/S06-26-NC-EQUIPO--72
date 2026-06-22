package com.example.appbitb2g.dto.responseDTO.socialProgram;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

import java.math.BigDecimal;
import java.util.List;

/**
 * Record inmutable que define la estructura exacta del contrato JSON
 * exigido por el Frontend para GET /mapa/indicadores.
 */
@Schema(description = "Respuesta de indicadores por región para el mapa")
public record MapIndicadoresResponseDTO(
        @JsonProperty("regiones") List<RegionIndicadorRecord> regiones

 ){

    /**
     * Record anidado para representar cada región en el mapa.
     */

    @Schema(description = "Detalle de una región con sus indicadores")
    public record RegionIndicadorRecord(
            @Schema(description = "Clúster territorial", example = "SAO_JOSE_KOBRASOL")
            String cluster,
            @Schema(description = "Municipio", example = "São José")
            String municipio,
            @Schema(description = "Latitud", example = "-27.5935")
            Double lat,
            @Schema(description = "Longitud", example = "-48.6358")
            Double lon,
            @Schema(description = "Cantidad de usuarios", example = "12400")
            @JsonProperty("n_usuarios") Integer nUsuarios,
            @Schema(description = "Congestión media", example = "0.72")
            @JsonProperty("congestionamento_medio") Double congestionamentoMedio,
            @Schema(description = "Lista de indicadores asociados")
            List<IndicadorDetalleRecord> indicadores
    ) {}

    /**
     * Record anidado para representar el desglose detallado de un indicador territorial.
     */

    @Schema(description = "Detalle de un indicador territorial")
    public record IndicadorDetalleRecord(
            @Schema(description = "Categoría del indicador", example = "EDUCACION")
            String categoria,
            @Schema(description = "Nombre del indicador", example = "idhm_2010_educacion")
            String indicador,
            @Schema(description = "Valor del indicador", example = "0.847")
            BigDecimal valor,
            @Schema(description = "Unidad de medida", example = "porcentaje")
            String unidad,
            @Schema(description = "Fuente de referencia", example = "IBGE / PNUD")
            @JsonProperty("fonte") String fonte,
            @Schema(description = "Fecha de referencia", example = "2010-12-31")
            @JsonProperty("fecha_referencia") String fechaReferencia
    ) {}
}
