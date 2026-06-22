package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.Antenna;
import com.example.appbitb2g.model.FlujoOd;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TensorOdSeederRepository extends JpaRepository<FlujoOd, String> {
}
