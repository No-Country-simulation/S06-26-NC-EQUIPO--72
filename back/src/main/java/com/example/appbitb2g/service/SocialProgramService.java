package com.example.appbitb2g.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramFilterDTO;
import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.mapper.SocialProgramMapper;
import com.example.appbitb2g.model.SocialProgram;
import com.example.appbitb2g.repository.SocialProgramRepository;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class SocialProgramService {

    private final SocialProgramRepository socialProgramRepository;
    private final SocialProgramMapper socialProgramMapper;

    @Transactional
    public SocialProgramResponseDTO createProgram(SocialProgramRequestDTO socialProgramRequestDTO) {
        if (socialProgramRequestDTO.getFechaInicio() == null) {
            socialProgramRequestDTO.setFechaInicio(LocalDate.now());
        }

        socialProgramRequestDTO.setActivo(true);

        SocialProgram socialProgram = socialProgramMapper.toEntity(socialProgramRequestDTO);

        var socialProgramdb = socialProgramRepository.save(socialProgram);

        var socialDto = SocialProgramResponseDTO.builder()
                .id(socialProgramdb.getId())
                .mensaje("Programa registrado correctamente.")
                .build();

        return socialDto;
    }

    @Transactional(readOnly = true)
    public Page<SocialProgramResponseDTO.ProgramDetail> programs(Pageable pageable, SocialProgramFilterDTO filtro) {

        SocialProgramFilterDTO f = (filtro != null) ? filtro : new SocialProgramFilterDTO(null, null, null, true);

        Page<SocialProgram> socialProgramDetailPag = socialProgramRepository.findWithDynamicFilters(
                f.tipo(),
                f.municipio(),
                f.cluster(),
                f.activo(),
                pageable);

        return socialProgramDetailPag.map(socialProgramMapper::toProgramDetailDto);
    }

    public SocialProgramResponseDTO deleteProgram(Integer id) {

     SocialProgram program = socialProgramRepository.findById(id).orElseThrow(
                () -> new com.example.appbitb2g.exception.NotFoundException("No existe un programa con el id indicado."));

        socialProgramRepository.deleteById(program.getId());

        return SocialProgramResponseDTO.builder()
                .id(id)
                .mensaje("Programa desactivado correctamente.")
                .build();
    }

    public SocialProgramResponseDTO updateProgram(Integer id, SocialProgramRequestDTO requestDto) {

        SocialProgram program = socialProgramRepository.findById(id).orElseThrow(
                () -> new com.example.appbitb2g.exception.NotFoundException("No existe un programa con el id indicado."));

        socialProgramMapper.updateEntityFromDto(requestDto, program);

        SocialProgram updatedProgram = socialProgramRepository.save(program);

        return SocialProgramResponseDTO.builder()
                .id(updatedProgram.getId())
                .mensaje("Programa actualizado correctamente.")
                .build();
    }

}
