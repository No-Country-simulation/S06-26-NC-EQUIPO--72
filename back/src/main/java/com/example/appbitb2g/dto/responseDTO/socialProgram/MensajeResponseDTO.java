package com.example.appbitb2g.dto.responseDTO.socialProgram;

import io.swagger.v3.oas.annotations.media.Schema;
/**
 * Record compartido para devolver mensajes estructurados al Frontend.
 * Sirve tanto para notificar éxitos como para detallar errores del sistema (e.g., FILTRO_INVALIDO).
 * No requiere Lombok ni anotaciones adicionales.
 */
@Schema(description = "Mensaje estructurado para respuestas funcionales o de error")
public record MensajeResponseDTO(
        @Schema(description = "Código o clave del mensaje", example = "FILTRO_INVALIDO")
        String error,
        @Schema(description = "Detalle legible para el cliente", example = "El valor de 'servicio' debe ser FORMACION / MENTORIA / EXPERIENCIA / SALUD_MENTAL / EMPLEO")
        String mensaje
) {
}
