package com.example.appbitb2g.dto.requestDTO.socialProgram;

public record SocialProgramFilterDTO(
        String tipo,
        String municipio,
        String cluster,
        Boolean activo) {

    public SocialProgramFilterDTO {
        if (activo == null) {
            activo = true;
        }
    }
}
