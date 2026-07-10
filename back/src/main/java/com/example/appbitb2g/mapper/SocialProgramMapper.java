package com.example.appbitb2g.mapper;

import org.mapstruct.BeanMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.model.SocialProgram;

@Mapper(componentModel = "spring")
public interface SocialProgramMapper {
    @Mapping(target = "id", ignore = true)
    SocialProgram toEntity(SocialProgramRequestDTO dto);

@Mapping(source = "totalRepo", target = "total")
SocialProgramResponseDTO.ProgramDetail toProgramDetailDto(SocialProgram socialProgram, Long totalRepo , Double efectividad);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    @Mapping(target = "id", ignore = true)
    void updateEntityFromDto(SocialProgramRequestDTO dto, @MappingTarget SocialProgram entity);
}
