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
        private final AntenaRepository antenaRepository;
        private final TerritorialIndicatorsRepository territorialIndicatorsRepository;
        private final ObjectMapper objectMapper;
          private static final Set<String> CATEGORIAS_VALIDAS = Set.of("SALUD_MENTAL", "EDUCACION", "EMPLEO");

        public MapServiceImpl(AntenaRepository antenaRepository, TerritorialIndicatorsRepository territorialIndicatorsRepository,
                              ObjectMapper objectMapper) {
            this.antenaRepository = antenaRepository;
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
                // Si los filtros vienen vacion de Front asignamos valores por defecto
                String periodoFinal = (periodo != null && !periodo.isBlank()) ? periodo.toUpperCase() : "TARDE";
                String fechaFinal = (fecha != null && !fecha.isBlank()) ? fecha : LocalDate.now().toString();
                // 2. Si dice "todos", mandamos null para que la query desactive el filtro de municipio
                String filtroMunicipio = (municipio!= null && !municipio.equalsIgnoreCase("todos"))? municipio : null;

                // 3. Llamamos a tu repositorio real que calcula promedios geográficos y de tráfico

                List<MapResponseDTO.MapRegionDTO> regionesReales= antenaRepository.obtenerDatosMapaPrincipal(periodoFinal,filtroMunicipio,fechaFinal);

                // Envolvemos la lista real en el DTO final y se lo mandamos al Frontend
                return new MapResponseDTO(regionesReales);
        }
}
