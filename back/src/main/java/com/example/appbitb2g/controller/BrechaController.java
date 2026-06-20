package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MensajeResponseDTO;
import com.example.appbitb2g.service.BrechasService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;


@RestController
@RequestMapping("/brechas")
public class BrechaController {

    private final BrechasService brechasService;

    public BrechaController(BrechasService brechasService) {
        this.brechasService = brechasService;
    }

    /**
     * GET /brechas?servicio=FORMACION
     * Retorna el análisis de brechas para el servicio solicitado.
     */

    @GetMapping
    public ResponseEntity<?> getBrechas(
        @RequestParam(name = "servicio") String servicio,
        @RequestParam(name = "municipio", required = false) String municipio,
        @RequestParam(name = "periodo", required = false) String periodo,
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
