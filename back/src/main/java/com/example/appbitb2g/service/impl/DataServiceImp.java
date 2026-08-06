package com.example.appbitb2g.service.impl;

import java.time.Duration;

import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiResumeRequestDTO;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiServiceRequestDTO;
import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.ResumeRequestDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiServiceResponseDTO;
import com.example.appbitb2g.exception.IrrelevantQueryException;
import com.example.appbitb2g.exception.NotFoundException;
import com.example.appbitb2g.service.DataService;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class DataServiceImp implements DataService {
	private final WebClient aiServiceWebClient;

	public DataServiceImp(WebClient aiServiceWebClient) {
		this.aiServiceWebClient = aiServiceWebClient;
	}

	@Override
	public AiQueryResponseDTO aiQueryAgent(AiQueryRequestDTO requestDto) {
		if (requestDto.consulta() == null || requestDto.consulta().isBlank()) {
			throw new IrrelevantQueryException(
					"CONSULTA_VACIA",
					"El campo 'consulta' es obligatorio."
			);
		}

		AiServiceRequestDTO aiRequest = new AiServiceRequestDTO(
				requestDto.consulta(),
				requestDto.idioma() != null ? requestDto.idioma() : "es"
		);

		// Llamar al servicio de IA. El endpoint del backend es síncrono,
		// por eso se usa .block().
		AiServiceResponseDTO aiResponse = aiServiceWebClient
				.post()
				.uri("/consulta")
				.bodyValue(aiRequest)
				.retrieve()
				// Preservar el mapeo de 422 -> CONSULTA_IRRELEVANTE que antes
				// hacía GlobalExceptionHandler con RestTemplate.
				.onStatus(
						status -> status.value() == 422,
						response -> response.bodyToMono(String.class)
								.map(body -> new IrrelevantQueryException(
										"CONSULTA_IRRELEVANTE",
										"La consulta no puede resolverse con los datos disponibles."
								))
				)
				.bodyToMono(AiServiceResponseDTO.class)
				.timeout(Duration.ofSeconds(60))
				.block();

		return toFrontendResponse(aiResponse);
	}

	@Override
	public AiQueryResponseDTO resumirConsulta(ResumeRequestDTO requestDto) {
		if (requestDto.sessionId() == null || requestDto.sessionId().isBlank()) {
			throw new NotFoundException(
					"SESION_NO_ENCONTRADA",
					"El campo 'sessionId' es obligatorio."
			);
		}

		AiResumeRequestDTO aiResumeRequest = new AiResumeRequestDTO(
				requestDto.sessionId(),
				requestDto.respuestaGestor() != null ? requestDto.respuestaGestor() : ""
		);

		AiServiceResponseDTO aiResponse = aiServiceWebClient
				.post()
				.uri("/consulta/respuesta")
				.bodyValue(aiResumeRequest)
				.retrieve()
				// Sesión expirada / inexistente -> 404
				.onStatus(
						status -> status.value() == 404,
						response -> response.bodyToMono(String.class)
								.map(body -> new NotFoundException(
										"SESION_EXPIRADA",
										"La sesión expiró o no existe. Enviá la consulta de nuevo."
								))
				)
				.onStatus(
						status -> status.value() == 422,
						response -> response.bodyToMono(String.class)
								.map(body -> new IrrelevantQueryException(
										"CONSULTA_IRRELEVANTE",
										"La consulta no puede resolverse con los datos disponibles."
								))
				)
				.bodyToMono(AiServiceResponseDTO.class)
				.timeout(Duration.ofSeconds(60))
				.block();

		return toFrontendResponse(aiResponse);
	}

	private AiQueryResponseDTO toFrontendResponse(AiServiceResponseDTO aiResponse) {
		return new AiQueryResponseDTO(
				aiResponse.respuesta_ia(),
				aiResponse.visualizacion_sugerida(),
				aiResponse.datos(),
				aiResponse.fuentes(),
				aiResponse.datos() != null ? aiResponse.datos().size() : 0,
				aiResponse.idioma(),
				aiResponse.session_id(),
				aiResponse.requiere_clarificacion(),
				aiResponse.pregunta_clarificacion(),
				aiResponse.opciones_clarificacion()
		);
	}
}
