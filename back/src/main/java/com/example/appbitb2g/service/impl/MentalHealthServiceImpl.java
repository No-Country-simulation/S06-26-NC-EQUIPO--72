package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.mentalHealth.ClusterDataDTO;
import com.example.appbitb2g.dto.responseDTO.mentalHealth.ClusterDataDTO.CorrelationConnectivityHealthDTO;
import com.example.appbitb2g.dto.responseDTO.mentalHealth.ClusterDataDTO.Metadata;
import com.example.appbitb2g.dto.responseDTO.mentalHealth.ServiceAccessDTO;
import com.example.appbitb2g.enums.CorrelativityGrade;
import com.example.appbitb2g.repository.ConcentracaoRepository;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.MentalHealthService;
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation;
import org.springframework.stereotype.Service;
import tools.jackson.core.type.TypeReference;
import tools.jackson.databind.ObjectMapper;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class MentalHealthServiceImpl implements MentalHealthService {
	private final ObjectMapper objectMapper = new ObjectMapper();

	private final TerritorialIndicatorsRepository territorialIndicatorsRepository;
	private final ConcentracaoRepository concentracaoRepository;

	public MentalHealthServiceImpl(TerritorialIndicatorsRepository territorialIndicatorsRepository,
	                               ConcentracaoRepository concentracaoRepository) {
		this.territorialIndicatorsRepository = territorialIndicatorsRepository;
		this.concentracaoRepository = concentracaoRepository;
	}

	@Override
	public ServiceAccessDTO getAvgServiceAccess() {
		final String INDICATOR = "taxa_internacao_psiquiatrica";
		return objectMapper.readValue(
				territorialIndicatorsRepository.getAvgHealthCoverageByIndicator(INDICATOR), // raw JSON
				ServiceAccessDTO.class
		);
	}

	@Override
	public ClusterDataDTO getClusterData() {
		String rawData = concentracaoRepository.getConnectivityHealthCorrelation();
		List<CorrelationConnectivityHealthDTO> data = objectMapper
				.readValue(rawData, new TypeReference<>() {
				});
		// add grade to each record
		data = data.stream()
				.map(c -> new CorrelationConnectivityHealthDTO(
						c.cluster(),
						c.connectivityPercentage(),
						c.healthValue(),
						getCorrelativityGrade(c.connectivityPercentage(), c.healthValue())
				))
				.collect(Collectors.toList());

		// calculate correlation using Pearson's correlation coefficient
		double[] xAxis = data.stream().mapToDouble(CorrelationConnectivityHealthDTO::connectivityPercentage).toArray();
		double[] yAxis = data.stream().mapToDouble(CorrelationConnectivityHealthDTO::healthValue).toArray();

		PearsonsCorrelation pearson = new PearsonsCorrelation();
		double r = Math.round(pearson.correlation(xAxis, yAxis) * 100.0) / 100.0;

		return new ClusterDataDTO(
				new Metadata(r, correlationAssessment(r)),
				data,
				data.size()
		);
	}

	private CorrelativityGrade getCorrelativityGrade(double connectivityPercentage, double healthValue) {
		if (connectivityPercentage < 40.0 || healthValue < 2.5) return CorrelativityGrade.RED;
		if (connectivityPercentage > 70.0 && healthValue > 4.0) return CorrelativityGrade.GREEN;
		return CorrelativityGrade.YELLOW;
	}

	private String correlationAssessment(double r) {
		double absR = Math.abs(r);
		if (absR >= 0.8) return "correlación muy fuerte";
		if (absR >= 0.6) return "correlación fuerte";
		if (absR >= 0.4) return "correlación moderada";
		if (absR >= 0.2) return "correlación débil";
		return "sin correlación aparente";
	}
}
