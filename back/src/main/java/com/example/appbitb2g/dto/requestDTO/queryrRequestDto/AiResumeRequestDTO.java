
package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

//  Envia la reanudación al servicio de IA
@Schema(description = "Solicitud interna que se envía al servicio de IA para reanudar")
public record AiResumeRequestDTO(
    @Schema(description = "ID de sesión de la consulta pausada", example = "a1b2c3d4")
    @JsonProperty("session_id") String sessionId,
    @Schema(description = "Respuesta del gestor a la pregunta de clarificación", example = "mentoría")
    @JsonProperty("respuesta_gestor") String respuestaGestor
) {}
