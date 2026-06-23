package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.service.RegionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/regiones")
@Tag(name = "Regiones", description = "Listado de regiones y clústeres disponibles para el mapa")
public class RegionController {

    private final RegionService regionService;

    public RegionController(RegionService regionService) {
        this.regionService = regionService;
    }

    @Operation(
            summary = "Obtener regiones",
            description = "Devuelve el catálogo de regiones con sus centroides y cantidad de antenas."
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Regiones recuperadas correctamente",
                    content = @Content(schema = @Schema(implementation = RegionResponseDTO.class))
            )
    })
    @GetMapping
    public ResponseEntity<RegionResponseDTO> obtenerRegiones() {
        RegionResponseDTO response = regionService.obtenerRegiones();
        return ResponseEntity.ok(response);
    }
}
