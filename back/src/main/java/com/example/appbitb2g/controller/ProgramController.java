package com.example.appbitb2g.controller;

import org.springframework.data.crossstore.ChangeSetPersister.NotFoundException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.appbitb2g.dto.requestDTO.socialProgram.SocialProgramRequestDTO;
import com.example.appbitb2g.dto.responseDTO.socialProgram.SocialProgramResponseDTO;
import com.example.appbitb2g.service.ProgramService;

import jakarta.websocket.server.PathParam;
import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/api")
@AllArgsConstructor
public class ProgramController {

    private final ProgramService programService;

     @PostMapping("/program")
    public ResponseEntity<SocialProgramResponseDTO> createProgram(
            @RequestBody SocialProgramRequestDTO socialProgramRequestDTO) {

        var response = programService.createProgram(socialProgramRequestDTO);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);

    }

     @GetMapping("/programs")
    public ResponseEntity<Page<SocialProgramResponseDTO.ProgramDetail>> program(
        @PageableDefault(page = 0, size = 5) Pageable pageable)
     {

       Page<SocialProgramResponseDTO.ProgramDetail> programPage = programService.programs(pageable);
       

        return ResponseEntity.ok(programPage);

    }
    
}
