#!/usr/bin/env python3
"""
Script para mostrar las columnas y la cantidad de filas de cada archivo CSV en la carpeta data/
"""

from pathlib import Path
import csv

def main():
    # Ruta de la carpeta de datos
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_dir = BASE_DIR / "data"
    
    if not data_dir.exists():
        print(f"La carpeta {data_dir} no existe.")
        print(f"Crea la carpeta y coloca tus archivos CSV allí.")
        return
    
    # Obtener todos los archivos CSV
    csv_files = [f for f in data_dir.iterdir() if f.suffix == '.csv']
    
    if not csv_files:
        print(f"No se encontraron archivos CSV en {data_dir}")
        return
    
    print(f"Encontrados {len(csv_files)} archivos CSV:\n")
    
    # Mostrar columnas y filas de cada CSV
    for file_path in csv_files:
        filename = file_path.name
        try:
            # Obtener el tamaño del archivo
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            
            # Leer solo la primera línea para obtener las columnas
            columns = []
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i == 0:
                        columns = row
                        break
            
            # Contar filas (usando lectura en bloques)
            def count_lines_fast(fname):
                with open(str(fname), 'rb') as f:
                    bufgen = (buf.count(b'\n') for buf in iter(lambda: f.read(1024 * 1024), b''))
                    return sum(bufgen)
            
            total_rows = count_lines_fast(file_path)
            
            # Resta 1 porque la primera fila es el encabezado
            total_data_rows = total_rows - 1
            
            print(f"{filename}")
            print(f"-Tamaño: {file_size:.2f} MB")
            print(f"-Filas (datos): {total_data_rows:,}")
            print(f"-Columnas: {len(columns)}")
            for i, col in enumerate(columns, 1):
                print(f"     {i}. {col}")
            print()
            
        except Exception as e:
            print(f"Error al leer {filename}: {e}\n")

if __name__ == "__main__":
    main()
