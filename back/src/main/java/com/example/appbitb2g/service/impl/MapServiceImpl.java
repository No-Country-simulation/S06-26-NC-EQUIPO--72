package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.repository.ConcentracaoRepository;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.MapService;

import tools.jackson.databind.ObjectMapper;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
import com.example.appbitb2g.exception.BadRequestException;

/**
 * Implementación Mock de MapService para la tarea de Endpoints Iniciales.
 *
 */
@Service
public class MapServiceImpl implements MapService {
        // Se inyecta el repositorio para cumplir con las dependencias de Spring,
        // garantizando que IntelliJ no marque la variable como inactiva.
        private final TerritorialIndicatorsRepository territorialIndicatorsRepository;
        private final ObjectMapper objectMapper;
          private static final Set<String> CATEGORIAS_VALIDAS = Set.of("SALUD_MENTAL", "EDUCACION", "EMPLEO");

        public MapServiceImpl(TerritorialIndicatorsRepository territorialIndicatorsRepository,
                        ObjectMapper objectMapper) {
                this.territorialIndicatorsRepository = territorialIndicatorsRepository;
                this.objectMapper = objectMapper;
        }

        @Override
        @Transactional(readOnly = true)
        public MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio) {
              
                
               
                if (categoria==null || !CATEGORIAS_VALIDAS.contains(categoria.toUpperCase())) {
                        throw new BadRequestException(
                                        "El valor de Categoria debe ser SALUD_MENTAL / EMPLEO / EDUCACION");
                }

                try {

                        String rawJson = territorialIndicatorsRepository.getIndicatorsRawJson(categoria, indicador,
                                        municipio);

                        return objectMapper.readValue(rawJson, MapIndicadoresResponseDTO.class);

                } catch (Exception e) {
                        throw new RuntimeException("Error al parsear el JSON por categoría", e);
                }

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
                                fechaFinal));

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
                                fechaFinal));

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
                                fechaFinal));

                // Filtrar por municipio si se proporciona
                if (municipio != null && !municipio.isBlank() && !municipio.equalsIgnoreCase("todos")) {
                        regiones = regiones.stream()
                                        .filter(r -> r.municipio().equalsIgnoreCase(municipio))
                                        .toList();
                }

                return new MapResponseDTO(regiones);
        }
}
