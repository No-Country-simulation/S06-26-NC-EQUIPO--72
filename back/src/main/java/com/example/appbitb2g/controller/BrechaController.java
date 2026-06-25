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
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;


@RestController
@RequestMapping("/brechas")
@CrossOrigin(origins = "*")
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
    @Parameter(description = "Clúster de ingresos reservado para compatibilidad del contrato", example = "SAO_JOSE_KOBRASOL")
    @RequestParam(name = "income_cluster", required = false) String incomeCluster)
    {
    // 1. Validación de parámetro obligatorio 'servicio' según el contrato
    if (servicio == null || servicio.isBlank()) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
            new MensajeResponseDTO(
                "DATO_REQUERIDO",
                "El parámetro 'servicio' es obligatorio en la consulta."
            )
        );
    }

    // 2. Validación de tipos de servicio admitidos en el MVP
    if (!Arrays.asList("MENTORIA", "FORMACION", "EXPERIENCIA", "SALUD_MENTAL", "EMPLEO").contains(servicio.toUpperCase())) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
            new MensajeResponseDTO(
                "FILTRO_INVALIDO",
                "El valor de 'servicio' debe ser MENTORIA / FORMACION / EXPERIENCIA / SALUD_MENTAL / EMPLEO"
            )

        );
    }

    // 3. Validación opcional de período si viene en la query
    if (periodo != null && !Arrays.asList("MADRUGADA", "MANHA", "TARDE", "NOITE").contains(periodo.toUpperCase())) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(
            new MensajeResponseDTO(
                "FILTRO_INVALIDO",
                "El valor de 'periodo' debe ser MADRUGADA / MANHA / TARDE / NOITE."
            )
        );

    }

    try {
        // 4. Delegamos el cálculo analítico al servicio especializado
        GapsResponseDTO response = brechasService.analizarBrechas(servicio.toUpperCase(), municipio);
        return ResponseEntity.ok(response);

    } catch (Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(
            new MensajeResponseDTO(
                "ERROR_INTERNO",
                "Ocurrió un error inesperado al calcular las brechas del territorio"
            )
        );
    }
    }
}
