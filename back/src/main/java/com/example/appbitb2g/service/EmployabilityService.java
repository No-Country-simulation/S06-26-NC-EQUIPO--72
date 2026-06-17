package com.example.appbitb2g.service;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;

import org.springframework.stereotype.Service;

import com.example.appbitb2g.dto.requestDTO.employability.AiQueryRequestDTO;
import com.example.appbitb2g.dto.requestDTO.employability.GapFilterDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.FountainDTO;
import com.example.appbitb2g.dto.responseDTO.employability.GapResponseContainerDTO;
import com.example.appbitb2g.exception.IrrelevantQueryException;

@Service
public class EmployabilityService {

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

  public GapResponseContainerDTO GetemploymentGaps(GapFilterDTO filtros) {
        
    
      String servicioActivo = (filtros.getServicio() != null) ? filtros.getServicio().toUpperCase() : "EMPLEO";

    GapResponseContainerDTO.IndicadorSocialDTO indicadorMock = GapResponseContainerDTO.IndicadorSocialDTO.builder()
            .categoria(servicioActivo) 
            .indicador("postulantes_sin_empleo")
            .valor(1450.0)
            .unidad("personas")
            .build();


    String clusterDestino = (filtros.getCluster()!= null && !filtros.getCluster().isBlank()) 
            ? filtros.getCluster() 
            : "FLORIPA_ALTO_CHOPIN";

    String municipioDestino = (filtros.getMunicipio() != null && !filtros.getMunicipio().isBlank()) 
            ? filtros.getMunicipio() 
            : "Florianópolis"; 

    GapResponseContainerDTO.BrechaDetailDTO brechaMock = GapResponseContainerDTO.BrechaDetailDTO.builder()
            .cluster(clusterDestino)     
            .municipio(municipioDestino) 
            .nUsuarios(12400)
            .congestionamentoMedio(0.74)
            .ratTypePredominante("LTE")
            .indicadorSocial(indicadorMock)
            .programasActivos(0)
            .severidadBrecha("ALTA")
            .build();

   
    GapResponseContainerDTO.CriterioDTO criterioMock = GapResponseContainerDTO.CriterioDTO.builder()
            .servicio(servicioActivo) 
            .logica("congestionamento_medio > 0.6 AND programas_activos = 0")
            .umbralCongestionamento(0.6)
            .build();

    return GapResponseContainerDTO.builder()
            .brechas(List.of(brechaMock))
            .criterio(criterioMock)
            .build();

}
}
