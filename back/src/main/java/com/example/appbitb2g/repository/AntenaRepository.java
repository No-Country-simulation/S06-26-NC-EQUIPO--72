package com.example.appbitb2g.repository;

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
         select  new com.example.appbitb2g.dto.responseDTO.socialProgram.MapResponseDTO$MapRegionDTO(
           a.cluster,
             max(a.municipio),
              cast(avg(a.lat) as big_decimal),
                cast(avg(a.lon) as big_decimal),
                  cast(coalesce(sum(c.n_usuarios), 0) as integer),
                    cast(coalesce(avg(c.congestionamiento_medio),0.0) as double),
                      'LTE',
                        0.0,
                          :periodo,
                            :fecha
                        )
                          from Antenna a
                            left join Concentracao c on c.ecgi = a.ecgi
                              where(:municipio is null or upper(a.municipio) = upper(:municipio))
                                and(:periodo is null or upper(c.periodo) = upper(:periodo))
                                  and(:fecha is null or c.day_date= :fecha)
                                    group by a.cluster
  """)
   List<MapResponseDTO.MapRegionDTO> obtenerDatosMapaPrincipal(
          @Param("periodo")String periodo,
          @Param("municipio")String municipio,
          @Param("fecha")String fecha
   );

}
