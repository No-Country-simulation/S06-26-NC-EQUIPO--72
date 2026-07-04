package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import com.example.appbitb2g.enums.DayPeriod;
import com.example.appbitb2g.enums.ServiceType;
import com.example.appbitb2g.exception.BadRequestException;
import com.example.appbitb2g.repository.GapsDashboardRepository;
import com.example.appbitb2g.service.BrechasService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BrechaServiceImpl implements BrechasService {
	private final GapsDashboardRepository gapsDashboardRepository;



	public BrechaServiceImpl(GapsDashboardRepository gapsDashboardRepository) {
		this.gapsDashboardRepository = gapsDashboardRepository;
	}

	@Override
	public GapsResponseDTO analizarBrechas(String servicio, String municipio, String periodo, String incomeCluster) {
		if (servicio == null || servicio.isBlank() || servicio.trim().isEmpty()) {
			throw new BadRequestException("El parámetro 'servicio' es obligatorio en la consulta.");
		}

		// normalización parámetros 'servicio' y 'periodo'
		servicio = servicio.toUpperCase();
		periodo = (periodo != null && !periodo.isBlank()) ? periodo.toUpperCase() : "TARDE"; // por defecto TARDE

		if (ServiceType.fromString(servicio) == null) {
			throw new BadRequestException(
					"El valor de 'servicio' debe ser MENTORIA / FORMACION / EXPERIENCIA / SALUD_MENTAL / EMPLEO"
			);
		}

		if (DayPeriod.fromString(periodo) == null) {
			throw new BadRequestException("El valor de 'periodo' debe ser MADRUGADA / MANHA / TARDE / NOITE.");
		}

		GapsResponseDTO.CriterioRecord criteria = new GapsResponseDTO.CriterioRecord(
			servicio,
			"n_usuarios > " + GapsDashboardRepository.UMBRAL_USUARIOS + " AND programas_activos = 0",
			GapsDashboardRepository.UMBRAL_CONGESTIONAMENTO
		);




		List<GapsResponseDTO.BrechaDetalleRecord> gapsDetails = gapsDashboardRepository
				.getGapsByCriteria(servicio, municipio, periodo, incomeCluster);

		return new GapsResponseDTO(gapsDetails, criteria);
	}
}

