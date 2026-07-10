package com.example.appbitb2g.service.impl;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramFilterDTO;
import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.exception.NotFoundException;
import com.example.appbitb2g.mapper.SocialProgramMapper;
import com.example.appbitb2g.model.SocialProgram;
import com.example.appbitb2g.repository.SocialProgramRepository;
import com.example.appbitb2g.service.SocialProgramService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

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
	public List<SocialProgramResponseDTO.ProgramDetail> programs(SocialProgramFilterDTO filtro) {

		SocialProgramFilterDTO f = (filtro != null) ? filtro
				: new SocialProgramFilterDTO(null, null, null, true);

		List<SocialProgram> socialProgramDetailPag = socialProgramRepository.findWithDynamicFilters(
				f.tipo(),
				f.municipio(),
				f.cluster(),
				f.activo());

		List<Object[]> rawTotals = socialProgramRepository.countSocialProgramRaw();

		Map<String, Long> clusterTotalsMap = rawTotals.stream()
				.collect(Collectors.toMap(
						fila -> (String) fila[0],
						fila -> (Long) fila[1]));

		return socialProgramDetailPag.stream().map(sp -> {
			Long totalParaEsteCluster = clusterTotalsMap.getOrDefault(sp.getCluster(), 0L);
			double promedioReplicable = (sp.getReplicable() != null) ? sp.getReplicable() * 4.0 : 0.0;
			double bonusPorVolumen = totalParaEsteCluster * 0.1;
			double efectividadCalculada = Math.round((promedioReplicable + bonusPorVolumen) * 10.0) / 10.0;


			efectividadCalculada = Math.min(5.0, efectividadCalculada);

			return this.socialProgramMapper.toProgramDetailDto(sp, totalParaEsteCluster,
					efectividadCalculada);
		}).collect(Collectors.toList());
	}

	public SocialProgramResponseDTO deleteProgram(Integer id) {

		SocialProgram program = socialProgramRepository.findById(id).orElseThrow(
				() -> new NotFoundException(
						"PROGRAMA_NO_ENCONTRADO",
						"No existe un programa con el id indicado."));

		socialProgramRepository.deleteById(program.getId());

		return SocialProgramResponseDTO.builder()
				.id(id)
				.mensaje("Programa desactivado correctamente.")
				.build();
	}

	public SocialProgramResponseDTO updateProgram(Integer id, SocialProgramRequestDTO requestDto) {

		SocialProgram program = socialProgramRepository.findById(id).orElseThrow(
				() -> new NotFoundException(
						"PROGRAMA_NO_ENCONTRADO",
						"No existe un programa con el id indicado."));

		socialProgramMapper.updateEntityFromDto(requestDto, program);

		SocialProgram updatedProgram = socialProgramRepository.save(program);

		return SocialProgramResponseDTO.builder()
				.id(updatedProgram.getId())
				.mensaje("Programa actualizado correctamente.")
				.build();
	}
}
