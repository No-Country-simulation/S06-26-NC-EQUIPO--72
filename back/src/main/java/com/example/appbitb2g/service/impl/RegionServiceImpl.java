package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.mapper.RegionesMapper;
import com.example.appbitb2g.model.Antenna;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.service.RegionService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RegionServiceImpl implements RegionService {

    private final AntenaRepository antenaRepository;
    private final RegionesMapper regionesMapper;

    public RegionServiceImpl(AntenaRepository antenaRepository, RegionesMapper regionesMapper) {
        this.antenaRepository = antenaRepository;
        this.regionesMapper = regionesMapper;
    }

    @Override
    public RegionResponseDTO obtenerRegiones() {

        List<Antenna> antenas = antenaRepository.findAll();

        List<RegionResponseDTO.RegionRecord> listaRecords = regionesMapper.toRegionRecordList(antenas);

        return new RegionResponseDTO(listaRecords);
    }
}
