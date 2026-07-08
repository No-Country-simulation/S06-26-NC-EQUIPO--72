package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.mentalHealth.ServiceAccessDTO;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.MentalHealthService;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

@Service
public class MentalHealthServiceImpl implements MentalHealthService {
	private final ObjectMapper objectMapper = new ObjectMapper();

	private final TerritorialIndicatorsRepository territorialIndicatorsRepository;

	public MentalHealthServiceImpl(TerritorialIndicatorsRepository territorialIndicatorsRepository) {
		this.territorialIndicatorsRepository = territorialIndicatorsRepository;
	}

	@Override
	public ServiceAccessDTO getAvgServiceAccess() {
		final String INDICATOR = "taxa_internacao_psiquiatrica";
		return objectMapper.readValue(
				territorialIndicatorsRepository.getAvgHealthCoverageByIndicator(INDICATOR), // raw JSON
				ServiceAccessDTO.class
		);
	}
}
