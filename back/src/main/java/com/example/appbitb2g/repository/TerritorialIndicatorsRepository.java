package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.TerritorialIndicators;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
 
public interface TerritorialIndicatorsRepository extends JpaRepository<TerritorialIndicators, Integer> {
 
    @Query(value = """
        SELECT JSON_OBJECT(
            'regiones', IFNULL(
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'cluster', geo.cluster,
                        'municipio', geo.municipio,
                        'lat', geo.lat,
                        'lon', geo.lon,
                        'n_usuarios', geo.n_usuarios,
                        'congestionamento_medio', geo.congestionamento_medio,
                        'indicadores', IFNULL(
                            (
                                SELECT JSON_ARRAYAGG(
                                    JSON_OBJECT(
                                        'categoria', ind.categoria,
                                        'indicador', ind.indicador,
                                        'valor', ind.valor,
                                        'unidad', ind.unidad,
                                        'fonte', ind.fonte,
                                        'fecha_referencia', ind.fecha_referencia
                                    )
                                )
                                FROM indicadores_territoriales ind
                                WHERE ind.cluster = geo.cluster
                                  AND ind.categoria = UPPER(:categoria)
                                  
                                  AND (:indicador IS NULL OR ind.indicador = :indicador)
                            ), JSON_ARRAY()
                        )
                    )
                ), JSON_ARRAY()
            )
        )
        FROM (
            SELECT 
                i.cluster,
                i.municipio,
                COALESCE(AVG(c_ant.lat), AVG(a_direct.lat)) as lat,               
                COALESCE(AVG(c_ant.lon), AVG(a_direct.lon)) as lon,               
                ROUND(
                    COALESCE(
                        LN(NULLIF(AVG(c.congestionamento_medio), 0)) / 26.0,
                        0
                    ),
                    4
                ) as congestionamento_medio,
                SUM(c.n_usuarios) as n_usuarios  
            FROM indicadores_territoriales i 
            LEFT JOIN concentracao c ON c.cluster = i.cluster
            LEFT JOIN antenas c_ant ON c_ant.ecgi = c.ecgi
            LEFT JOIN antenas a_direct ON a_direct.cluster = i.cluster
           
            WHERE (:municipio IS NULL OR i.municipio = :municipio)
            GROUP BY i.cluster, i.municipio
        ) geo
        """, nativeQuery = true)
    String getIndicatorsRawJson(
        @Param("categoria") String categoria,
        @Param("indicador") String indicador,
        @Param("municipio") String municipio
    );



}