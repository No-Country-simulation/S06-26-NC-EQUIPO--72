package com.example.appbitb2g.controller;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO;
import com.example.appbitb2g.service.RegionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/regiones")
public class RegionController {

    private final RegionService regionService;

    public RegionController(RegionService regionService) {
        this.regionService = regionService;
    }

    @GetMapping
    public ResponseEntity<RegionResponseDTO> obtenerRegiones() {
        RegionResponseDTO response = regionService.obtenerRegiones();
        return ResponseEntity.ok(response);
    }
}
