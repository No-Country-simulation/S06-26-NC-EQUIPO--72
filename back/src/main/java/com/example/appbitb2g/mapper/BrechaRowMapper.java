package com.example.appbitb2g.mapper;

import com.example.appbitb2g.dto.responseDTO.socialProgram.GapsResponseDTO;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;

public class BrechaRowMapper implements RowMapper<GapsResponseDTO.BrechaDetalleRecord> {
	@Override
	public GapsResponseDTO.BrechaDetalleRecord mapRow(ResultSet rs, int rowNum) throws SQLException {
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
	}
}
