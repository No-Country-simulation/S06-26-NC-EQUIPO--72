package com.example.appbitb2g.repository;

import com.example.appbitb2g.model.Concentracao;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;

public interface ConcentracaoRepository extends JpaRepository<Concentracao, Integer> {
	@Query("SELECT MAX(c.dayDate) FROM concentracao c")
	LocalDate findMaxDayDate();

	@Query(value = """
			SELECT JSON_ARRAYAGG(
			    JSON_OBJECT(
			        'cluster', datos.cluster,
			        'connectivityPercentage', datos.conectividad_pct,
			        'healthValue', datos.valor_salud_mental
			    )
			) AS json_resultado
			FROM (
			    -- Tu consulta original intacta actuando como subconsulta
			    SELECT\s
			        tech.cluster,
			
			        -- EJE X: Porcentaje de Conectividad real
			        ROUND((1 - tech.congestionamento_avg) * 100, 2) AS conectividad_pct,
			
			        -- EJE Y: Valor de salud mental directo
			        ind.valor_salud_mental
			
			    FROM (
			        SELECT\s
			            cluster,
			            AVG(congestionamento_medio) AS congestionamento_avg
			        FROM concentracao
			        GROUP BY cluster
			    ) tech
			
			    INNER JOIN (
			        SELECT cluster, valor AS valor_salud_mental
			        FROM (
			            SELECT cluster, valor,
			                   ROW_NUMBER() OVER (PARTITION BY cluster ORDER BY fecha_referencia DESC, id DESC) AS rn
			            FROM indicadores_territoriales
			            WHERE categoria = 'SALUD_MENTAL'
			              AND indicador = 'taxa_internacao_psiquiatrica'
			        ) it_ranked
			        WHERE rn = 1
			    ) ind ON tech.cluster = ind.cluster
			
			    ORDER BY conectividad_pct
			) AS datos;
			""", nativeQuery = true)
	String getConnectivityHealthCorrelation();
}
