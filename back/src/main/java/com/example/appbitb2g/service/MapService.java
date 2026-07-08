package com.example.appbitb2g.service;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
import com.example.appbitb2g.dto.responseDTO.territorialIndicator.IndicadorEvolucionResponseDTO;

public interface MapService {
    MapIndicadoresResponseDTO obtenerMapaIndicadores(String categoria, String indicador, String municipio);
    MapResponseDTO obtenerMapa(String periodo, String municipio, String fecha);
    IndicadorEvolucionResponseDTO obtenerEvolucionIndicador(String categoria, String indicador, String municipio);
}
