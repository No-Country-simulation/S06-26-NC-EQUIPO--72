package com.example.appbitb2g.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.appbitb2g.model.TerritorialIndicators;

import java.util.List;

public interface TerritorialIndicatorsRepository extends JpaRepository<TerritorialIndicators,Integer> {
    List<TerritorialIndicators> findAll();
    
}
