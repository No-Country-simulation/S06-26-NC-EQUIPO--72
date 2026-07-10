package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.MapIndicadoresResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MensajeResponseDTO;
import com.example.appbitb2g.dto.responseDTO.territorialIndicator.IndicadorEvolucionResponseDTO;
import com.example.appbitb2g.service.MapService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;

import org.apache.coyote.BadRequestException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;

@RestController
@RequestMapping("/mapa")
@Tag(name = "Mapa", description = "Endpoints para visualizar regiones y sus indicadores territoriales")
public class MapController{
    private final MapService mapService;
    

    public MapController(MapService mapService) {
        this.mapService = mapService;
    }

    // GET /mapa?periodo=TARDE
    @Operation(
            summary = "Obtener mapa territorial",
            description = "Devuelve regiones con métricas de congestión, usuarios y fecha para el mapa principal."
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Mapa calculado correctamente",
                    content = @Content(schema = @Schema(implementation = MapResponseDTO.class))
            ),
            @ApiResponse(
                    responseCode = "400",
                    description = "Filtro inválido",
                    content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
            )
    })
    @GetMapping
    public ResponseEntity<?> getMapa(
            @Parameter(description = "Período horario para la vista del mapa", example = "TARDE")
            @RequestParam(name = "periodo", required = false, defaultValue = "TARDE") String periodo,
            @Parameter(description = "Municipio a filtrar", example = "todos")
            @RequestParam(name = "municipio", required = false, defaultValue = "todos") String municipio,
            @Parameter(description = "Fecha de referencia del mapa", example = "2025-12-01")
            @RequestParam(name = "fecha", required = false) String fecha
    ) {
        // Validar periodo
        if (!Arrays.asList("MADRUGADA", "MANHA", "TARDE", "NOITE").contains(periodo.toUpperCase())) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
                    new MensajeResponseDTO(
                            "FILTRO_INVALIDO",
                            "El valor de ´periodo´ debe ser MADRUGADA / MANHA / TARDE / NOITE"
                    )
            );
        }

        MapResponseDTO response = mapService.obtenerMapa(periodo, municipio, fecha);
        return ResponseEntity.ok(response);
    }

    // GET /mapa/indicadores?categoria=EDUCACION
    @Operation(
            summary = "Obtener indicadores por región",
            description = "Devuelve el detalle de indicadores territoriales agrupados por región y categoría."
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Indicadores calculados correctamente",
                    content = @Content(schema = @Schema(implementation = MapIndicadoresResponseDTO.class))
            ),
            @ApiResponse(
                    responseCode = "400",
                    description = "Categoría inválida",
                    content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
            ),
            @ApiResponse(
                    responseCode = "404",
                    description = "No hay resultados para los filtros",
                    content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
            )
    })
    @GetMapping("/indicadores")
    public ResponseEntity<?> getIndicadoresMap(
            @Parameter(description = "Categoría de indicadores a consultar", example = "EDUCACION", required = true)
            @RequestParam(name = "categoria" ,required = false) String categoria,
            @Parameter(description = "Indicador específico opcional", example = "idhm_2010_educacion")
            @RequestParam(name = "indicador", required = false) String indicador,
            @Parameter(description = "Municipio a filtrar", example = "São José")
            @RequestParam(name = "municipio", required = false) String municipio
    ){
          
          
       

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

    // GET /mapa/indicadores/evolucion?categoria=EMPLEO
    @Operation(
            summary = "Obtener evolución de un indicador",
            description = "Devuelve la evolución temporal de un indicador territorial."
    )
    @ApiResponses({
            @ApiResponse(
                    responseCode = "200",
                    description = "Evolución calculada correctamente",
                    content = @Content(schema = @Schema(implementation = IndicadorEvolucionResponseDTO.class))
            ),
            @ApiResponse(
                    responseCode = "400",
                    description = "Categoría inválida",
                    content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
            ),
            @ApiResponse(
                    responseCode = "404",
                    description = "No hay resultados para los filtros",
                    content = @Content(schema = @Schema(implementation = MensajeResponseDTO.class))
            )
    })
    @GetMapping("/indicadores/evolucion")
    public ResponseEntity<?> getIndicadoresEvolucionMap(
            @Parameter(description = "Categoría de indicadores a consultar", example = "EMPLEO", required = true)
            @RequestParam(name = "categoria") String categoria,
            @Parameter(description = "Indicador específico opcional", example = "taxa_emprego_formal")
            @RequestParam(name = "indicador", required = false) String indicador,
            @Parameter(description = "Municipio a filtrar", example = "São José")
            @RequestParam(name = "municipio", required = false) String municipio
    ){
        // Llamada al servicio que obtiene la evolución del indicador
        IndicadorEvolucionResponseDTO response = mapService.obtenerEvolucionIndicador(categoria, indicador, municipio);
        
        if(response.evolucion().isEmpty()){
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(
                    new MensajeResponseDTO(
                            "SIN_RESULTADOS",
                            "No se encontraron datos para los filtros aplicados."
                    )
            );
        }

        // Devolvemos el JSON estructurado/DTO al Frontend
        return ResponseEntity.ok(response);
    }
}

