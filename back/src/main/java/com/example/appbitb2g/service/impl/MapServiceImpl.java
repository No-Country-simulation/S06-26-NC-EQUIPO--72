package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
import com.example.appbitb2g.dto.responseDTO.territorialIndicator.IndicadorEvolucionResponseDTO;
import com.example.appbitb2g.enums.ServiceType;
import com.example.appbitb2g.exception.BadRequestException;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.repository.ConcentracaoRepository;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.MapService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tools.jackson.databind.ObjectMapper;

import java.time.LocalDate;
import java.util.List;

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
	private final ConcentracaoRepository concentracaoRepository;
	private final ObjectMapper objectMapper;

	public MapServiceImpl(AntenaRepository antenaRepository,
	                      TerritorialIndicatorsRepository territorialIndicatorsRepository,
	                      ConcentracaoRepository concentracaoRepository,
	                      ObjectMapper objectMapper) {
		this.antenaRepository = antenaRepository;
		this.territorialIndicatorsRepository = territorialIndicatorsRepository;
		this.concentracaoRepository = concentracaoRepository;
		this.objectMapper = objectMapper;
	}

	@Override
	@Transactional(readOnly = true)
	public MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio) {
		if (categoria == null || ServiceType.fromString(categoria) == null) {
			throw new BadRequestException(
					"FILTRO_INVALIDO",
					"El valor de Categoria debe ser SALUD_MENTAL / EMPLEO / EDUCACION");
		}

		try {
			String rawJson = territorialIndicatorsRepository.getIndicatorsRawJson(categoria, indicador, municipio);
			return objectMapper.readValue(rawJson, MapIndicadoresResponseDTO.class);
		} catch (Exception e) {
			throw new RuntimeException("Error al parsear el JSON por categoría", e);
		}
	}

	@Override
	public MapResponseDTO obtenerMapa(String periodo, String municipio, String fecha) {
		// Si los filtros vienen vacion de Front asignamos valores por defecto
		String periodoFinal = (periodo != null && !periodo.isBlank()) ? periodo.toUpperCase() : "TARDE";
		LocalDate fechaFinal = (fecha != null && !fecha.isBlank())
				? LocalDate.parse(fecha)
				: concentracaoRepository.findMaxDayDate();

		// 2. Si dice "todos", mandamos null para que la query desactive el filtro de municipio
		String filtroMunicipio = (municipio != null && !municipio.equalsIgnoreCase("todos")) ? municipio : null;

		// 3. Llamamos a tu repositorio real que calcula promedios geográficos y de tráfico
		List<MapResponseDTO.MapRegionDTO> regionesReales =
				antenaRepository.obtenerDatosMapaPrincipal(periodoFinal, filtroMunicipio, fechaFinal);

		// Envolvemos la lista real en el DTO final y se lo mandamos al Frontend
		return new MapResponseDTO(regionesReales);
	}

	@Override
	@Transactional(readOnly = true)
	public IndicadorEvolucionResponseDTO obtenerEvolucionIndicador(String categoria, String indicador, String municipio) {
		if (categoria == null || ServiceType.fromString(categoria) == null) {
			throw new BadRequestException(
					"FILTRO_INVALIDO",
					"El valor de Categoria debe ser SALUD_MENTAL / EMPLEO / EDUCACION");
		}

		// Establecer indicador por defecto si no viene
		String indicadorFinal = indicador;
		if (indicadorFinal == null || indicadorFinal.isBlank()) {
			indicadorFinal = switch (categoria.toUpperCase()) {
				case "EMPLEO" -> "taxa_emprego_formal";
				case "SALUD_MENTAL" -> "taxa_internacao_psiquiatrica";
				case "EDUCACION" -> "idhm_2010_educacion";
				default -> null;
			};
		}

		try {
			String rawJson = territorialIndicatorsRepository.getIndicatorEvolutionRawJson(categoria, indicadorFinal, municipio);
			return objectMapper.readValue(rawJson, IndicadorEvolucionResponseDTO.class);
		} catch (Exception e) {
			throw new RuntimeException("Error al parsear el JSON de evolución del indicador", e);
		}
	}
}
