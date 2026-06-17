package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MensajeResponseDTO;
import com.example.appbitb2g.service.MapService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;

@RestController
@RequestMapping("/mapa")
public class MapController{
    private final MapService mapService;

    public MapController(MapService mapService) {
        this.mapService = mapService;
    }

    // GET /mapa/indicadores?categoria=EDUCACION
    @GetMapping("/indicadores")
    public ResponseEntity<?> getIndicadoresMap(
            @RequestParam(name = "categoria") String categoria,
            @RequestParam(name = "indicador", required = false) String indicador,
            @RequestParam(name = "municipio", required = false) String municipio
    ){
        // 1. Validación de seguridad contra el contrato
        if(!Arrays.asList("SALUD_MENTAL", "EMPLEO","EDUCACION").contains(categoria.toUpperCase())){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                    new MensajeResponseDTO(
                            "FILTRO_INVALIDO",
                            "El valor de ´Categoria´ debe ser SALUD_MENTAL / EMPLEO / EDUCACION"
                    )
            );

        }

        // 2. Llamada al servicio que cruza Antenas + Concentracion + TerritorialIndicators
              MapIndicadoresResponseDTO response = mapService.obtenerMapaIndicadores(categoria, indicador,municipio);
            if(response.regiones().isEmpty()){
                return  ResponseEntity.status(HttpStatus.NOT_FOUND).body(
                        new MensajeResponseDTO(
                                "SIN_RESULTADOS",
                                "No se encontraron datos para los filtros apluicados."

                        )
                );
            }

        // 3. Devolvemos el JSON estructurado/DTO al Frontend
      return ResponseEntity.ok(response);

    }
}

