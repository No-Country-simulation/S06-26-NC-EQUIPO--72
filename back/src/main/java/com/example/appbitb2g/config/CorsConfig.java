package com.example.appbitb2g.config;


import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig {

	private static final String[] ALLOWED_ORIGINS = {
			"http://localhost:5173",
			"http://localhost:3000",
			"https://appbit-b2b.onrender.com"
	};

	private final String[] ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE", "OPTIONS"};

	@Bean
	public WebMvcConfigurer corsConfigurer() {
		return new WebMvcConfigurer() {
			@Override
			public void addCorsMappings(CorsRegistry registry) {
				//TODO despues solo agregar las rutas publicas
				registry.addMapping("/**")
						.allowedOriginPatterns(ALLOWED_ORIGINS)
						.allowedMethods(ALLOWED_METHODS)
						.allowedHeaders("*")
						.allowCredentials(true);
			}
		};
	}
}

