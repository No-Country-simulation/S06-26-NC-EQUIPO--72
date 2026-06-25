package com.example.appbitb2g.repository;

import com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO.RegionRecord;
import com.example.appbitb2g.model.Antenna;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.jpa.repository.JpaRepository;


public interface AntenaRepository extends JpaRepository<Antenna, String> {

   @Query("""
    select new com.example.appbitb2g.dto.responseDTO.socialProgram.RegionResponseDTO$RegionRecord(
         a.cluster, 
         max(a.municipio), 
         cast(avg(a.lat) as big_decimal), 
         cast(avg(a.lon) as big_decimal), 
         cast(count(a) as integer)
    )
    from antenas a
    group by a.cluster
""")
   List<RegionRecord> obtenerDetallePorMunicipio();
}
