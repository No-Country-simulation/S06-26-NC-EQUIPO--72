# pipeline.py
import os
import time
import traceback
from app.etl.database import wait_for_database, engine
from sqlalchemy import text
from app.etl.loaders_fast import (
    load_antenas_fast,
    load_assinantes_fast,
    load_concentracao_fast,
    load_mobilidade_agregada_fast,
    load_flujo_od_fast,
    load_fluxo_vias_fast,
)

DATA_DIR = "/app/data"
TABLES_REQUIRED = [
    "antenas", "assinantes", "concentracao",
    "mobilidade_agregada", "flujo_od", "fluxo_vias",
]

# Orden y función de carga para cada tabla
LOAD_ORDER = [
    ("antenas",              load_antenas_fast),
    ("assinantes",           load_assinantes_fast),
    ("mobilidade_agregada",  load_mobilidade_agregada_fast),
    ("concentracao",         load_concentracao_fast),   # depende de mobilidade
    ("flujo_od",             load_flujo_od_fast),
    ("fluxo_vias",           load_fluxo_vias_fast),
]


def check_data_dir() -> bool:
    if not os.path.exists(DATA_DIR):
        print(f"[ETL] Directorio {DATA_DIR} no existe", flush=True)
        return False
    files = os.listdir(DATA_DIR)
    if not files:
        print(f"[ETL] Directorio {DATA_DIR} vacío", flush=True)
        return False
    print(f"[ETL] Archivos disponibles: {files}", flush=True)
    return True


def table_exists(name: str) -> bool:
    try:
        with engine.connect() as conn:
            r = conn.execute(text(
                "SELECT 1 FROM information_schema.tables WHERE table_name = :t"
            ), {"t": name})
            return r.fetchone() is not None
    except Exception as e:
        print(f"[ETL] Error verificando tabla {name}: {e}", flush=True)
        return False


def wait_for_tables(max_retries: int = 60, interval: int = 2):
    for attempt in range(1, max_retries + 1):
        missing = [t for t in TABLES_REQUIRED if not table_exists(t)]
        if not missing:
            print("[ETL] Todas las tablas existen", flush=True)
            return
        print(f"[ETL] Esperando tablas {missing} ({attempt}/{max_retries})...", flush=True)
        time.sleep(interval)
    raise RuntimeError(f"Tablas no creadas tras {max_retries * interval}s")


def is_empty(table: str) -> bool:
    try:
        with engine.connect() as conn:
            return conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() == 0
    except Exception:
        return True


def run_pipeline():
    print("[ETL] Iniciando pipeline...", flush=True)

    if not check_data_dir():
        print("[ETL] Sin datos, abortando", flush=True)
        return

    wait_for_database()
    wait_for_tables()

    errors = []
    for table, loader in LOAD_ORDER:
        if not is_empty(table):
            print(f"[ETL] {table} ya tiene datos, saltando", flush=True)
            continue
        try:
            loader()
        except Exception as e:
            print(f"[ETL] FALLO en {table}: {e}", flush=True)
            errors.append(table)
            # Continúa con las siguientes tablas independientes
            # concentracao depende de mobilidade - si mobilidade falla, la saltamos
            if table == "mobilidade_agregada":
                print("[ETL] Saltando concentracao por dependencia con mobilidade", flush=True)
                errors.append("concentracao (saltada por dependencia)")
                # Marca concentracao para que no intente cargar
                LOAD_ORDER[3] = ("concentracao", lambda: None)

    if errors:
        print(f"[ETL] Pipeline completado con errores en: {errors}", flush=True)
    else:
        print("[ETL] Pipeline completado exitosamente", flush=True)



        