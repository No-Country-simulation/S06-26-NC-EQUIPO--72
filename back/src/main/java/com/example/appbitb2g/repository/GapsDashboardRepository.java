package com.example.appbitb2g.repository;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio de solo lectura (Read Model) orientado a la extracción analítica y cálculo de brechas territoriales.
 * <p>
 * Este componente prescinde del motor ORM (JPA/Hibernate)
 * y utiliza {@link org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate}
 * para ejecutar consultas SQL nativas altamente optimizadas. Su responsabilidad exclusiva es cruzar
 * y consolidar de forma eficiente grandes volúmenes de datos provenientes de métricas de red,
 * indicadores socioeconómicos y programas sociales activos.
 * </p>
 * <p>
 * Los resultados obtenidos de la base de datos se proyectan y mapean directamente en
 * Data Transfer Objects (DTOs) inmutables, garantizando una transferencia de datos segura,
 * de bajo consumo de memoria y lista para su serialización estructural en la capa de presentación.
 * </p>
 */
@Repository
public class GapsDashboardRepository {

	private final NamedParameterJdbcTemplate jdbcTemplate;

	public GapsDashboardRepository(NamedParameterJdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	public List<GapsResponseDTO.BrechaDetalleRecord> getGapsByCriteria(String servicio,
	                                                                   String municipio,
	                                                                   String periodo,
	                                                                   String incomeCluster) {

		final String QUERY = """
					SELECT
					    tech.cluster,
					    tech.municipio,
					    tech.n_usuarios,
					    ROUND(tech.congestionamento_medio, 2) AS congestionamento_medio,
					    tech.rat_type_predominante,
				
					    -- Sub-objeto indicador_social
					    ind.categoria AS ind_categoria,
					    ind.indicador AS ind_indicador,
					    ind.valor AS ind_valor,
					    ind.unidad AS ind_unidad,
				
					    COALESCE(prog.programas_activos, 0) AS programas_activos,
				
					    -- severidad_brecha: Concentración de personas + calidad de red + ausencia de programas
					    CASE
					        WHEN tech.congestionamento_medio > @umbral_congestionamento
					             AND tech.n_usuarios > @umbral_usuarios
					             AND COALESCE(prog.programas_activos, 0) = 0
					        THEN 'ALTA'
					        WHEN tech.congestionamento_medio > (@umbral_congestionamento - 0.2)
					        THEN 'MEDIA'
					        ELSE 'BAJA'
					    END AS severidad_brecha
				
					FROM (
					    -- Eje Técnico (Calidad de red y concentración de personas)
					    SELECT
					        cluster,
					        municipio,
					        ROUND(AVG(n_usuarios)) AS n_usuarios,
					        AVG(congestionamento_medio) AS congestionamento_medio,
					        MAX(rat_type_predominante) AS rat_type_predominante
					    FROM concentracao
					    WHERE periodo = COALESCE(@periodo, 'TARDE')
					      AND (@municipio IS NULL OR municipio = @municipio)
					      AND (@income_cluster IS NULL OR EXISTS (
					          SELECT 1
					          FROM mobilidade_agregada ma
					          WHERE ma.cluster = concentracao.cluster
					            AND ma.municipio = concentracao.municipio
					            AND ma.periodo = concentracao.periodo
					            AND ma.income_cluster = @income_cluster
					      ))
					    GROUP BY cluster, municipio
					) tech
				
					LEFT JOIN (
					    -- Eje Social (Indicador más reciente)
					    SELECT cluster, municipio, categoria, indicador, valor, unidad
					    FROM (
					        SELECT cluster, municipio, categoria, indicador, valor, unidad,
					               ROW_NUMBER() OVER (PARTITION BY cluster, municipio ORDER BY fecha_referencia DESC, id DESC) AS rn
					        FROM indicadores_territoriales
					        WHERE categoria = @servicio
					          AND (@municipio IS NULL OR municipio = @municipio)
					    ) it_ranked
					    WHERE rn = 1
					) ind ON tech.cluster = ind.cluster AND tech.municipio = ind.municipio
				
					LEFT JOIN (
					    -- Eje Programas (Conteo de cobertura)
					    SELECT
					        cluster,
					        municipio,
					        COUNT(*) AS programas_activos
					    FROM programas_sociales
					    WHERE activo = 1
					      AND (tipo = @servicio OR @servicio NOT IN ('FORMACION', 'MENTORIA', 'EXPERIENCIA'))
					      AND (@municipio IS NULL OR municipio = @municipio)
					    GROUP BY cluster, municipio
					) prog ON tech.cluster = prog.cluster AND tech.municipio = prog.municipio
				
					ORDER BY
					    CASE severidad_brecha
					        WHEN 'ALTA' THEN 1
					        WHEN 'MEDIA' THEN 2
					        ELSE 3
					    END ASC,
					    tech.n_usuarios DESC,
					    tech.congestionamento_medio DESC;
				""";

		// params assignation
		MapSqlParameterSource params = new MapSqlParameterSource()
				.addValue("servicio", servicio)
				.addValue("municipio", municipio)
				.addValue("periodo", periodo)
				.addValue("incomeCluster", incomeCluster);

		// mapping
		return jdbcTemplate.query(QUERY, params, (rs, rowNum) -> {
			GapsResponseDTO.IndicadorSocialRecord socialIndicator = null;
			if (rs.getString("ind_categoria") != null) {
				socialIndicator = new GapsResponseDTO.IndicadorSocialRecord(
						rs.getString("ind_categoria"),
						rs.getString("ind_indicador"),
						rs.getDouble("ind_valor"),
						rs.getString("ind_unidad")
				);
			}

			// main object
			return new GapsResponseDTO.BrechaDetalleRecord(
					rs.getString("cluster"),
					rs.getString("municipio"),
					rs.getInt("n_usuarios"),
					rs.getDouble("congestionamento_medio"),
					rs.getString("rat_type_predominante"),
					socialIndicator,
					rs.getInt("programas_activos"),
					rs.getString("severidad_brecha")
			);
		});
	}
}
