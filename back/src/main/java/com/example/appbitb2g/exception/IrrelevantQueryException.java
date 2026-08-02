package com.example.appbitb2g.exception;

public class IrrelevantQueryException extends RuntimeException {
    private final String errorCode;

    public IrrelevantQueryException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public String getErrorCode() {
        return errorCode;
    }
}
