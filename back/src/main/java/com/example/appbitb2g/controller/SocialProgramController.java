package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramListResponseDTO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramFilterDTO;
import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.service.impl.SocialProgramServiceImpl;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/programas")
@AllArgsConstructor
public class SocialProgramController {

    private final SocialProgramServiceImpl programService;

    @PostMapping
    public ResponseEntity<SocialProgramResponseDTO> createProgram(
            @RequestBody SocialProgramRequestDTO socialProgramRequestDTO) {

        var response = programService.createProgram(socialProgramRequestDTO);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<Page<SocialProgramResponseDTO.ProgramDetail>> program(
            @PageableDefault(page = 0, size = 5) Pageable pageable,
            @ModelAttribute SocialProgramFilterDTO filtro) {

        Page<SocialProgramResponseDTO.ProgramDetail> programPage = programService.programs(pageable, filtro);
        return ResponseEntity.ok(programPage);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<SocialProgramResponseDTO> delete(@PathVariable Integer id) {
        SocialProgramResponseDTO response = programService.deleteProgram(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<SocialProgramResponseDTO> updateProgram(
            @PathVariable Integer id,
            @RequestBody SocialProgramRequestDTO requestDto) {

        var response = programService.updateProgram(id, requestDto);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /programas?tipo=FORMACION
     * Retorna la lista de programas sociales activos o filtrados por tipo, municipio o clúster.
     */
    @GetMapping("/list")
    public ResponseEntity<SocialProgramListResponseDTO> obtenerProgramas(
            @RequestParam(name = "tipo", required = false) String tipo,
            @RequestParam(name = "municipio", required = false) String municipio,
            @RequestParam(name = "cluster", required = false) String cluster,
            @RequestParam(name = "activo", required = false, defaultValue = "true") Boolean activo
    ) {
        SocialProgramListResponseDTO response = programService.listarProgramas(tipo, municipio, cluster, activo);
        return ResponseEntity.ok(response);
    }


}
