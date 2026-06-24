import os
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

DATA_DIR = "/app/data"

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

def is_table_empty(table_name: str) -> bool:
    """
    Verifica si una tabla está vacía.
    
    Args:
        table_name: Nombre de la tabla a verificar
    
    Returns:
        True si la tabla está vacía o hay un error, False en caso contrario
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            return count == 0
    except Exception as e:
        print(f"Error al verificar si la tabla {table_name} está vacía: {e}")
        return True  # Asumir vacía si hay error (tabla podría no existir aún)

def run_pipeline():
    """Ejecuta el pipeline ETL completo"""
    print("Iniciando pipeline ETL...")
    
    # Chequeos previos
    if not check_data_dir():
        print("Saltando pipeline ETL (no se encontraron datos)")
        return
    
    wait_for_database()
    
    # Cargar tablas en orden respetando dependencias
    if is_table_empty("antenas"):
        load_antenas()
    else:
        print("La tabla antenas ya tiene datos, saltando")
    
    if is_table_empty("assinantes"):
        load_assinantes()
    else:
        print("La tabla assinantes ya tiene datos, saltando")
    
    if is_table_empty("concentracao"):
        load_concentracao()
    else:
        print("La tabla concentracao ya tiene datos, saltando")
    
    if is_table_empty("mobilidade_agregada"):
        load_mobilidade_agregada()
    else:
        print("La tabla mobilidade_agregada ya tiene datos, saltando")
    
    if is_table_empty("flujo_od"):
        load_flujo_od()
    else:
        print("La tabla flujo_od ya tiene datos, saltando")
    
    if is_table_empty("fluxo_vias"):
        load_fluxo_vias()
    else:
        print("La tabla fluxo_vias ya tiene datos, saltando")
    
    print("Pipeline ETL completado exitosamente!")
