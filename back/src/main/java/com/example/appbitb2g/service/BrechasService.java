package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;

public interface BrechasService {
    GapsResponseDTO analizarBrechas(String servicio, String municipio);
}
