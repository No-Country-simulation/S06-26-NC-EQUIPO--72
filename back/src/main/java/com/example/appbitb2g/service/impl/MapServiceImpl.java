package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.repository.ConcentracaoRepository;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.MapService;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
/**
 * Implementación Mock de MapService para la tarea de Endpoints Iniciales.
 *
 */
@Service
public class MapServiceImpl implements MapService {
    //Se inyecta el repositorio para cumplir con las dependencias de Spring,
    // garantizando que IntelliJ no marque la variable como inactiva.
    private final TerritorialIndicatorsRepository territorialIndicatorsRepository;

    public MapServiceImpl(TerritorialIndicatorsRepository territorialIndicatorsRepository) {
        this.territorialIndicatorsRepository = territorialIndicatorsRepository;
    }

    @Override
    public MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio) {

        List<MapIndicadoresResponseDTO.RegionIndicadorRecord> regionesMock = new ArrayList<>();

        // Normalizamos la categoría para evitar errores de mayúsculas/minúsculas
        String categoriaFiltro = (categoria != null) ? categoria.toUpperCase() : "EDUCACION";

        if ("EDUCACION".equals(categoriaFiltro)) {

            // --- REGION 1: SAO_JOSE_KOBRASOL ---
            List<MapIndicadoresResponseDTO.IndicadorDetalleRecord> indicadoresKobrasol = List.of(
                    new MapIndicadoresResponseDTO.IndicadorDetalleRecord(
                            "EDUCACION",
                            "idhm_2010_educacion",
                            new BigDecimal("0.847"),
                            "porcentaje",
                            "IBGE / PNUD",
                            "2010-12-31"
                    )
            );

            regionesMock.add(new MapIndicadoresResponseDTO.RegionIndicadorRecord(
                    "SAO_JOSE_KOBRASOL",
                    "São José",
                    -27.5935,
                    -48.6358,
                    12400,
                    0.72, // 72% de congestión (Alerta Roja)
                    indicadoresKobrasol
            ));

            // --- REGION 2: FLORIANOPOLIS_CENTRO ---
            List<MapIndicadoresResponseDTO.IndicadorDetalleRecord> indicadoresCentro = List.of(
                    new MapIndicadoresResponseDTO.IndicadorDetalleRecord(
                            "EDUCACION",
                            "idhm_2010_educacion",
                            new BigDecimal("0.915"),
                            "porcentaje",
                            "IBGE / PNUD",
                            "2010-12-31"
                    )
            );

            regionesMock.add(new MapIndicadoresResponseDTO.RegionIndicadorRecord(
                    "FLORIANOPOLIS_CENTRO",
                    "Florianópolis",
                    -27.5969,
                    -48.5495,
                    18500,
                    0.42, // 42% de congestión (Alerta Amarilla)
                    indicadoresCentro
            ));

        } else if ("SALUD_MENTAL".equals(categoriaFiltro)) {

            // --- REGION 3: FLORIANOPOLIS_TRINDADE ---
            List<MapIndicadoresResponseDTO.IndicadorDetalleRecord> indicadoresTrindade = List.of(
                    new MapIndicadoresResponseDTO.IndicadorDetalleRecord(
                            "SALUD_MENTAL",
                            "taxa_internacao_psiquiatrica",
                            new BigDecimal("14.2"),
                            "porcentaje",
                            "DATASUS",
                            "2025-12-01"
                    )
            );

            regionesMock.add(new MapIndicadoresResponseDTO.RegionIndicadorRecord(
                    "FLORIANOPOLIS_TRINDADE",
                    "Florianópolis",
                    -27.5862,
                    -48.5152,
                    8200,
                    0.18, // 18% de congestión (Alerta Verde - Señal Limpia)
                    indicadoresTrindade
            ));

        } else {
            // --- REGION 4: FALLBACK GENERAL / EMPLEO ---
            List<MapIndicadoresResponseDTO.IndicadorDetalleRecord> indicadoresBarreiros = List.of(
                    new MapIndicadoresResponseDTO.IndicadorDetalleRecord(
                            "EMPLEO",
                            "taxa_desemprego_municipal",
                            new BigDecimal("8.3"),
                            "porcentaje",
                            "IBGE",
                            "2024-06-30"
                    )
            );

            regionesMock.add(new MapIndicadoresResponseDTO.RegionIndicadorRecord(
                    "SAO_JOSE_BARREIROS",
                    "São José",
                    -27.5642,
                    -48.6189,
                    9400,
                    0.31,
                    indicadoresBarreiros
            ));
        }

        // Retornamos el DTO de respuesta final envuelto en el Record
        return new MapIndicadoresResponseDTO(regionesMock);
    }

    @Override
    public MapResponseDTO obtenerMapa(String periodo, String municipio, String fecha) {
        // Valores por defecto según contrato
        String periodoFinal = (periodo != null && !periodo.isBlank()) ? periodo.toUpperCase() : "TARDE";
        String fechaFinal = (fecha != null && !fecha.isBlank()) ? fecha : LocalDate.now().toString();

        List<MapResponseDTO.MapRegionDTO> regiones = new ArrayList<>();

        regiones.add(new MapResponseDTO.MapRegionDTO(
                "SAO_JOSE_KOBRASOL",
                "São José",
                -27.5935,
                -48.6358,
                12400,
                0.72,
                "LTE",
                34.5,
                periodoFinal,
                fechaFinal
        ));

        regiones.add(new MapResponseDTO.MapRegionDTO(
                "FLORIANOPOLIS_CENTRO",
                "Florianópolis",
                -27.5969,
                -48.5495,
                18500,
                0.42,
                "5G",
                45.2,
                periodoFinal,
                fechaFinal
        ));

        regiones.add(new MapResponseDTO.MapRegionDTO(
                "FLORIANOPOLIS_TRINDADE",
                "Florianópolis",
                -27.5862,
                -48.5152,
                8200,
                0.18,
                "LTE",
                28.1,
                periodoFinal,
                fechaFinal
        ));

        // Filtrar por municipio si se proporciona
        if (municipio != null && !municipio.isBlank() && !municipio.equalsIgnoreCase("todos")) {
            regiones = regiones.stream()
                    .filter(r -> r.municipio().equalsIgnoreCase(municipio))
                    .toList();
        }

        return new MapResponseDTO(regiones);
    }
}
