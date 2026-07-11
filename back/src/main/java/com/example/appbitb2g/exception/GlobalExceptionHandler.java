package com.example.appbitb2g.exception;


import com.example.appbitb2g.dto.responseDTO.errorResponse.ErrorResponseDto;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.RestClientResponseException;

@RestControllerAdvice
public class GlobalExceptionHandler {

	@ExceptionHandler(NotFoundException.class)
	public ResponseEntity<ErrorResponseDto> handleNotFound(NotFoundException ex) {
		ErrorResponseDto errorDTO = new ErrorResponseDto(
				ex.getErrorCode(),
				ex.getMessage());
		return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorDTO);
	}

	@ExceptionHandler(IrrelevantQueryException.class)
	public ResponseEntity<ErrorResponseDto> handleIrrelevantQuery(IrrelevantQueryException ex) {
		ErrorResponseDto errorDTO = new ErrorResponseDto(
				ex.getErrorCode(),
				ex.getMessage());
		return ResponseEntity.status(HttpStatus.UNPROCESSABLE_CONTENT).body(errorDTO);
	}

	@ExceptionHandler(BadRequestException.class)
	public ResponseEntity<ErrorResponseDto> handleBadRequest(BadRequestException ex) {
		ErrorResponseDto errorDTO = new ErrorResponseDto(
				ex.getErrorCode(),
				ex.getMessage());
		return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorDTO);
	}

	@ExceptionHandler(Exception.class)
	public ResponseEntity<ErrorResponseDto> handleGeneralException(Exception ex) {
		ErrorResponseDto errorDTO = new ErrorResponseDto(
				"ERROR_INTERNO",
				"Ocurrió un error inesperado al calcular las brechas del territorio"
		);
		return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorDTO);
	}

	@ExceptionHandler({HttpClientErrorException.class, HttpServerErrorException.class})
	public ResponseEntity<ErrorResponseDto> handleRestClientException(RestClientResponseException ex) {
		if (ex.getStatusCode().value() == 422) {
			return ResponseEntity.status(HttpStatus.UNPROCESSABLE_CONTENT).body(new ErrorResponseDto(
					"CONSULTA_IRRELEVANTE",
					"La consulta no puede resolverse con los datos disponibles."
			));
		}

		return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ErrorResponseDto(
				"ERROR_INTERNO",
				"Ocurrió un error procesando la consulta."
		));
	}
}
