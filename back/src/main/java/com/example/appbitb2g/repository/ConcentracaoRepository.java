package com.example.appbitb2g.repository;

import java.time.LocalDate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.example.appbitb2g.model.Concentracao;

public interface ConcentracaoRepository extends JpaRepository<Concentracao,Integer> {
    @Query("SELECT MAX(c.dayDate) FROM concentracao c")
    LocalDate findMaxDayDate();
}
