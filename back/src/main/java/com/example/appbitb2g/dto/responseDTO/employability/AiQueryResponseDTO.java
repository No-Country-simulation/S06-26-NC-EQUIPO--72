
package com.example.appbitb2g.dto.responseDTO.employability;

import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;

//  Envía la respuesta final al frontend
@Schema(description = "Respuesta estructurada que devuelve el servicio de IA al frontend")
public record AiQueryResponseDTO(
    @Schema(description = "Respuesta textual generada por IA", example = "La brecha principal está en formación.")
    @JsonProperty("respuesta_ia") String respuestaIa,
    @Schema(description = "Visualización sugerida para presentar los datos", example = "bar")
    @JsonProperty("visualizacion_sugerida") String visualizacionSugerida,
    @Schema(description = "Datos tabulares asociados a la respuesta")
    @JsonProperty("datos") List<Map<String, Object>> datos,
    @Schema(description = "Fuentes utilizadas por la IA")
    @JsonProperty("fuentes") List<FountainDTO> fuentes,
    @Schema(description = "Cantidad total de registros devueltos", example = "12")
    @JsonProperty("total_registros") Integer totalRegistros,
    @Schema(description = "Idioma de la respuesta", example = "es")
    @JsonProperty("idioma") String idioma,
    @Schema(description = "ID de sesión HITL para reanudar la consulta pausada", example = "a1b2c3d4")
    @JsonProperty("session_id") String sessionId,
    @Schema(description = "True si el agente pausó y necesita clarificación del gestor", example = "false")
    @JsonProperty("requiere_clarificacion") Boolean requiereClarificacion,
    @Schema(description = "Pregunta de clarificación al gestor")
    @JsonProperty("pregunta_clarificacion") String preguntaClarificacion,
    @Schema(description = "Opciones de respuesta para la clarificación")
    @JsonProperty("opciones_clarificacion") List<String> opcionesClarificacion
) {}
