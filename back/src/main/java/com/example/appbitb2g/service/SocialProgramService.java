package com.example.appbitb2g.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.model.SocialProgram;
import com.example.appbitb2g.repository.SocialProgramRepository;

import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class SocialProgramService {

    private final SocialProgramRepository socialProgramRepository;

    @Transactional
    public SocialProgramResponseDTO createProgram(SocialProgramRequestDTO socialProgramRequestDTO) {

        SocialProgram socialProgram = new SocialProgram();
        socialProgram.setNombre(socialProgramRequestDTO.getNombre());
        socialProgram.setTipo(socialProgramRequestDTO.getTipo());
        socialProgram.setDescripcion(socialProgramRequestDTO.getDescripcion());
        socialProgram.setMunicipio(socialProgramRequestDTO.getMunicipio());
        socialProgram.setCluster(socialProgramRequestDTO.getCluster());
        socialProgram.setOrganizacion(socialProgramRequestDTO.getOrganizacion());
        socialProgram.setLiderReferente(socialProgramRequestDTO.getLiderReferente());
        socialProgram.setReplicable(socialProgramRequestDTO.getReplicable());
        socialProgram.setImpactoEstimado(socialProgramRequestDTO.getImpactoEstimado());
        socialProgram.setUrlReferencia(socialProgramRequestDTO.getUrlReferencia());
        socialProgram.setFechaInicio(socialProgramRequestDTO.getFechaInicio());
        socialProgram.setFechaFin(socialProgramRequestDTO.getFechaFin());

        var socialProgramdb = socialProgramRepository.save(socialProgram);

        var socialDto = SocialProgramResponseDTO.builder()
                .id(socialProgramdb.getId())
                .mensaje("Programa registrado correctamente.")
                .build();

        return socialDto;
    }

    public Page<SocialProgramResponseDTO.ProgramDetail> programs(Pageable pageable) {
        Page<SocialProgram> onboardingPage = socialProgramRepository.findAll(pageable);

        return onboardingPage.map(sm -> SocialProgramResponseDTO.ProgramDetail.builder()
            .id(sm.getId())
            .nombre(sm.getNombre())
            .tipo(sm.getTipo())
            .descripcion(sm.getDescripcion())
            .municipio(sm.getMunicipio())
            .cluster(sm.getCluster())
            .organizacion(sm.getOrganizacion())
            .liderReferente(sm.getLiderReferente())
            .replicable(sm.getReplicable())
            .impactoEstimado(sm.getImpactoEstimado())
            .urlReferencia(sm.getUrlReferencia())
            .fechaInicio(sm.getFechaInicio())
            .fechaFin(sm.getFechaFin())
            .build());
    }

}
