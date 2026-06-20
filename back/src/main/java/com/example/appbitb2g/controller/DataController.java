package com.example.appbitb2g.controller;



import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.appbitb2g.dto.requestDTO.queryrRequestDto.AiQueryRequestDTO;

import com.example.appbitb2g.dto.responseDTO.employability.AiQueryResponseDTO;

import com.example.appbitb2g.service.DataService;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping("/employability")
@AllArgsConstructor
public class DataController {

    private final DataService dataService;

    @PostMapping("/query")
    public ResponseEntity<AiQueryResponseDTO> employabilityQuery(@RequestBody AiQueryRequestDTO requestDto) {

        var response = dataService.aiQueryAgent(requestDto);

        return ResponseEntity.ok(response);
    }

}
