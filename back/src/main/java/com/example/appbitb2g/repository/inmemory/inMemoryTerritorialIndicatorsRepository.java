package com.example.appbitb2g.repository.inmemory;

import com.example.appbitb2g.model.TerritorialIndicators;
import com.example.appbitb2g.repository.TerritorialIndicatorsRepository;

import java.util.List;

public class inMemoryTerritorialIndicatorsRepository implements TerritorialIndicatorsRepository {
    @Override
    public List<TerritorialIndicators> findAll() {
        return List.of();
    }
}
