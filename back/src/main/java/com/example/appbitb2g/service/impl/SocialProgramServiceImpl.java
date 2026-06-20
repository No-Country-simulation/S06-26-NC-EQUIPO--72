package com.example.appbitb2g.service.impl;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramListResponseDTO;
import com.example.appbitb2g.service.SocialProgramService;
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
public class SocialProgramServiceImpl implements SocialProgramService {

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

    /*
    *
    * SERVICIOS DE FORMACIONES
    * *
    * */
    @Override
    public SocialProgramListResponseDTO listarProgramas(String tipo, String municipio, String cluster, Boolean activo) {
        List<SocialProgramListResponseDTO.ProgramDetailRecord> programasMock = new ArrayList<>();

        // --- REGISTRO MOCK 1: FORMACIÓN (Florianópolis) ---
        programasMock.add(new SocialProgramListResponseDTO.ProgramDetailRecord(
                1,
                "Alfabetización Digital para Adultos Mayores",
                "FORMACION",
                "Clases presenciales de uso de smartphones y banca móvil en centros comunitarios.",
                "Florianópolis",
                "FLORIANOPOLIS_CENTRO",
                "Municipalidad de Florianópolis",
                "Isabela Martins",
                1,
                "ALTO",
                "https://florianopolis.sc.gov.br/alfabetizacion",
                LocalDate.of(2025, 2, 1),
                LocalDate.of(2025, 12, 31),
                true
        ));

        // --- REGISTRO MOCK 2: FORMACIÓN (São José) ---
        programasMock.add(new SocialProgramListResponseDTO.ProgramDetailRecord(
                2,
                "Iniciación a la Programación Web",
                "FORMACION",
                "Curso intensivo online de desarrollo frontend (HTML, CSS y JavaScript) para jóvenes.",
                "São José",
                "SAO_JOSE_KOBRASOL",
                "ONG Conectar",
                "Carlos Souza",
                1,
                "MEDIO",
                "https://conectar.org/web-basic",
                LocalDate.of(2025, 4, 15),
                LocalDate.of(2025, 7, 15),
                true
        ));

        // --- REGISTRO MOCK 3: MENTORÍA (São José) ---
        programasMock.add(new SocialProgramListResponseDTO.ProgramDetailRecord(
                3,
                "Mentores para el Futuro Tecnológico",
                "MENTORIA",
                "Acompañamiento personalizado y guía de carrera de programadores senior a estudiantes de secundaria.",
                "São José",
                "SAO_JOSE_KOBRASOL",
                "ONG Conectar",
                "Mateo Santos",
                0,
                "ALTO",
                "https://conectar.org/mentores",
                LocalDate.of(2025, 3, 10),
                null,
                true
        ));

        // --- PROCESAMIENTO DINÁMICO DE FILTROS EN MEMORIA ---
        List<SocialProgramListResponseDTO.ProgramDetailRecord> resultadosFiltrados = new ArrayList<>(programasMock);

        // 1. Filtrado por tipo (ej: FORMACION o MENTORIA)
        if (tipo != null && !tipo.isBlank()) {
            resultadosFiltrados = resultadosFiltrados.stream()
                    .filter(p -> p.tipo().equalsIgnoreCase(tipo))
                    .toList();
        }

        // 2. Filtrado opcional por municipio
        if (municipio != null && !municipio.isBlank()) {
            resultadosFiltrados = resultadosFiltrados.stream()
                    .filter(p -> p.municipio().equalsIgnoreCase(municipio))
                    .toList();
        }

        // 3. Filtrado opcional por clúster
        if (cluster != null && !cluster.isBlank()) {
            resultadosFiltrados = resultadosFiltrados.stream()
                    .filter(p -> p.cluster().equalsIgnoreCase(cluster))
                    .toList();
        }

        // 4. Filtrado opcional por estado activo
        if (activo != null) {
            resultadosFiltrados = resultadosFiltrados.stream()
                    .filter(p -> p.activo().equals(activo))
                    .toList();
        }

        // Devolvemos el DTO consolidado con la lista filtrada y el total de elementos
        return new SocialProgramListResponseDTO(resultadosFiltrados, resultadosFiltrados.size());
    }
}

