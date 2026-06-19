package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;

public interface MapService {
    MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio);
    MapResponseDTO obtenerMapa(String periodo, String municipio, String fecha);
}
