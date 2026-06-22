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

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springdoc.core.annotations.ParameterObject;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/programas")
@AllArgsConstructor
@Tag(name = "Programas sociales", description = "Gestión y consulta de programas sociales de la aplicación")
public class SocialProgramController {

    private final SocialProgramServiceImpl programService;

    @Operation(
        summary = "Crear programa social",
        description = "Registra un nuevo programa social con los datos enviados en el cuerpo de la petición."
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "201",
            description = "Programa creado correctamente",
            content = @Content(schema = @Schema(implementation = SocialProgramResponseDTO.class))
        )
    })
    @io.swagger.v3.oas.annotations.parameters.RequestBody(
        description = "Datos del programa a crear",
        required = true,
        content = @Content(schema = @Schema(implementation = SocialProgramRequestDTO.class))
    )
    @PostMapping
    public ResponseEntity<SocialProgramResponseDTO> createProgram(
            @RequestBody SocialProgramRequestDTO socialProgramRequestDTO) {

        var response = programService.createProgram(socialProgramRequestDTO);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

        @Operation(
            summary = "Listar programas paginados",
            description = "Devuelve una página de programas sociales filtrados por tipo, municipio, clúster o estado activo."
        )
        @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Página de programas recuperada correctamente")
        })
    @GetMapping
    public ResponseEntity<Page<SocialProgramResponseDTO.ProgramDetail>> program(
            @ParameterObject
            @PageableDefault(page = 0, size = 5) Pageable pageable,
            @ParameterObject
            @ModelAttribute SocialProgramFilterDTO filtro) {

        Page<SocialProgramResponseDTO.ProgramDetail> programPage = programService.programs(pageable, filtro);
        return ResponseEntity.ok(programPage);
    }

        @Operation(
            summary = "Eliminar programa",
            description = "Desactiva o elimina lógicamente un programa social por su identificador."
        )
        @ApiResponses({
            @ApiResponse(
                responseCode = "200",
                description = "Programa desactivado correctamente",
                content = @Content(schema = @Schema(implementation = SocialProgramResponseDTO.class))
            ),
            @ApiResponse(responseCode = "404", description = "Programa no encontrado")
        })
    @DeleteMapping("/{id}")
        public ResponseEntity<SocialProgramResponseDTO> delete(
            @Parameter(description = "Identificador del programa", example = "1") @PathVariable Integer id) {
        SocialProgramResponseDTO response = programService.deleteProgram(id);
        return ResponseEntity.ok(response);
    }

        @Operation(
            summary = "Actualizar programa",
            description = "Actualiza los datos principales de un programa social existente."
        )
        @ApiResponses({
            @ApiResponse(
                responseCode = "200",
                description = "Programa actualizado correctamente",
                content = @Content(schema = @Schema(implementation = SocialProgramResponseDTO.class))
            ),
            @ApiResponse(responseCode = "404", description = "Programa no encontrado")
        })
        @io.swagger.v3.oas.annotations.parameters.RequestBody(
            description = "Datos del programa a actualizar",
            required = true,
            content = @Content(schema = @Schema(implementation = SocialProgramRequestDTO.class))
        )
    @PutMapping("/{id}")
    public ResponseEntity<SocialProgramResponseDTO> updateProgram(
            @Parameter(description = "Identificador del programa", example = "1") @PathVariable Integer id,
            @RequestBody SocialProgramRequestDTO requestDto) {

        var response = programService.updateProgram(id, requestDto);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /programas?tipo=FORMACION
     * Retorna la lista de programas sociales activos o filtrados por tipo, municipio o clúster.
     */
        @Operation(
            summary = "Listar programas resumidos",
            description = "Devuelve una lista consolidada de programas sociales para consumo del frontend."
        )
        @ApiResponses({
            @ApiResponse(
                responseCode = "200",
                description = "Listado recuperado correctamente",
                content = @Content(schema = @Schema(implementation = SocialProgramListResponseDTO.class))
            )
        })
    @GetMapping("/list")
    public ResponseEntity<SocialProgramListResponseDTO> obtenerProgramas(
            @Parameter(description = "Tipo de programa", example = "FORMACION")
            @RequestParam(name = "tipo", required = false) String tipo,
            @Parameter(description = "Municipio a filtrar", example = "São José")
            @RequestParam(name = "municipio", required = false) String municipio,
            @Parameter(description = "Clúster a filtrar", example = "SAO_JOSE_KOBRASOL")
            @RequestParam(name = "cluster", required = false) String cluster,
            @Parameter(description = "Filtra por estado activo", example = "true")
            @RequestParam(name = "activo", required = false, defaultValue = "true") Boolean activo
    ) {
        SocialProgramListResponseDTO response = programService.listarProgramas(tipo, municipio, cluster, activo);
        return ResponseEntity.ok(response);
    }


}
