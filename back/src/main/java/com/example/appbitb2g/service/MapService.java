package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;

public interface MapService {
    MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio);

}
