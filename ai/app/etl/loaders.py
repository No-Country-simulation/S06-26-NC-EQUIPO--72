import os
import time
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.etl.database import engine

DATA_DIR = "/app/data"

def load_antenas():
    """Carga la tabla de antenas desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "antenas_flp.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando antenas")
        return
    
    df = pd.read_csv(file_path)
    # Seleccionar solo las columnas necesarias
    df = df[["ecgi", "cluster", "municipio", "lat", "lon"]]
    df["ecgi"] = df["ecgi"].astype(str)
    df.to_sql("antenas", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en antenas")

def load_assinantes():
    """Carga la tabla de assinantes desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "assinantes.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando assinantes")
        return
    
    df = pd.read_csv(file_path)
    # Seleccionar solo las columnas necesarias
    df = df[["assinante_hash", "home_cluster", "home_municipio", "income_cluster", "age_group", "mobility_pattern", "flag_flagship"]]
    df.to_sql("assinantes", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en assinantes")

def load_concentracao():
    """Carga la tabla de concentración desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "tensor_concentracao.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando concentracao")
        return
    
    df = pd.read_csv(file_path)
    # Seleccionar solo las columnas necesarias
    df = df[["ecgi", "cluster", "municipio", "day_date", "periodo", "n_usuarios", "download_bytes", "congestionamento_medio"]]
    # Transformaciones
    df["download_gb"] = df["download_bytes"] / 1e9
    df["rat_type_predominante"] = None
    # Eliminar columna original
    df = df.drop(columns=["download_bytes"])
    df.to_sql("concentracao", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en concentracao")

def load_with_retry(chunk, table_name, max_retries=5):
    """Carga un chunk con reintentos para manejar deadlocks"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            chunk.to_sql(table_name, engine, if_exists="append", index=False)
            return True
        except OperationalError as e:
            if "Deadlock found" in str(e):
                retry_count += 1
                wait_time = 2 ** retry_count  # Backoff exponencial
                print(f"Deadlock detectado (intento {retry_count}/{max_retries}) - esperando {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
    return False

def load_mobilidade_agregada():
    """Carga la tabla de mobilidade agregada desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "tensor_mobilidade.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando mobilidade_agregada")
        return
    
    print("Iniciando carga de mobilidade_agregada (16,798,060 filas)...")
    
    # Cargar en trozos para archivos grandes (tamaño reducido para evitar deadlocks)
    chunk_size = 5000
    total_rows = 0
    start_time = time.time()
    
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size), 1):
        # Seleccionar solo las columnas necesarias
        chunk = chunk[["ecgi", "cluster", "municipio", "day_date", "periodo_sessao", "income_cluster", "age_group", "rat_type", "n_sessoes", "download_bytes", "drop_pct", "congestionamento"]]
        # Transformaciones - renombrar columnas
        chunk = chunk.rename(columns={
            "periodo_sessao": "periodo",
            "drop_pct": "drop_pct_avg",
            "congestionamento": "congestionamento_avg"
        })
        
        # Cargar con reintentos para deadlocks
        success = load_with_retry(chunk, "mobilidade_agregada")
        
        if not success:
            print(f"Error al cargar chunk {i} después de reintentos - deteniendo")
            return
        
        total_rows += len(chunk)
        
        # Imprimir progreso cada 50 chunks
        if i % 50 == 0:
            elapsed = time.time() - start_time
            avg_speed = total_rows / elapsed
            print(f"Progreso: {total_rows:,} filas cargadas ({i} chunks) - {avg_speed:,.0f} filas/s")
    
    elapsed_total = time.time() - start_time
    print(f"Carga completa. {total_rows:,} filas en {elapsed_total:.1f} segundos ({total_rows/elapsed_total:,.0f} filas/s)")

def load_flujo_od():
    """Carga la tabla de flujo OD desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "tensor_od.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando flujo_od")
        return
    
    df = pd.read_csv(file_path)
    # Seleccionar solo las columnas necesarias 
    df = df[["cluster_origem", "municipio_origem", "cluster_destino", "municipio_destino", "n_usuarios", "n_viagens", "dist_media_km", "mesmo_cluster"]]
    df.to_sql("flujo_od", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en flujo_od")

def load_fluxo_vias():
    """Carga la tabla de fluxo vias desde el CSV correspondiente"""
    file_path = os.path.join(DATA_DIR, "tensor_fluxo_vias.csv")
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no encontrado, saltando fluxo_vias")
        return
    
    df = pd.read_csv(file_path)
    # Seleccionar solo las columnas que existen en la tabla
    df = df[["ecgi_origem", "cluster_origem", "ecgi_destino", "cluster_destino", "n_usuarios", "n_transicoes", "dist_km", "periodo_predominante", "pct_do_cluster_origem"]]
    df.to_sql("fluxo_vias", engine, if_exists="append", index=False)
    print(f"Cargadas {len(df)} filas en fluxo_vias")
