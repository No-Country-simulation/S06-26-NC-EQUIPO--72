package com.example.appbitb2g.dto.responseDTO.mentalHealth;

import com.example.appbitb2g.enums.CorrelativityGrade;

import java.util.List;

public record ClusterDataDTO(
		Metadata metadata,
		List<CorrelationConnectivityHealthDTO> data,
		int records
) {
	public record Metadata(
			double pearsonCorrelation,
			String interpretation
	) {}

	public record CorrelationConnectivityHealthDTO(
			String cluster,
			double connectivityPercentage,
			double healthValue,
			CorrelativityGrade grade
	) {}
}
