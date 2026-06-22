from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CHUNK_SIZE = 500_000
DTYPE_VIAS = {"ecgi_origem": str, "ecgi_destino": str}
DTYPE_SECUENCIAS = {"ecgi": str, "assinante_hash": "int32", "municipio": str}


def mostrar_encabezado(titulo: str) -> None:
    print("\n" + "=" * 66)
    print(f"🔍 {titulo}")
    print("=" * 66 + "\n")


def auditar_fluxo_vias(ruta_archivo: Path) -> None:
    mostrar_encabezado("FASE 1: AUDITORÍA DE TENSOR_FLUXO_VIAS")

    if not ruta_archivo.exists():
        print(f"⚠️ No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"✅ Cargando archivo real: {ruta_archivo.name}")
    df_vias = pd.read_csv(ruta_archivo, dtype=DTYPE_VIAS)

    nulos = df_vias.isnull().sum()
    duplicados = df_vias.duplicated().sum()
    usuarios_negativos = len(df_vias[df_vias["n_usuarios"] < 0])
    distancias_exageradas = len(df_vias[df_vias["dist_km"] > 200])

    print(f"\n📊 RESULTADOS DE CALIDAD DE DATOS ({ruta_archivo.name}):")
    print(f"   - Total registros evaluados: {len(df_vias)}")
    print(f"   - Campos vacíos (Nulos): {nulos[nulos > 0].to_dict() if nulos.sum() > 0 else '✅ Ninguno'}")
    print(f"   - Registros duplicados: {duplicados if duplicados > 0 else '✅ Ninguno'}")
    print(f"   - Usuarios con conteo inválido (< 0): {usuarios_negativos if usuarios_negativos > 0 else '✅ Ninguno'}")
    print(f"   - Distancias fuera de rango (> 200 km): {distancias_exageradas if distancias_exageradas > 0 else '✅ Ninguno'}")
    
    print("\n📍 Municipios detectados de origen (Check de texto):")
    print(f"     {df_vias['municipio_origem'].dropna().unique()}")


def auditar_tensor_sequencias(ruta_archivo: Path) -> None:
    mostrar_encabezado("FASE 2: AUDITORÍA EN BLOQUES - TENSOR_SEQUENCIAS (915 MB)")

    if not ruta_archivo.exists():
        print(f"⚠️ No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"🚀 Procesando {ruta_archivo.name} en bloques de {CHUNK_SIZE:,} líneas...")

    total_registros = 0
    total_nulos_municipio = 0
    total_permanencias_negativas = 0

    lector_chunks = pd.read_csv(
        ruta_archivo,
        chunksize=CHUNK_SIZE,
        dtype=DTYPE_SECUENCIAS,
        parse_dates=["arrival_time", "day_date"]
    )

    for i, chunk in enumerate(lector_chunks, start=1):
        total_registros += len(chunk)
        total_nulos_municipio += chunk["municipio"].isnull().sum()
        total_permanencias_negativas += len(chunk[chunk["permanencia_seg"] < 0])
        
        print(f"   📦 Bloque {i} processed... ({total_registros:,} filas acumuladas)")

    print(f"\n📊 REPORTE DE SECUENCIAS CONSOLIDADO ({ruta_archivo.name}):")
    print(f"   - Total absoluto de filas leídas: {total_registros:,}")
    print(f"   - Municipios con valores nulos detectados: {total_nulos_municipio}")
    print(f"   - Registros con permanencia corrupta (< 0s): {total_permanencias_negativas}")


def main() -> None:
    print("==================================================================")
    print("⚙️ INICIANDO PIPELINE DE CALIDAD DE DATOS (BACKEND AI)")
    print("==================================================================")
    
    archivo_vias = DATA_DIR / "tensor_fluxo_vias.csv"
    archivo_seq = DATA_DIR / "tensor_sequencias.csv"

    auditar_fluxo_vias(archivo_vias)
    auditar_tensor_sequencias(archivo_seq)
    
    mostrar_encabezado("ÉPICA 0.7: GENERANDO SUBCOJUNTO MOCK PARA BACKEND")

    if archivo_vias.exists():
        df_vias_mock = pd.read_csv(archivo_vias, dtype=DTYPE_VIAS, nrows=50)
        ruta_json_vias = DATA_DIR / "mock_fluxo_vias.json"
        df_vias_mock.to_json(ruta_json_vias, orient="records", indent=4, force_ascii=False)
        print(f"✅ Mock JSON creado con éxito: {ruta_json_vias.name} (50 filas)")

    if archivo_seq.exists():
        df_seq_mock = pd.read_csv(archivo_seq, dtype=DTYPE_SECUENCIAS, nrows=50, parse_dates=["arrival_time", "day_date"])
        df_seq_mock["arrival_time"] = df_seq_mock["arrival_time"].astype(str)
        df_seq_mock["day_date"] = df_seq_mock["day_date"].astype(str)
        
        ruta_json_seq = DATA_DIR / "mock_tensor_sequencias.json"
        df_seq_mock.to_json(ruta_json_seq, orient="records", indent=4, force_ascii=False)
        print(f"✅ Mock JSON creado con éxito: {ruta_json_seq.name} (50 filas)")
    
    print("\n✅ Proceso de auditoría y generación de mocks finalizado.")


if __name__ == "__main__":
    main()