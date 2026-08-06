package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.ResumeRequestDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;

public interface DataService {
    AiQueryResponseDTO aiQueryAgent(AiQueryRequestDTO requestDto);

    AiQueryResponseDTO resumirConsulta(ResumeRequestDTO requestDto);
}
