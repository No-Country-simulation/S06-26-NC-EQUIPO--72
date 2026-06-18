CREATE TABLE IF NOT EXISTS indicadores_territoriales (
    id SERIAL PRIMARY KEY,
    municipio VARCHAR(60),
    cluster VARCHAR(40),
    categoria VARCHAR(30),
    indicador VARCHAR(100),
    valor DECIMAL(15,4),
    unidad VARCHAR(30),
    fonte VARCHAR(50),
    codigo_origem VARCHAR(100),
    url_origem TEXT NULL,
    fecha_referencia DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
