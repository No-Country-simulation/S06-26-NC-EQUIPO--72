package com.example.appbitb2g.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.example.appbitb2g.model.SocialProgram;

public interface SocialProgramRepository extends JpaRepository<SocialProgram,Integer> {

  @Query("""
         SELECT p
         FROM SocialProgram p
         WHERE
         (:tipo IS NULL OR UPPER(p.tipo) = UPPER(:tipo))
         AND (:municipio IS NULL OR UPPER(p.municipio) = UPPER(:municipio))
         AND (:cluster IS NULL OR UPPER(p.cluster) = UPPER(:cluster))
         AND (:activo IS NULL OR p.activo = :activo)
        """)
        Page<SocialProgram> findWithDynamicFilters(
                @Param("tipo") String tipo,
                @Param("municipio") String municipio,
                @Param("cluster") String cluster,
                @Param("activo") Boolean activo,
                Pageable pageable
        );
    
}
