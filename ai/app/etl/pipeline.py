import os
import time
from app.etl.database import wait_for_database, engine
from sqlalchemy import text
from app.etl.loaders import (
    load_antenas,
    load_assinantes,
    load_concentracao,
    load_mobilidade_agregada,
    load_flujo_od,
    load_fluxo_vias
)
from app.etl.loaders_fast import (
    load_antenas_fast,
    load_assinantes_fast,
    load_concentracao_fast,
    load_mobilidade_agregada_fast,
    load_flujo_od_fast,
    load_fluxo_vias_fast
)

DATA_DIR = "/app/data"
TABLES_REQUIRED = ["antenas", "assinantes", "concentracao", "mobilidade_agregada", "flujo_od", "fluxo_vias"]

def check_data_dir():
    """Verifica que el directorio de datos exista y tenga archivos"""
    if not os.path.exists(DATA_DIR):
        print(f"Directorio de datos {DATA_DIR} no existe")
        return False
    files = os.listdir(DATA_DIR)
    if not files:
        print(f"Directorio de datos {DATA_DIR} está vacío")
        return False
    print(f"Encontrados archivos de datos: {files}")
    return True

def table_exists(table_name: str) -> bool:
    """Verifica si una tabla existe en la base de datos"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}'"
            ))
            return result.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar si la tabla {table_name} existe: {e}")
        return False

def wait_for_tables(max_retries: int = 60, retry_interval: int = 2):
    """
    Espera a que todas las tablas requeridas existan en la base de datos
    
    Args:
        max_retries: Número máximo de intentos
        retry_interval: Tiempo de espera entre intentos en segundos
    """
    retries = 0
    while retries < max_retries:
        all_tables_exist = all(table_exists(table) for table in TABLES_REQUIRED)
        
        if all_tables_exist:
            print("Todas las tablas requeridas existen!")
            return
        
        missing_tables = [table for table in TABLES_REQUIRED if not table_exists(table)]
        print(f"Esperando a que el backend cree las tablas... Faltantes: {missing_tables}")
        print(f"Intento {retries+1}/{max_retries} - esperando {retry_interval}s...")
        time.sleep(retry_interval)
        retries += 1
    
    raise Exception(f"Las tablas no se crearon después de {max_retries * retry_interval} segundos!")

def is_table_empty(table_name: str) -> bool:
    """
    Verifica si una tabla está vacía.
    
    Args:
        table_name: Nombre de la tabla a verificar
    
    Returns:
        True si la tabla está vacía, False en caso contrario
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            return count == 0
    except Exception as e:
        print(f"Error al verificar si la tabla {table_name} está vacía: {e}")
        return True  # Asumir vacía si hay error (tabla podría no existir aún)

def run_pipeline(use_fast_load: bool = True):
    """
    Ejecuta el pipeline ETL completo
    
    Args:
        use_fast_load: Si es True, usa LOAD DATA INFILE (5-10x más rápido)
    """
    print(f"Iniciando pipeline ETL {'(modo rápido)' if use_fast_load else '(modo normal)'}...")
    
    # Chequeos previos
    if not check_data_dir():
        print("Saltando pipeline ETL (no se encontraron datos)")
        return
    
    wait_for_database()
    wait_for_tables()  # Esperar a que el backend cree todas las tablas
    
    try:
        # Cargar tablas en orden respetando dependencias
        if is_table_empty("antenas"):
            if use_fast_load:
                load_antenas_fast()
            else:
                load_antenas()
        else:
            print("La tabla antenas ya tiene datos, saltando")
        
        if is_table_empty("assinantes"):
            if use_fast_load:
                load_assinantes_fast()
            else:
                load_assinantes()
        else:
            print("La tabla assinantes ya tiene datos, saltando")
        
        if is_table_empty("concentracao"):
            if use_fast_load:
                load_concentracao_fast()
            else:
                load_concentracao()
        else:
            print("La tabla concentracao ya tiene datos, saltando")
        
        if is_table_empty("mobilidade_agregada"):
            if use_fast_load:
                load_mobilidade_agregada_fast()
            else:
                load_mobilidade_agregada()
        else:
            print("La tabla mobilidade_agregada ya tiene datos, saltando")
        
        if is_table_empty("flujo_od"):
            if use_fast_load:
                load_flujo_od_fast()
            else:
                load_flujo_od()
        else:
            print("La tabla flujo_od ya tiene datos, saltando")
        
        if is_table_empty("fluxo_vias"):
            if use_fast_load:
                load_fluxo_vias_fast()
            else:
                load_fluxo_vias()
        else:
            print("La tabla fluxo_vias ya tiene datos, saltando")
        
        print("Pipeline ETL completado exitosamente!")
    except Exception as e:
        print(f"Error en pipeline ETL: {e}")
        print("Intentando con modo normal como fallback...")
        if use_fast_load:
            run_pipeline(use_fast_load=False)
