package com.example.appbitb2g.service.impl;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.FountainDTO;
import com.example.appbitb2g.exception.IrrelevantQueryException;
import com.example.appbitb2g.service.DataService;
@Service
public class DataServiceImp implements DataService {

    @Override
    public AiQueryResponseDTO aiQueryAgent(AiQueryRequestDTO requestDto) {
         String consultaLower = requestDto.getConsulta().toLowerCase();
                // TODO tnemos que ver que datos son irrelevantes o capz no lo estoy entendiendo
                if (consultaLower.contains("boca") || consultaLower.contains("clima")
                                || consultaLower.contains("comida")) {
                        throw new IrrelevantQueryException(
                                        "La consulta no puede resolverse con los datos disponibles.");
                }
                Map<String, Object> datoMock = Map.of(
                                "cluster", "SAO_JOSE_KOBRASOL",
                                "periodo", "MANHA",
                                "n_usuarios", 8200,
                                "congestionamento_medio", 0.68,
                                "taxa_internacao_psiquiatrica", 14.2);

                FountainDTO fuente1 = new FountainDTO(
                                "Vísent CDRView v2", "tensor_concentracao", "2026-03-10");
                FountainDTO fuente2 = new FountainDTO(
                                "DATASUS", "SIH-SUS", "2025-12-01");

                return new AiQueryResponseDTO(
                                "En SAO_JOSE_KOBRASOL hay 8.200 personas con cobertura WCDMA precaria y ningún programa activo.",
                                "mapa_brechas",
                                List.of(datoMock),
                                List.of(fuente1, fuente2),
                                1,
                                requestDto.getIdioma());
    }
    
}
