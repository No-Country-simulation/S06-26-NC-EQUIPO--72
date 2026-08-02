package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.territorialIndicator.IndicadorEvolucionResponseDTO;
import com.example.appbitb2g.service.MapService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/indicadores")
@Tag(name = "Indicadores", description = "Endpoints para la evolución temporal de indicadores territoriales")
public class IndicadorEvolucionController {

	private final MapService mapService;

	public IndicadorEvolucionController(MapService mapService) {
		this.mapService = mapService;
	}

	// GET /indicadores/evolucion?categoria=EMPLEO&indicador=taxa_emprego_formal&municipio=São José
	@Operation(
			summary = "Obtener evolución de un indicador",
			description = "Devuelve la evolución temporal de un indicador territorial."
	)
	@GetMapping("/evolucion")
	public ResponseEntity<?> getIndicadoresEvolucion(
			@Parameter(description = "Categoría de indicadores a consultar", example = "EMPLEO", required = true)
			@RequestParam(name = "categoria") String categoria,
			@Parameter(description = "Indicador específico opcional", example = "taxa_emprego_formal")
			@RequestParam(name = "indicador", required = false) String indicador,
			@Parameter(description = "Municipio a filtrar", example = "São José")
			@RequestParam(name = "municipio", required = false) String municipio
	) {
		IndicadorEvolucionResponseDTO response = mapService.obtenerEvolucionIndicador(categoria, indicador, municipio);
		return ResponseEntity.ok(response);
	}
}
