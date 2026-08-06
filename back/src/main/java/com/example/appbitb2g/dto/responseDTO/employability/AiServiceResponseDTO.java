
package com.example.appbitb2g.dto.responseDTO.employability;

import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

//  Recibe la respuesta desde el servicio de IA
@Schema(description = "Respuesta devuelta por el servicio de IA externo")
public record AiServiceResponseDTO(
    @Schema(description = "Respuesta textual generada por IA", example = "La brecha principal está en formación.")
    @JsonProperty("respuesta_ia") String respuesta_ia,
    @Schema(description = "Datos tabulares asociados a la respuesta")
    @JsonProperty("datos") List<Map<String, Object>> datos,
    @Schema(description = "Fuentes utilizadas por la IA")
    @JsonProperty("fuentes") List<FountainDTO> fuentes,
    @Schema(description = "Visualización sugerida para presentar los datos", example = "bar")
    @JsonProperty("visualizacion_sugerida") String visualizacion_sugerida,
    @Schema(description = "Idioma de la respuesta", example = "es")
    @JsonProperty("idioma") String idioma,
    @Schema(description = "ID de sesión HITL para reanudar una consulta pausada", example = "a1b2c3d4")
    @JsonProperty("session_id") String session_id,
    @Schema(description = "True si el agente pausó y necesita clarificación del gestor", example = "false")
    @JsonProperty("requiere_clarificacion") Boolean requiere_clarificacion,
    @Schema(description = "Pregunta de clarificación al gestor")
    @JsonProperty("pregunta_clarificacion") String pregunta_clarificacion,
    @Schema(description = "Opciones de respuesta para la clarificación")
    @JsonProperty("opciones_clarificacion") List<String> opciones_clarificacion
) {}
