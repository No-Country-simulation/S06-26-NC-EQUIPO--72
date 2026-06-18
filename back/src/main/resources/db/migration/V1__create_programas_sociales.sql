CREATE TABLE IF NOT EXISTS programas_sociales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150),
    tipo VARCHAR(30),
    descripcion TEXT,
    municipio VARCHAR(60),
    cluster VARCHAR(40),
    organizacion VARCHAR(150),
    lider_referente VARCHAR(150) NULL,
    replicable SMALLINT NULL,
    impacto_estimado VARCHAR(10) NULL,
    url_referencia VARCHAR(255) NULL,
    fecha_inicio DATE,
    fecha_fin DATE NULL,
    activo SMALLINT
);
