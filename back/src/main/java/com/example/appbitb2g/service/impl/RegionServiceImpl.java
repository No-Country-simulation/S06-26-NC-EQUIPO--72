package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.repository.AntenaRepository;
import com.example.appbitb2g.service.RegionService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RegionServiceImpl implements RegionService {

    private final AntenaRepository antenaRepository;

    public RegionServiceImpl(AntenaRepository antenaRepository) {
        this.antenaRepository = antenaRepository;
    }

    @Override
    public RegionResponseDTO obtenerRegiones() {
        List<RegionResponseDTO.RegionRecord> regiones = new ArrayList<>();

        regiones.add(new RegionResponseDTO.RegionRecord(
                "SAO_JOSE_KOBRASOL",
                "Sao Jose",
                -27.5935,
                -48.6358,
                7
        ));

        regiones.add(new RegionResponseDTO.RegionRecord(
                "FLORIANOPOLIS_CENTRO",
                "Florianópolis",
                -27.5969,
                -48.5495,
                10
        ));

        regiones.add(new RegionResponseDTO.RegionRecord(
                "FLORIANOPOLIS_TRINDADE",
                "Florianópolis",
                -27.5862,
                -48.5152,
                5
        ));

        regiones.add(new RegionResponseDTO.RegionRecord(
                "SAO_JOSE_BARREIROS",
                "São José",
                -27.5642,
                -48.6189,
                6
        ));

        return new RegionResponseDTO(regiones);
    }
}
