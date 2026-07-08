package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.TerritorialIndicators;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface TerritorialIndicatorsRepository extends JpaRepository<TerritorialIndicators, Integer> {

    @Query(value = """
        -- Resuelve el día más reciente una sola vez
        WITH ultimo_dia AS (
            SELECT MAX(day_date) AS day_date FROM concentracao
        ),
        -- Universo base de clusters: todo cluster que tenga al menos un indicador territorial cargado
        clusters_filtrados AS (
            SELECT DISTINCT cluster, municipio
            FROM indicadores_territoriales
            WHERE (:municipio IS NULL OR municipio = :municipio)
        ),
        -- Centroide aproximado de cada cluster, promediando las antenas que lo componen
        coordenadas AS (
            SELECT cluster, AVG(lat) AS lat, AVG(lon) AS lon
            FROM antenas
            GROUP BY cluster
        ),
        -- Concentración de usuarios y congestión del cluster en el último día disponible
        concentracion_actual AS (
            SELECT c.cluster,
                TRUNCATE(AVG(c.congestionamento_medio), 2) AS congestionamento_medio,
                SUM(c.n_usuarios) AS n_usuarios
            FROM concentracao c
            JOIN ultimo_dia u ON c.day_date = u.day_date
            GROUP BY c.cluster
        ),
        -- Indicadores territoriales agregados a un solo array JSON por cluster (evita subquery repetida por fila)
        indicadores_agg AS (
            SELECT ind.cluster,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'categoria', ind.categoria,
                        'indicador', ind.indicador,
                        'valor', ind.valor,
                        'unidad', ind.unidad,
                        'fonte', ind.fonte,
                        'fecha_referencia', ind.fecha_referencia
                    )
                ) AS indicadores
            FROM indicadores_territoriales ind
            -- UPPER en ambos lados por las dudas de que la data no esté normalizada en mayúsculas
            WHERE UPPER(ind.categoria) = UPPER(:categoria)
            AND (:indicador IS NULL OR ind.indicador = :indicador)
            GROUP BY ind.cluster
        )
        SELECT JSON_OBJECT(
            'regiones', IFNULL(
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'cluster', i.cluster,
                        'municipio', i.municipio,
                        'lat', coord.lat,
                        'lon', coord.lon,
                        'n_usuarios', conc.n_usuarios,
                        'congestionamento_medio', conc.congestionamento_medio,
                        -- si el cluster no tiene indicadores que matcheen el filtro, devuelve array vacío en vez de null
                        'indicadores', IFNULL(ia.indicadores, JSON_ARRAY())
                    )
                ), JSON_ARRAY()
            )
        )
        FROM clusters_filtrados i
        LEFT JOIN coordenadas coord ON coord.cluster = i.cluster
        LEFT JOIN concentracion_actual conc ON conc.cluster = i.cluster
        LEFT JOIN indicadores_agg ia ON ia.cluster = i.cluster
        """, nativeQuery = true)
    String getIndicatorsRawJson(
        @Param("categoria") String categoria,
        @Param("indicador") String indicador,
        @Param("municipio") String municipio
    );

    @Query(value = """
        SELECT JSON_OBJECT(
            'indicador', :indicador,
            'categoria', :categoria,

            -- Evolución nacional: promedio mensual de los últimos 12 meses
            'evolucion', COALESCE(
                (SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'fecha_referencia', sub.fecha_referencia,
                        'valor_promedio', sub.valor_promedio
                    )
                )
                FROM (
                    SELECT fecha_referencia, ROUND(AVG(valor), 4) AS valor_promedio
                    FROM indicadores_territoriales
                    WHERE UPPER(categoria) = UPPER(:categoria)
                    AND indicador = :indicador
                    AND (:municipio IS NULL OR municipio = :municipio)
                    AND fecha_referencia >= DATE_SUB(
                        (SELECT MAX(fecha_referencia) FROM indicadores_territoriales
                        WHERE UPPER(categoria) = UPPER(:categoria) AND indicador = :indicador),
                        INTERVAL 11 MONTH
                    )
                    GROUP BY fecha_referencia
                    ORDER BY fecha_referencia ASC
                ) sub),
                JSON_ARRAY()
            ),

            -- Último valor por cluster (snapshot más reciente) + n_usuarios de concentracao
            'por_cluster', COALESCE(
                (SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'cluster', ranked.cluster,
                        'municipio', ranked.municipio,
                        'valor', ranked.valor,
                        'fecha_referencia', ranked.fecha_referencia,
                        'n_usuarios', COALESCE(conc.n_usuarios, 0)
                    )
                )
                FROM (
                    SELECT cluster, municipio, valor, fecha_referencia,
                        ROW_NUMBER() OVER (PARTITION BY cluster, municipio
                                        ORDER BY fecha_referencia DESC) AS rn
                    FROM indicadores_territoriales
                    WHERE UPPER(categoria) = UPPER(:categoria)
                    AND indicador = :indicador
                    AND (:municipio IS NULL OR municipio = :municipio)
                ) ranked
                LEFT JOIN (
                    SELECT cluster, municipio, SUM(n_usuarios) AS n_usuarios
                    FROM concentracao
                    WHERE day_date = (SELECT MAX(day_date) FROM concentracao)
                    GROUP BY cluster, municipio
                ) conc ON conc.cluster = ranked.cluster AND conc.municipio = ranked.municipio
                WHERE ranked.rn = 1),
                JSON_ARRAY()
            )
        )
        """, nativeQuery = true)
    String getIndicatorEvolutionRawJson(
        @Param("categoria") String categoria,
        @Param("indicador") String indicador,
        @Param("municipio") String municipio
    );
}