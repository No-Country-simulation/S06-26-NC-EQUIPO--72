package com.example.appbitb2g.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.appbitb2g.dto.requestDTO.employability.AiQueryRequestDTO;
import com.example.appbitb2g.dto.requestDTO.employability.GapFilterDTO;
import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;
import com.example.appbitb2g.dto.responseDTO.employability.GapResponseContainerDTO;
import com.example.appbitb2g.service.EmployabilityService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/employability")
@AllArgsConstructor
public class EmployabilityController {

    private final EmployabilityService employabilityService;

    @PostMapping("/query")
    public ResponseEntity<AiQueryResponseDTO> employabilityQuery(@RequestBody AiQueryRequestDTO requestDto) {

        var response = employabilityService.aiQueryAgent(requestDto);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/gaps")

    public ResponseEntity<GapResponseContainerDTO> getGaps(GapFilterDTO filtros) {

        GapResponseContainerDTO respuesta = employabilityService.GetemploymentGaps(filtros);
        return ResponseEntity.ok(respuesta);
    }

}
