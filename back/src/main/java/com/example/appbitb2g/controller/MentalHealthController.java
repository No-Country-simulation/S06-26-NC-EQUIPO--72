package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.mentalHealth.ServiceAccessDTO;
import com.example.appbitb2g.service.MentalHealthService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/mental-health")
public class MentalHealthController {
	private final MentalHealthService mentalHealthService;

	public MentalHealthController(MentalHealthService mentalHealthService) {
		this.mentalHealthService = mentalHealthService;
	}

	@GetMapping("/avg-service-access")
	public ResponseEntity<ServiceAccessDTO> getAvgServiceAccess() {
		return ResponseEntity.ok(mentalHealthService.getAvgServiceAccess());
	}
}
