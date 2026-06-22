package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.Antenna;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


public interface AntenaRepository extends JpaRepository<Antenna, String> {
}
