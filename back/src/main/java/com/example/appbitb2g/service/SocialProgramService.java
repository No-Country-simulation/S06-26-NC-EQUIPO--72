package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramListResponseDTO;

public interface SocialProgramService {
    SocialProgramListResponseDTO listarProgramas(String tipo, String municipio, String cluster, Boolean activo);
}
