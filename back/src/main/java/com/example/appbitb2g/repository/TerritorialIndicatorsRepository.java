package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.TerritorialIndicators;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TerritorialIndicatorsRepository
        extends JpaRepository<TerritorialIndicators, Integer> {

}