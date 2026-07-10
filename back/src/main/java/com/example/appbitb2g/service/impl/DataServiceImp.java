package com.example.appbitb2g.service.impl;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.example.appbitb2g.config.Config;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiServiceRequestDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiServiceResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.FountainDTO;
import com.example.appbitb2g.exception.IrrelevantQueryException;
import com.example.appbitb2g.service.DataService;

@Service
public class DataServiceImp implements DataService {
    private final RestTemplate restTemplate;
    private final Config config;

    public DataServiceImp(RestTemplate restTemplate, Config config) {
        this.restTemplate = restTemplate;
        this.config = config;
    }

    @Override
    public AiQueryResponseDTO aiQueryAgent(AiQueryRequestDTO requestDto) {
        // Llamar al servicio de IA
        String aiUrl = config.getAiServiceUrl() + "/consulta";
        AiServiceRequestDTO aiRequest = new AiServiceRequestDTO(
                requestDto.consulta(),
                requestDto.idioma() != null ? requestDto.idioma() : "es"
        );

        AiServiceResponseDTO aiResponse = restTemplate.postForObject(
                aiUrl, aiRequest, AiServiceResponseDTO.class);

        return new AiQueryResponseDTO(
                aiResponse.respuesta_ia(),
                aiResponse.visualizacion_sugerida(),
                aiResponse.datos(),
                aiResponse.fuentes(),
                aiResponse.datos().size(),
                aiResponse.idioma()
        );
    }
}
