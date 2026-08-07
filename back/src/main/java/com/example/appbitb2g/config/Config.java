package com.example.appbitb2g.config;

import java.time.Duration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.netty.http.client.HttpClient;

@Configuration
public class Config {
    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    @Value("${ai.service.api-token:}")
    private String aiServiceApiToken;

    @Bean
    public WebClient aiServiceWebClient() {
        WebClient.Builder builder = WebClient.builder()
                .baseUrl(aiServiceUrl)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                // Timeout generoso: las consultas compuestas del AI Service
                // tienen p95 ~15s, así que 60s cubre el peor caso sin cortar.
                .clientConnector(new ReactorClientHttpConnector(
                        HttpClient.create().responseTimeout(Duration.ofSeconds(60))
                ));
        // API key compartida con el AI Service (si está configurada).
        // Solo se envía el header cuando hay token, para no romper el dev
        // local donde el AI Service corre sin auth.
        if (aiServiceApiToken != null && !aiServiceApiToken.isBlank()) {
            builder.defaultHeader("X-API-Key", aiServiceApiToken);
        }
        return builder.build();
    }

    public String getAiServiceUrl() {
        return aiServiceUrl;
    }
}
