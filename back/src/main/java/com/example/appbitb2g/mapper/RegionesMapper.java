package com.example.appbitb2g.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.model.Antenna;

@Mapper(componentModel = "spring")
public interface RegionesMapper {
    
    List<RegionResponseDTO.RegionRecord> toRegionRecordList(List<Antenna> antennas);
    
    @Mapping(source = "lat", target = "latCentroide")
    @Mapping(source = "lon", target = "lonCentroide")
    @Mapping(target = "nAntenas", ignore = true) 
    RegionResponseDTO.RegionRecord toRegionDetailDto(Antenna antenna);
}
