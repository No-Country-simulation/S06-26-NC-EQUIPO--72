package com.example.appbitb2g.controller;



import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;

import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;

import com.example.appbitb2g.service.DataService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping
@AllArgsConstructor
@Tag(name = "Datos de IA", description = "Endpoint que delega consultas al servicio de inteligencia artificial")
public class DataController {

    private final DataService dataService;

    @Operation(
        summary = "Ejecutar consulta de IA",
        description = "Envía una consulta y el idioma al servicio de IA y devuelve la respuesta estructurada para el frontend."
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "Consulta procesada correctamente",
            content = @Content(schema = @Schema(implementation = AiQueryResponseDTO.class))
        ),
        @ApiResponse(responseCode = "422", description = "Consulta irrelevante o no resoluble"),
        @ApiResponse(responseCode = "500", description = "Error interno del servicio")
    })
    @io.swagger.v3.oas.annotations.parameters.RequestBody(
        description = "Consulta a enviar al servicio de IA",
        required = true,
        content = @Content(schema = @Schema(implementation = AiQueryRequestDTO.class))
    )
    @PostMapping("/datos")
    public ResponseEntity<AiQueryResponseDTO> datosQuery(@RequestBody AiQueryRequestDTO requestDto) {
        var response = dataService.aiQueryAgent(requestDto);
        return ResponseEntity.ok(response);
    }

}
