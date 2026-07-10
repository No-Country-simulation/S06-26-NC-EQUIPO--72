package com.example.appbitb2g.exception;

public class BadRequestException extends RuntimeException {
    private String errorCode;

    public BadRequestException(String errorCode, String message) {
        this.errorCode = errorCode;
        super(message);
    }

    public String getErrorCode() {
        return errorCode;
    }
}
