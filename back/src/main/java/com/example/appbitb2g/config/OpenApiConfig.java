package com.example.appbitb2g.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.info.License;
import io.swagger.v3.oas.annotations.servers.Server;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "Appbitb2g API",
                version = "1.0.0",
                description = "Documentación OpenAPI de los endpoints de brechas, mapas, regiones, programas sociales y consultas de IA.",
                contact = @Contact(
                        name = "Equipo Appbitb2g"
                ),
                license = @License(
                        name = "Apache 2.0"
                )
        ),
        servers = {
                @Server(url = "/api", description = "Servidor local de la aplicación")
        }
)
public class OpenApiConfig {
}