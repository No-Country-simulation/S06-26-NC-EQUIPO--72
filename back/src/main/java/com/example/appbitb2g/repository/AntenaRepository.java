package com.example.appbitb2g.repository;
import java.time.LocalDate;
import com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO;
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

  @Query("""
      select new com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO$MapRegionDTO(
          a.cluster,
          max(a.municipio),
          avg(a.lat),
          avg(a.lon),
          cast(coalesce(sum(c.nUsuarios), 0) as integer),
          coalesce(avg(c.congestionamentoMedio), 0.0),
          'LTE',
          coalesce(avg(c.downloadGb), 0.0),
          :periodo,
          cast(:fecha as string)
      )
      from antenas a
      left join concentracao c on c.ecgi = a.ecgi
          and (:periodo is null or upper(c.periodo) = upper(:periodo))
          and (:fecha is null or c.dayDate = :fecha)
      where (:municipio is null or upper(a.municipio) = upper(:municipio))
      group by a.cluster
  """)
  List<MapResponseDTO.MapRegionDTO> obtenerDatosMapaPrincipal(
          @Param("periodo") String periodo,
          @Param("municipio") String municipio,
          @Param("fecha") LocalDate fecha
  );

}
 