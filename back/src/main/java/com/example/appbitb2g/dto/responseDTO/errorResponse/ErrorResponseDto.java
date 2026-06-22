package com.example.appbitb2g.dto.responseDTO.errorResponse;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Respuesta estándar de error de la API")
public record ErrorResponseDto(
        @Schema(description = "Código o clave de error", example = "FILTRO_INVALIDO")
        String error,
        @Schema(description = "Mensaje legible para el cliente", example = "El parámetro 'servicio' es obligatorio.")
        String mensaje) {
}
