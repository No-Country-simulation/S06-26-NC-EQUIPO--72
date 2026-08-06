
package com.example.appbitb2g.dto.requestDTO.queryrRequestDto;

import io.swagger.v3.oas.annotations.media.Schema;

//  Recibe la respuesta del gestor desde el front para reanudar una consulta
@Schema(description = "Solicitud para reanudar una consulta pausada con la respuesta del gestor")
public record ResumeRequestDTO(
    @Schema(description = "ID de sesión devuelto por POST /api/datos cuando requiere_clarificacion era true", example = "a1b2c3d4")
    String sessionId,
    @Schema(description = "Respuesta del gestor a la pregunta de clarificación", example = "mentoría")
    String respuestaGestor
) {}
