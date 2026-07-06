package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MensajeResponseDTO;
import com.example.appbitb2g.service.BrechasService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/brechas")
@Tag(name = "Brechas", description = "Consulta analítica de brechas territoriales por servicio y municipio")
public class BrechaController {

	private final BrechasService brechasService;

	public BrechaController(BrechasService brechasService) {
		this.brechasService = brechasService;
	}

	/**
	 * GET /brechas?servicio=FORMACION
	 * Retorna el análisis de brechas para el servicio solicitado.
	 */
	@Operation(
			summary = "Analizar brechas territoriales",
			description = "Devuelve brechas estimadas para un servicio dado y, opcionalmente, filtra por municipio y período."
	)
	@ApiResponses({
			@ApiResponse(
					responseCode = "200",
					description = "Brechas calculadas correctamente",
					content = @Content(schema = @Schema(implementation = GapsResponseDTO.class))
			),
			@ApiResponse(
					responseCode = "400",
					description = "Parámetro inválido o faltante",
					content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
			),
			@ApiResponse(
					responseCode = "500",
					description = "Error inesperado al calcular las brechas",
					content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
			)
	})
	@GetMapping
	public ResponseEntity<?> getBrechas(
			@Parameter(description = "Servicio a analizar", example = "FORMACION", required = true)
			@RequestParam(name = "servicio") String servicio,
			@Parameter(description = "Municipio para el filtro opcional", example = "São José")
			@RequestParam(name = "municipio", required = false) String municipio,
			@Parameter(description = "Período horario opcional", example = "TARDE")
			@RequestParam(name = "periodo", required = false) String periodo,
			@Parameter(description = "Clúster de ingresos reservado para compatibilidad del contrato", example = "A")
			@RequestParam(name = "income_cluster", required = false) String incomeCluster) {
		GapsResponseDTO response = brechasService.analizarBrechas(servicio, municipio, periodo, incomeCluster);
		return ResponseEntity.ok(response);
	}
}
