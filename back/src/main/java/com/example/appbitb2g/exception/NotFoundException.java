package com.example.appbitb2g.exception;

public class NotFoundException extends RuntimeException {
    private String errorCode;

    public NotFoundException(String errorCode, String message) {
        this.errorCode = errorCode;
        super(message);
    }

    public String getErrorCode() {
        return errorCode;
    }
}
