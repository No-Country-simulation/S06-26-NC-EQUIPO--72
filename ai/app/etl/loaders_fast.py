# loaders_fast.py
import os
import time
import traceback
import tempfile
import pandas as pd
import mysql.connector
from app.core.config import settings

DATA_DIR = "/app/data"

# helpers 

def get_conn():
    return mysql.connector.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        allow_local_infile=True,
    )


def _fast_load(cursor, conn, file_path: str, sql: str, label: str) -> int:
    """Ejecuta un LOAD DATA LOCAL INFILE y retorna rowcount."""
    cursor.execute(sql, (file_path,))
    conn.commit()
    return cursor.rowcount


def _bulk_insert(conn, cursor, table: str, columns: list[str], rows: list[tuple]) -> int:
    """executemany con placeholders — para cuando INFILE no aplica."""
    placeholders = ", ".join(["%s"] * len(columns))
    cols = ", ".join(columns)
    cursor.executemany(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
        rows,
    )
    conn.commit()
    return len(rows)


def _session_speed_settings(cursor):
    cursor.execute("SET SESSION foreign_key_checks = 0")
    cursor.execute("SET SESSION unique_checks = 0")
    cursor.execute("SET SESSION sql_mode = ''")


def _session_speed_restore(cursor):
    cursor.execute("SET SESSION foreign_key_checks = 1")
    cursor.execute("SET SESSION unique_checks = 1")


# loaders

