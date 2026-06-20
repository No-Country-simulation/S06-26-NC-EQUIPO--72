package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;
import com.example.appbitb2g.service.BrechasService;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Service
public class BrechaServiceImpl implements BrechasService {
    private final TerritorialIndicatorsRepository territorialIndicatorsRepository;

    public BrechaServiceImpl(TerritorialIndicatorsRepository territorialIndicatorsRepository) {
        this.territorialIndicatorsRepository = territorialIndicatorsRepository;
    }

    @Override
    public GapsResponseDTO analizarBrechas(String servicio, String municipio) {
        List<GapsResponseDTO.BrechaDetalleRecord> brechasMock = new ArrayList<>();

        // Normalizamos el parámetro del servicio recibido para evitar problemas de mayúsculas/minúsculas
        String servicioFiltro = (servicio != null) ? servicio.toUpperCase() : "SALUD_MENTAL";

        if ("SALUD_MENTAL".equals(servicioFiltro)) {

            // --- BRECHA 1: BIGUACU_BR101_NORTE (Dato exacto de tu contrato) ---
            GapsResponseDTO.IndicadorSocialRecord socialBiguacu = new GapsResponseDTO.IndicadorSocialRecord(
                    "SALUD_MENTAL",
                    "taxa_internacao_psiquiatrica",
                    new BigDecimal("17.4"),
                    "porcentaje"
            );

            brechasMock.add(new GapsResponseDTO.BrechaDetalleRecord(
                    "BIGUACU_BR101_NORTE",
                    "Biguaçu",
                    9800,                    // n_usuarios
                    0.81,                    // congestionamento_medio (81% - Alerta Crítica)
                    "WCDMA",                 // rat_type_predominante
                    socialBiguacu,
                    0,                       // programas_activos (Brecha ALTA porque no hay programas de contención)
                    "ALTA"                   // severidad_brecha
            ));

            // --- BRECHA 2: FLORIANOPOLIS_CENTRO (Dato adicional de Salud Mental) ---
            GapsResponseDTO.IndicadorSocialRecord socialCentro = new GapsResponseDTO.IndicadorSocialRecord(
                    "SALUD_MENTAL",
                    "taxa_internacao_psiquiatrica",
                    new BigDecimal("11.2"),
                    "porcentaje"
            );

            brechasMock.add(new GapsResponseDTO.BrechaDetalleRecord(
                    "FLORIANOPOLIS_CENTRO",
                    "Florianópolis",
                    14500,
                    0.42,                    // Congestión moderada (42%)
                    "NR",                    // 5G
                    socialCentro,
                    2,                       // Tiene 2 programas activos, por lo que la brecha baja
                    "BAJA"
            ));

        } else if ("FORMACION".equals(servicioFiltro)) {

            // --- BRECHA 3: SAO_JOSE_KOBRASOL (Brecha de Educación) ---
            GapsResponseDTO.IndicadorSocialRecord socialKobrasol = new GapsResponseDTO.IndicadorSocialRecord(
                    "EDUCACION",
                    "idhm_2010_educacion",
                    new BigDecimal("0.847"),
                    "índice"
            );

            brechasMock.add(new GapsResponseDTO.BrechaDetalleRecord(
                    "SAO_JOSE_KOBRASOL",
                    "São José",
                    12400,
                    0.72,                    // Congestión Alta (72%)
                    "LTE",                   // 4G
                    socialKobrasol,
                    0,                       // Cero programas formativos
                    "ALTA"
            ));

        } else {
            // --- BRECHA 4: FALLBACK GENERAL / EMPLEO ---
            GapsResponseDTO.IndicadorSocialRecord socialBarreiros = new GapsResponseDTO.IndicadorSocialRecord(
                    "EMPLEO",
                    "taxa_desemprego_municipal",
                    new BigDecimal("8.3"),
                    "porcentaje"
            );

            brechasMock.add(new GapsResponseDTO.BrechaDetalleRecord(
                    "SAO_JOSE_BARREIROS",
                    "São José",
                    9400,
                    0.31,
                    "LTE",
                    socialBarreiros,
                    1,
                    "MEDIA"
            ));
        }

        // Filtramos por municipio de manera dinámica si el usuario lo manda en la URL de Postman
        if (municipio != null && !municipio.isBlank()) {
            brechasMock = brechasMock.stream()
                    .filter(b -> b.municipio().equalsIgnoreCase(municipio))
                    .toList();
        }

        // Estructuramos el criterio técnico de corte exigido en el contrato JSON
        GapsResponseDTO.CriterioRecord criterio = new GapsResponseDTO.CriterioRecord(
                servicioFiltro,
                "congestionamento_medio > 0.6 AND programas_activos = 0",
                0.6
        );

        // Retornamos el DTO consolidado con nuestra simulación inteligente
        return new GapsResponseDTO(brechasMock, criterio);
    }
}

