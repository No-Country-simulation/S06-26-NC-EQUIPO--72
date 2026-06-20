package com.example.appbitb2g.dto.responseDTO.socialProgram;
/**
 * Record compartido para devolver mensajes estructurados al Frontend.
 * Sirve tanto para notificar éxitos como para detallar errores del sistema (e.g., FILTRO_INVALIDO).
 * No requiere Lombok ni anotaciones adicionales.
 */
public record MensajeResponseDTO(
        String error,
        String mensaje
) {
}
