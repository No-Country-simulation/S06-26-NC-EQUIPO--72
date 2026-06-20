package com.example.appbitb2g.exception;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.example.appbitb2g.dto.responseDTO.errorResponse.ErrorResponseDto;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponseDto> handleNotFound(NotFoundException ex) {

        // Creamos el molde usando el Record
        ErrorResponseDto errorDTO = new ErrorResponseDto(
                "PROGRAMA_NO_ENCONTRADO",
                ex.getMessage());

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorDTO);
    }

    @ExceptionHandler(IrrelevantQueryException.class)
    public ResponseEntity<ErrorResponseDto> handleIrrelevantQuery(IrrelevantQueryException ex) {
         ErrorResponseDto errorDTO = new ErrorResponseDto(
                "PROGRAMA_NO_ENCONTRADO",
                ex.getMessage());
                 return ResponseEntity.status(422).body(errorDTO);
    }
      @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<ErrorResponseDto> handleBadRequest(BadRequestException ex) {
        
       
        ErrorResponseDto errorDTO = new ErrorResponseDto(
                "FILTRO_INVALIDO",
                ex.getMessage());

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorDTO);
    }

}
