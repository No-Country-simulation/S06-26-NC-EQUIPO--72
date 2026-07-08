package com.example.appbitb2g.service;

import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramFilterDTO;
import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramListResponseDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;

public interface SocialProgramService {
    
    SocialProgramResponseDTO createProgram(SocialProgramRequestDTO socialProgramRequestDTO);
    List<SocialProgramResponseDTO.ProgramDetail> programs( SocialProgramFilterDTO filtro);
    SocialProgramResponseDTO deleteProgram(Integer id);
    SocialProgramResponseDTO updateProgram(Integer id, SocialProgramRequestDTO requestDto);
}
