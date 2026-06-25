import os
import time
import mysql.connector
from app.core.config import settings
from sqlalchemy import text
from app.etl.database import engine

DATA_DIR = "/app/data"


def get_mysql_connection():
    """Obtiene una conexión directa a MySQL usando mysql-connector"""
    return mysql.connector.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        allow_local_infile=True
    )


def load_antenas_fast():
    """Carga la tabla de antenas usando LOAD DATA INFILE"""
    file_path = os.path.join(DATA_DIR, "antenas_flp.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando antenas")
        return
    
    print("Cargando antenas con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE antenas
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@ecgi, @cluster, @municipio, @lat, @lon)
        SET ecgi = CAST(@ecgi AS CHAR),
            cluster = @cluster,
            municipio = @municipio,
            lat = @lat,
            lon = @lon
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas en antenas en {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()


def load_assinantes_fast():
    """Carga la tabla de assinantes usando LOAD DATA INFILE"""
    file_path = os.path.join(DATA_DIR, "assinantes.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando assinantes")
        return
    
    print("Cargando assinantes con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE assinantes
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (assinante_hash, home_cluster, home_municipio, income_cluster, age_group, mobility_pattern, flag_flagship)
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas en assinantes en {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()


def load_concentracao_fast():
    """Carga la tabla de concentração usando LOAD DATA INFILE con transformaciones"""
    file_path = os.path.join(DATA_DIR, "tensor_concentracao.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando concentracao")
        return
    
    print("Cargando concentracao con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE concentracao
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@ecgi, @cluster, @municipio, @day_date, @periodo, @n_usuarios, @download_bytes, @congestionamento_medio)
        SET ecgi = CAST(@ecgi AS CHAR),
            cluster = @cluster,
            municipio = @municipio,
            day_date = @day_date,
            periodo = @periodo,
            n_usuarios = @n_usuarios,
            download_gb = @download_bytes / 1000000000,
            congestionamento_medio = @congestionamento_medio,
            rat_type_predominante = NULL
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas em concentracao em {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()


def load_mobilidade_agregada_fast():
    """Carga la tabla de mobilidade agregada usando LOAD DATA INFILE (el más rápido para archivos grandes)"""
    file_path = os.path.join(DATA_DIR, "tensor_mobilidade.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando mobilidade_agregada")
        return
    
    print("Cargando mobilidade_agregada con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE mobilidade_agregada
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@ecgi, @cluster, @municipio, @day_date, @periodo_sessao, @income_cluster, @age_group, @rat_type, @n_sessoes, @download_bytes, @drop_pct, @congestionamento)
        SET ecgi = CAST(@ecgi AS CHAR),
            cluster = @cluster,
            municipio = @municipio,
            day_date = @day_date,
            periodo = @periodo_sessao,
            income_cluster = @income_cluster,
            age_group = @age_group,
            rat_type = @rat_type,
            n_sessoes = @n_sessoes,
            download_gb = @download_bytes / 1000000000,
            drop_pct_avg = @drop_pct,
            congestionamento_avg = @congestionamento
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas en mobilidade_agregada en {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()


def load_flujo_od_fast():
    """Carga la tabla de flujo OD usando LOAD DATA INFILE"""
    file_path = os.path.join(DATA_DIR, "tensor_od.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando flujo_od")
        return
    
    print("Cargando flujo_od con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE flujo_od
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@cluster_origem, @municipio_origem, @cluster_destino, @municipio_destino, @n_usuarios, @n_viagens, @dist_media_km, @mesmo_cluster)
        SET cluster_origem = @cluster_origem,
            municipio_origem = @municipio_origem,
            cluster_destino = @cluster_destino,
            municipio_destino = @municipio_destino,
            n_usuarios = @n_usuarios,
            n_viagens = @n_viagens,
            dist_media_km = @dist_media_km,
            mesmo_cluster = @mesmo_cluster
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas en flujo_od en {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()


def load_fluxo_vias_fast():
    """Carga la tabla de fluxo vias usando LOAD DATA INFILE"""
    file_path = os.path.join(DATA_DIR, "tensor_fluxo_vias.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando fluxo_vias")
        return
    
    print("Cargando fluxo_vias con LOAD DATA INFILE...")
    start_time = time.time()
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    try:
        sql = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE fluxo_vias
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES
        (@ecgi_origem, @cluster_origem, @ecgi_destino, @cluster_destino, @n_usuarios, @n_transicoes, @dist_km, @periodo_predominante, @pct_do_cluster_origem)
        SET ecgi_origem = CAST(@ecgi_origem AS CHAR),
            cluster_origem = @cluster_origem,
            ecgi_destino = CAST(@ecgi_destino AS CHAR),
            cluster_destino = @cluster_destino,
            n_usuarios = @n_usuarios,
            n_transicoes = @n_transicoes,
            dist_km = @dist_km,
            periodo_predominante = @periodo_predominante,
            pct_do_cluster_origem = @pct_do_cluster_origem
        """
        cursor.execute(sql, (file_path,))
        conn.commit()
        
        elapsed = time.time() - start_time
        print(f"Cargadas {cursor.rowcount} filas en fluxo_vias en {elapsed:.2f}s")
    finally:
        cursor.close()
        conn.close()
