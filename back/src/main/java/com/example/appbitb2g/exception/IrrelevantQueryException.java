package com.example.appbitb2g.exception;

public class IrrelevantQueryException extends RuntimeException {
    private String errorCode;

    public IrrelevantQueryException(String errorCode, String message) {
        this.errorCode = errorCode;
        super(message);
    }

    public String getErrorCode() {
        return errorCode;
    }
}
