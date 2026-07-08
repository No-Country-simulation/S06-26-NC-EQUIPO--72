package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.mentalHealth.ClusterDataDTO;
import com.example.appbitb2g.dto.responseDTO.mentalHealth.ServiceAccessDTO;

public interface MentalHealthService {
	ServiceAccessDTO getAvgServiceAccess();

	ClusterDataDTO getClusterData();
}