def load_antenas_fast():
    path = os.path.join(DATA_DIR, "antenas_flp.csv")
    if not os.path.exists(path):
        print("  [antenas] archivo no encontrado, saltando", flush=True)
        return

    print(f"[antenas] LOAD DATA INFILE ({os.path.getsize(path):,} bytes)...", flush=True)
    t0 = time.time()
    conn = get_conn(); cur = conn.cursor()
    try:
        _session_speed_settings(cur)
        n = _fast_load(cur, conn, path, """
            LOAD DATA LOCAL INFILE %s
            INTO TABLE antenas
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
            IGNORE 1 LINES
            (@ecgi, @cluster, @municipio, @lat, @lon)
            SET ecgi = CAST(@ecgi AS CHAR),
                cluster = @cluster, municipio = @municipio,
                lat = @lat, lon = @lon
        """, "antenas")
        print(f"[antenas] {n:,} filas en {time.time()-t0:.1f}s", flush=True)
    except Exception:
        print("[antenas] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()


def load_assinantes_fast():
    path = os.path.join(DATA_DIR, "assinantes.csv")
    if not os.path.exists(path):
        print("  [assinantes] archivo no encontrado, saltando", flush=True)
        return

    print(f"[assinantes] LOAD DATA INFILE ({os.path.getsize(path):,} bytes)...", flush=True)
    t0 = time.time()
    conn = get_conn(); cur = conn.cursor()
    try:
        _session_speed_settings(cur)
        n = _fast_load(cur, conn, path, """
            LOAD DATA LOCAL INFILE %s
            INTO TABLE assinantes
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
            IGNORE 1 LINES
            (assinante_hash, home_cluster, home_municipio,
             income_cluster, age_group, mobility_pattern, flag_flagship)
        """, "assinantes")
        print(f"[assinantes] {n:,} filas en {time.time()-t0:.1f}s", flush=True)
    except Exception:
        print("[assinantes] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()


def load_mobilidade_agregada_fast():
    """
    Lee el CSV por chunks de 100k filas, escribe cada chunk en un archivo
    temporal y lo carga con LOAD DATA LOCAL INFILE.
    Ventajas: velocidad de INFILE + progreso visible + sin iterrows.
    """
    path = os.path.join(DATA_DIR, "tensor_mobilidade.csv")
    if not os.path.exists(path):
        print("  [mobilidade] archivo no encontrado, saltando", flush=True)
        return

    size_mb = os.path.getsize(path) / 1_048_576
    print(f"[mobilidade] carga por chunks via INFILE ({size_mb:.0f} MB)...", flush=True)
    t0 = time.time()
    total = 0
    CHUNK = 100_000

    conn = get_conn(); cur = conn.cursor()
    _session_speed_settings(cur)

    sql_load = """
        LOAD DATA LOCAL INFILE %s
        INTO TABLE mobilidade_agregada
        FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
        IGNORE 0 LINES
        (@ecgi, @cluster, @municipio, @day_date, @periodo,
         @income_cluster, @age_group, @rat_type, @n_sessoes,
         @download_bytes, @drop_pct_avg, @congestionamento_avg)
        SET ecgi = CAST(@ecgi AS CHAR),
            cluster = @cluster, municipio = @municipio,
            day_date = NULLIF(@day_date, '0000-00-00'),
            periodo = @periodo, income_cluster = @income_cluster,
            age_group = @age_group, rat_type = @rat_type,
            n_sessoes = @n_sessoes, download_bytes = @download_bytes,
            drop_pct_avg = @drop_pct_avg,
            congestionamento_avg = @congestionamento_avg
    """

    try:
        for i, chunk in enumerate(pd.read_csv(path, chunksize=CHUNK), 1):
            chunk = (
                chunk[["ecgi", "cluster", "municipio", "day_date", "periodo_sessao",
                        "income_cluster", "age_group", "rat_type", "n_sessoes",
                        "download_bytes", "drop_pct", "congestionamento"]]
                .rename(columns={
                    "periodo_sessao": "periodo",
                    "drop_pct": "drop_pct_avg",
                    "congestionamento": "congestionamento_avg",
                })
            )
            chunk["ecgi"] = chunk["ecgi"].astype(str)

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, newline=""
            ) as tmp:
                tmp_path = tmp.name
                chunk.to_csv(tmp, index=False, header=False)

            try:
                cur.execute(sql_load, (tmp_path,))
                conn.commit()
                total += cur.rowcount
            finally:
                os.unlink(tmp_path)

            elapsed = time.time() - t0
            speed = total / elapsed if elapsed else 0
            print(
                f"  [mobilidade] chunk {i:>4} | {total:>12,} filas | {speed:>8,.0f} f/s",
                flush=True,
            )

        print(f"[mobilidade] completado: {total:,} filas en {time.time()-t0:.1f}s", flush=True)

    except Exception:
        print("[mobilidade] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()


def load_concentracao_fast():
    path = os.path.join(DATA_DIR, "tensor_concentracao.csv")
    if not os.path.exists(path):
        print("  [concentracao] archivo no encontrado, saltando", flush=True)
        return

    print(f"[concentracao] LOAD DATA INFILE ({os.path.getsize(path):,} bytes)...", flush=True)
    t0 = time.time()
    conn = get_conn(); cur = conn.cursor()
    try:
        _session_speed_settings(cur)
        n = _fast_load(cur, conn, path, """
            LOAD DATA LOCAL INFILE %s
            INTO TABLE concentracao
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
            IGNORE 1 LINES
            (@ecgi, @cluster, @municipio, @day_date, @periodo,
             @n_usuarios, @download_bytes, @congestionamento_medio)
            SET ecgi = CAST(@ecgi AS CHAR),
                cluster = @cluster, municipio = @municipio,
                day_date = NULLIF(@day_date, '0000-00-00'),
                periodo = @periodo, n_usuarios = @n_usuarios,
                download_gb = @download_bytes / 1000000000,
                congestionamento_medio = @congestionamento_medio,
                rat_type_predominante = NULL
        """, "concentracao")
        print(f"[concentracao] {n:,} filas cargadas en {time.time()-t0:.1f}s", flush=True)

        # Calcular rat_type_predominante desde mobilidade_agregada
        print("[concentracao] calculando rat_type_predominante...", flush=True)
        t1 = time.time()
        cur.execute("""
            UPDATE concentracao c
            INNER JOIN (
                SELECT ecgi, day_date, periodo, rat_type
                FROM (
                    SELECT ecgi, day_date, periodo, rat_type,
                           ROW_NUMBER() OVER (
                               PARTITION BY ecgi, day_date, periodo
                               ORDER BY COUNT(*) DESC, rat_type
                           ) AS rn
                    FROM mobilidade_agregada
                    WHERE rat_type IS NOT NULL AND day_date IS NOT NULL
                    GROUP BY ecgi, day_date, periodo, rat_type
                ) ranked WHERE rn = 1
            ) m ON c.ecgi = m.ecgi AND c.day_date = m.day_date AND c.periodo = m.periodo
            SET c.rat_type_predominante = m.rat_type
        """)
        conn.commit()
        print(f"[concentracao] rat_type actualizado para {cur.rowcount:,} filas en {time.time()-t1:.1f}s", flush=True)

    except Exception:
        print("[concentracao] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()


def load_flujo_od_fast():
    path = os.path.join(DATA_DIR, "tensor_od.csv")
    if not os.path.exists(path):
        print("  [flujo_od] archivo no encontrado, saltando", flush=True)
        return

    print(f"[flujo_od] LOAD DATA INFILE ({os.path.getsize(path):,} bytes)...", flush=True)
    t0 = time.time()
    conn = get_conn(); cur = conn.cursor()
    try:
        _session_speed_settings(cur)
        n = _fast_load(cur, conn, path, """
            LOAD DATA LOCAL INFILE %s
            INTO TABLE flujo_od
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
            IGNORE 1 LINES
            (@cluster_origem, @municipio_origem, @cluster_destino,
             @municipio_destino, @n_usuarios, @n_viagens,
             @dist_media_km, @mesmo_cluster)
            SET cluster_origem = @cluster_origem,
                municipio_origem = @municipio_origem,
                cluster_destino = @cluster_destino,
                municipio_destino = @municipio_destino,
                n_usuarios = @n_usuarios, n_viagens = @n_viagens,
                dist_media_km = @dist_media_km,
                mesmo_cluster = @mesmo_cluster
        """, "flujo_od")
        print(f"[flujo_od] {n:,} filas en {time.time()-t0:.1f}s", flush=True)
    except Exception:
        print("[flujo_od] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()


def load_fluxo_vias_fast():
    path = os.path.join(DATA_DIR, "tensor_fluxo_vias.csv")
    if not os.path.exists(path):
        print("  [fluxo_vias] archivo no encontrado, saltando", flush=True)
        return

    print(f"[fluxo_vias] LOAD DATA INFILE ({os.path.getsize(path):,} bytes)...", flush=True)
    t0 = time.time()
    conn = get_conn(); cur = conn.cursor()
    try:
        _session_speed_settings(cur)
        n = _fast_load(cur, conn, path, """
            LOAD DATA LOCAL INFILE %s
            INTO TABLE fluxo_vias
            FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\\n'
            IGNORE 1 LINES
            (@ecgi_origem, @cluster_origem, @ecgi_destino, @cluster_destino,
             @n_usuarios, @n_transicoes, @dist_km,
             @periodo_predominante, @pct_do_cluster_origem)
            SET ecgi_origem = CAST(@ecgi_origem AS CHAR),
                cluster_origem = @cluster_origem,
                ecgi_destino = CAST(@ecgi_destino AS CHAR),
                cluster_destino = @cluster_destino,
                n_usuarios = @n_usuarios, n_transicoes = @n_transicoes,
                dist_km = @dist_km,
                periodo_predominante = @periodo_predominante,
                pct_do_cluster_origem = @pct_do_cluster_origem
        """, "fluxo_vias")
        print(f"[fluxo_vias] {n:,} filas en {time.time()-t0:.1f}s", flush=True)
    except Exception:
        print("[fluxo_vias] ERROR:", flush=True); traceback.print_exc(); raise
    finally:
        _session_speed_restore(cur); cur.close(); conn.close()