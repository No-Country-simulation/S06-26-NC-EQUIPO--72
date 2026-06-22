#!/usr/bin/env python3
"""
Script para corregir los 44 valores nulos en tensor_od.csv
Basado en el análisis de resultado_analisis.md
"""
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def corregir_tensor_od():
    """
    Corrige los valores nulos en tensor_od.csv usando antenas_flp.csv
    """
    print("=" * 80)
    print("Correccion tensor_od.csv")
    print("=" * 80)

    # Paso 1: Carga archivos
    try:
        antenas_df = pd.read_csv(DATA_DIR / "antenas_flp.csv", dtype={"ecgi": str})
        tensor_od_df = pd.read_csv(DATA_DIR / "tensor_od.csv")
    except FileNotFoundError as e:
        print(f"ERROR: Falta archivo - {e}")
        print("Por favor coloca los archivos CSV en la carpeta 'ai/data'")
        return

    print(f"Cargados:")
    print(f"- antenas_flp.csv: {len(antenas_df)} filas")
    print(f"- tensor_od.csv: {len(tensor_od_df)} filas")

    # Paso 2: Crea diccionario de cluster -> municipio y coordenadas
    cluster_info = antenas_df.groupby("cluster").agg(
        municipio=("municipio", "first"),
        lat=("lat", "mean"),  # Promedio de latitudes del cluster
        lon=("lon", "mean")   # Promedio de longitudes del cluster
    ).reset_index()

    cluster_dict = cluster_info.set_index("cluster").T.to_dict("list")

    print(f"\nInformación de clusters extraída: {len(cluster_dict)} clusters")

    # Paso 3: Cuenta nulos iniciales
    nulos_origen = tensor_od_df["municipio_origem"].isna().sum()
    nulos_destino = tensor_od_df["municipio_destino"].isna().sum()
    print(f"\nNulos iniciales:")
    print(f"- municipio_origem: {nulos_origen}")
    print(f"- municipio_destino: {nulos_destino}")
    print(f"- Total: {nulos_origen + nulos_destino}")

    # Paso 4: Corrige los valores nulos
    def corregir_fila(row):
        # Corrige origen
        if pd.isna(row["municipio_origem"]) and row["cluster_origem"] in cluster_dict:
            municipio, lat, lon = cluster_dict[row["cluster_origem"]]
            row["municipio_origem"] = municipio
            if pd.isna(row["lat_origem"]) or row["lat_origem"] == 0.0:
                row["lat_origem"] = lat
            if pd.isna(row["lon_origem"]) or row["lon_origem"] == 0.0:
                row["lon_origem"] = lon

        # Corrige destino
        if pd.isna(row["municipio_destino"]) and row["cluster_destino"] in cluster_dict:
            municipio, lat, lon = cluster_dict[row["cluster_destino"]]
            row["municipio_destino"] = municipio
            if pd.isna(row["lat_destino"]) or row["lat_destino"] == 0.0:
                row["lat_destino"] = lat
            if pd.isna(row["lon_destino"]) or row["lon_destino"] == 0.0:
                row["lon_destino"] = lon

        return row

    tensor_od_corregido = tensor_od_df.apply(corregir_fila, axis=1)

    # Paso 5: Verifica corrección
    nulos_origen_final = tensor_od_corregido["municipio_origem"].isna().sum()
    nulos_destino_final = tensor_od_corregido["municipio_destino"].isna().sum()
    print(f"\nNulos después de corrección:")
    print(f"- municipio_origem: {nulos_origen_final}")
    print(f"- municipio_destino: {nulos_destino_final}")

    # Paso 6: Guardar CSV corregido
    # Primero hace backup del original
    backup_file = DATA_DIR / "tensor_od.csv.original"
    if not backup_file.exists():
        tensor_od_df.to_csv(backup_file, index=False)
        print(f"\nBackup del original guardado en: {backup_file}")

    # Guarda el CSV corregido
    tensor_od_corregido.to_csv(DATA_DIR / "tensor_od.csv", index=False)
    print(f"\nCSV corregido guardado en: {DATA_DIR / 'tensor_od.csv'}")

    print("\n" + "=" * 80)
    print("Correccion completa!")
    print("=" * 80)


if __name__ == "__main__":
    corregir_tensor_od()
