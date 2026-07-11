package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.service.RegionService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RegionServiceImpl implements RegionService {
	private final AntenaRepository antenaRepository;

	public RegionServiceImpl(AntenaRepository antenaRepository) {
		this.antenaRepository = antenaRepository;
	}

	@Override
	public RegionResponseDTO obtenerRegiones() {
		List<RegionResponseDTO.RegionRecord> listaRecords = antenaRepository.obtenerDetallePorMunicipio();
		return new RegionResponseDTO(listaRecords);
	}
}
