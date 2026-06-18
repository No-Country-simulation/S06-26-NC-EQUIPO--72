from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


CHUNK_SIZE = 500_000
DTYPE_VIAS = {"ecgi_origem": str, "ecgi_destino": str}
DTYPE_SECUENCIAS = {"ecgi": str, "assinante_hash": "int32", "municipio": str}
DTYPE_ANTENAS = {"ecgi": str}
DTYPE_CONCENTRACAO = {"ecgi": str}
DTYPE_MOBILIDADE = {
    "ecgi": str,
    "assinante_hash": "int32",
    "income_cluster": str,
    "age_group": str,
    "rat_type": str
}
def mostrar_encabezado(titulo: str) -> None:
    """Imprime un separador visual limpio para la consola."""
    print("\n" + "=" * 66)
    print(f"🔍 {titulo}")
    print("=" * 66 + "\n")


def auditar_fluxo_vias(ruta_archivo: Path) -> None:
    """Audita el archivo de flujo de vías (volumen moderado)."""
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
    """Audita el archivo masivo de secuencias optimizando la memoria RAM con chunks."""
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
        
        print(f"   📦 Bloque {i} procesado de forma segura... ({total_registros:,} filas acumuladas)")

    print(f"\nREPORTE DE SECUENCIAS CONSOLIDADO ({ruta_archivo.name}):")
    print(f"- Total absoluto de filas leídas: {total_registros:,}")
    print(f"- Municipios con valores nulos detectados: {total_nulos_municipio}")
    print(f"- Registros con permanencia corrupta (< 0s): {total_permanencias_negativas}")

def auditar_antenas(ruta_archivo: Path) -> None:
    """Audita el catálogo de antenas (volumen mínimo)."""
    mostrar_encabezado("FASE 3: AUDITORÍA DE ANTENAS_FLP")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"Cargando archivo real: {ruta_archivo.name}")
    df_antenas = pd.read_csv(ruta_archivo, dtype=DTYPE_ANTENAS)

    nulos = df_antenas.isnull().sum()
    duplicados_ecgi = df_antenas.duplicated(subset=["ecgi"]).sum()
    lat_fuera_rango = len(df_antenas[(df_antenas["lat"] < -90) | (df_antenas["lat"] > 90)])
    lon_fuera_rango = len(df_antenas[(df_antenas["lon"] < -180) | (df_antenas["lon"] > 180)])

    print(f"\nRESULTADOS DE CALIDAD DE DATOS ({ruta_archivo.name}):")
    print(f"- Total registros evaluados: {len(df_antenas)}")
    print(f"- Campos vacíos (Nulos): {nulos[nulos > 0].to_dict() if nulos.sum() > 0 else 'Ninguno'}")
    print(f"- ECGI duplicados: {duplicados_ecgi if duplicados_ecgi > 0 else 'Ninguno'}")
    print(f"- Latitudes fuera de rango: {lat_fuera_rango if lat_fuera_rango > 0 else 'Ninguno'}")
    print(f"- Longitudes fuera de rango: {lon_fuera_rango if lon_fuera_rango > 0 else 'Ninguno'}")

    print("\nClusters detectados:")
    print(f"{df_antenas['cluster'].dropna().unique()}")
    print("\nMunicipalios detectados:")
    print(f"{df_antenas['municipio'].dropna().unique()}")


def auditar_assinantes(ruta_archivo: Path) -> None:
    """Audita el perfil demográfico de los suscriptores."""
    mostrar_encabezado("FASE 4: AUDITORÍA DE ASSINANTES")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"Cargando archivo real: {ruta_archivo.name}")
    df_assinantes = pd.read_csv(ruta_archivo)

    nulos = df_assinantes.isnull().sum()
    duplicados_hash = df_assinantes.duplicated(subset=["assinante_hash"]).sum()

    valores_income_validos = {"A", "B", "C", "D"}
    income_invalidos = df_assinantes[~df_assinantes["income_cluster"].isin(valores_income_validos)]

    valores_mobility_validos = {"BAIXA", "MODERADA", "INTENSA"}
    mobility_invalidos = df_assinantes[~df_assinantes["mobility_pattern"].isin(valores_mobility_validos)]

    print(f"\nRESULTADOS DE CALIDAD DE DATOS ({ruta_archivo.name}):")
    print(f"- Total registros evaluados: {len(df_assinantes)}")
    print(f"- Campos vacíos (Nulos): {nulos[nulos > 0].to_dict() if nulos.sum() > 0 else 'Ninguno'}")
    print(f"- assinante_hash duplicados: {duplicados_hash if duplicados_hash > 0 else 'Ninguno'}")
    print(f"- income_cluster con valores inválidos: {len(income_invalidos) if len(income_invalidos) > 0 else 'Ninguno'}")
    print(f"- mobility_pattern con valores inválidos: {len(mobility_invalidos) if len(mobility_invalidos) > 0 else 'Ninguno'}")

    print("\nValores únicos de age_group:")
    print(f"{df_assinantes['age_group'].dropna().unique()}")
    print("\nValores únicos de income_cluster:")
    print(f"{df_assinantes['income_cluster'].dropna().unique()}")
    print("\nValores únicos de mobility_pattern:")
    print(f"{df_assinantes['mobility_pattern'].dropna().unique()}")
    
def auditar_concentracao(ruta_archivo: Path) -> None:
    """Audita el archivo de concentración por antena, día y período."""
    mostrar_encabezado("FASE 5: AUDITORÍA DE TENSOR_CONCENTRACAO")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"Cargando archivo real: {ruta_archivo.name}")
    df_concentracao = pd.read_csv(ruta_archivo, dtype=DTYPE_CONCENTRACAO)

    print(f"\nColumnas reales encontradas en el CSV: {list(df_concentracao.columns)}")

    nulos = df_concentracao.isnull().sum()
    usuarios_negativos = len(df_concentracao[df_concentracao["n_usuarios"] < 0])

    print(f"\nRESULTADOS DE CALIDAD DE DATOS ({ruta_archivo.name}):")
    print(f"- Total registros evaluados: {len(df_concentracao)}")
    print(f"- Campos vacíos (Nulos): {nulos[nulos > 0].to_dict() if nulos.sum() > 0 else 'Ninguno'}")
    print(f"- Usuarios con conteo inválido (< 0): {usuarios_negativos if usuarios_negativos > 0 else 'Ninguno'}")

    # congestionamento_medio — validar solo si existe
    if "congestionamento_medio" in df_concentracao.columns:
        congestion_fuera_rango = len(df_concentracao[
            (df_concentracao["congestionamento_medio"] < 0) | (df_concentracao["congestionamento_medio"] > 1)
        ])
        print(f"-Congestionamento fuera de rango [0,1]: {congestion_fuera_rango if congestion_fuera_rango > 0 else 'Ninguno'}")
    else:
        print("-Confirmado: Columna 'congestionamento_medio' NO existe en el CSV")

    # periodo
    if "periodo" in df_concentracao.columns:
        valores_periodo_validos = {"MADRUGADA", "MANHA", "TARDE", "NOITE"}
        periodo_invalidos = df_concentracao[~df_concentracao["periodo"].isin(valores_periodo_validos)]
        print(f"-Confirmado: valores de 'periodo' inválidos: {len(periodo_invalidos) if len(periodo_invalidos) > 0 else 'Ninguno'}")
        print(f"\nValores únicos de periodo: {df_concentracao['periodo'].dropna().unique()}")

    # rat_type_predominante — esperado que NO exista según el schema doc
    if "rat_type_predominante" in df_concentracao.columns:
        print("-INESPERADO: 'rat_type_predominante' SÍ existe en el CSV crudo (el doc dice que se calcula aparte)")
    else:
        print("-Confirmado: 'rat_type_predominante' NO existe en el CSV crudo (se calcula desde tensor_mobilidade, como documenta el schema)")

    # download_bytes vs download_gb
    if "download_bytes" in df_concentracao.columns:
        print("-Confirmado: existe 'download_bytes' (se convierte a download_gb con /1e9 en el pipeline)")
    elif "download_gb" in df_concentracao.columns:
        print("-INESPERADO: 'download_gb' ya viene calculado en el CSV crudo")

    print(f"\nRango de fechas (day_date): {df_concentracao['day_date'].min()} → {df_concentracao['day_date'].max()}")
    
def auditar_od(ruta_archivo: Path) -> None:
    """Audita los pares Origen-Destino entre clusters."""
    mostrar_encabezado("FASE 6: AUDITORÍA DE TENSOR_OD")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"Cargando archivo real: {ruta_archivo.name}")
    df_od = pd.read_csv(ruta_archivo)

    nulos = df_od.isnull().sum()
    duplicados = df_od.duplicated().sum()
    usuarios_negativos = len(df_od[df_od["n_usuarios"] < 0])
    viagens_negativas = len(df_od[df_od["n_viagens"] < 0])

    columnas_schema = {"cluster_origem", "cluster_destino", "municipio_origem",
                        "municipio_destino", "n_usuarios", "n_viagens",
                        "dist_media_km", "mesmo_cluster"}
    columnas_faltantes = columnas_schema - set(df_od.columns)
    columnas_extra = set(df_od.columns) - columnas_schema

    print(f"\nRESULTADOS DE CALIDAD DE DATOS ({ruta_archivo.name}):")
    print(f"- Total registros evaluados: {len(df_od)}")
    print(f"- Campos vacíos (Nulos): {nulos[nulos > 0].to_dict() if nulos.sum() > 0 else 'Ninguno'}")
    print(f"- Registros duplicados: {duplicados if duplicados > 0 else 'Ninguno'}")
    print(f"- Usuarios con conteo inválido (< 0): {usuarios_negativos if usuarios_negativos > 0 else 'Ninguno'}")
    print(f"- Viagens con conteo inválido (< 0): {viagens_negativas if viagens_negativas > 0 else 'Ninguno'}")
    print(f"- Columnas del schema faltantes en el CSV: {columnas_faltantes if columnas_faltantes else 'Ninguna'}")
    print(f"- Columnas extra en el CSV (no están en el schema): {columnas_extra if columnas_extra else 'Ninguna'}")
    
def auditar_mobilidade(ruta_archivo: Path) -> None:
    """Audita el archivo masivo de mobilidade_agregada optimizando RAM con chunks."""
    mostrar_encabezado("FASE 7: AUDITORÍA EN BLOQUES - TENSOR_MOBILIDADE (2.7 GB)")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    print(f"Procesando {ruta_archivo.name} en bloques de {CHUNK_SIZE:,} líneas...")

    total_registros = 0
    total_nulos_por_columna = None
    total_sesiones_negativas = 0
    total_congestion_fuera_rango = 0
    valores_income_vistos = set()
    valores_rat_vistos = set()
    valores_periodo_vistos = set()
    columnas_reales = None

    lector_chunks = pd.read_csv(
        ruta_archivo,
        chunksize=CHUNK_SIZE,
        dtype=DTYPE_MOBILIDADE
    )

    for i, chunk in enumerate(lector_chunks, start=1):
        if columnas_reales is None:
            columnas_reales = list(chunk.columns)
            print(f"\nColumnas reales encontradas en el CSV: {columnas_reales}\n")

        total_registros += len(chunk)

        nulos_chunk = chunk.isnull().sum()
        total_nulos_por_columna = nulos_chunk if total_nulos_por_columna is None else total_nulos_por_columna + nulos_chunk

        if "n_sessoes" in chunk.columns:
            total_sesiones_negativas += len(chunk[chunk["n_sessoes"] < 0])

        # nombre real: 'congestionamento', no 'congestionamento_avg'
        if "congestionamento" in chunk.columns:
            total_congestion_fuera_rango += len(chunk[
                (chunk["congestionamento"] < 0) | (chunk["congestionamento"] > 1)
            ])

        if "income_cluster" in chunk.columns:
            valores_income_vistos.update(chunk["income_cluster"].dropna().unique())

        if "rat_type" in chunk.columns:
            valores_rat_vistos.update(chunk["rat_type"].dropna().unique())

        # nombre real: 'periodo_sessao', no 'periodo'
        if "periodo_sessao" in chunk.columns:
            valores_periodo_vistos.update(chunk["periodo_sessao"].dropna().unique())

        print(f"Bloque {i} procesado de forma segura... ({total_registros:,} filas acumuladas)")

    print(f"\nREPORTE DE MOBILIDADE CONSOLIDADO ({ruta_archivo.name}):")
    print(f"- Total absoluto de filas leídas: {total_registros:,}")
    print(f"- Campos vacíos (Nulos): {total_nulos_por_columna[total_nulos_por_columna > 0].to_dict() if total_nulos_por_columna.sum() > 0 else 'Ninguno'}")
    print(f"- n_sessoes con conteo inválido (< 0): {total_sesiones_negativas if total_sesiones_negativas > 0 else 'Ninguno'}")
    print(f"- congestionamento fuera de rango [0,1]: {total_congestion_fuera_rango if total_congestion_fuera_rango > 0 else 'Ninguno'}")
    print(f"\nValores únicos de income_cluster vistos: {valores_income_vistos}")
    print(f"Valores únicos de rat_type vistos: {valores_rat_vistos}")
    print(f"Valores únicos de periodo_sessao vistos: {valores_periodo_vistos}")

    columnas_schema_esperadas = {"ecgi", "cluster", "municipio", "day_date", "periodo",
                                   "income_cluster", "age_group", "rat_type", "n_sessoes",
                                   "download_bytes", "drop_pct_avg", "congestionamento_avg"}
    columnas_extra = set(columnas_reales) - columnas_schema_esperadas
    columnas_faltantes_con_otro_nombre = columnas_schema_esperadas - set(columnas_reales)

    print(f"\nColumnas del schema 'mobilidade_agregada' que no aparecen con ese nombre exacto en el CSV:")
    print(f"{columnas_faltantes_con_otro_nombre}")
    print(f"\nColumnas extra en el CSV no contempladas en 'mobilidade_agregada':")
    print(f"{columnas_extra}")



def analizar_nulos_od_en_detalle(ruta_archivo: Path) -> None:
    """Análisis forense de los nulos en municipio_origem/municipio_destino de tensor_od."""
    mostrar_encabezado("FASE 8: ANÁLISIS DETALLADO DE NULOS EN TENSOR_OD")

    if not ruta_archivo.exists():
        print(f"No se encontró '{ruta_archivo.name}' en la carpeta data. Saltando fase.")
        return

    df_od = pd.read_csv(ruta_archivo)

    filas_con_nulo = df_od[
        df_od["municipio_origem"].isnull() | df_od["municipio_destino"].isnull()
    ]

    print(f"Total de filas con algún nulo: {len(filas_con_nulo)}")
    

    if len(filas_con_nulo) == 0:
        print("No hay nulos para analizar.")
        return
    nulos_son_roçado = filas_con_nulo[
    (filas_con_nulo["cluster_origem"] == "SAO_JOSE_ROÇADO") | 
    (filas_con_nulo["cluster_destino"] == "SAO_JOSE_ROÇADO")
    ]
    print(f"Filas con nulo que involucran SAO_JOSE_ROÇADO: {len(nulos_son_roçado)} de {len(filas_con_nulo)}")    


    # ¿Coincide con mesmo_cluster?
    if "mesmo_cluster" in df_od.columns:
        distribucion_mesmo_cluster = filas_con_nulo["mesmo_cluster"].value_counts()
        print(f"\nDistribución de 'mesmo_cluster' en filas con nulo:")
        print(distribucion_mesmo_cluster.to_dict())

    # ¿Los nulos están en origen, destino o ambos?
    solo_origem_nulo = len(filas_con_nulo[
        filas_con_nulo["municipio_origem"].isnull() & filas_con_nulo["municipio_destino"].notnull()
    ])
    solo_destino_nulo = len(filas_con_nulo[
        filas_con_nulo["municipio_destino"].isnull() & filas_con_nulo["municipio_origem"].notnull()
    ])
    ambos_nulos = len(filas_con_nulo[
        filas_con_nulo["municipio_origem"].isnull() & filas_con_nulo["municipio_destino"].isnull()
    ])

    print(f"\nDesglose:")
    print(f"  - Solo municipio_origem nulo: {solo_origem_nulo}")
    print(f"  - Solo municipio_destino nulo: {solo_destino_nulo}")
    print(f"  - Ambos nulos: {ambos_nulos}")

    # ¿Qué clusters están involucrados en filas con nulo?
    print(f"\nClusters de origen involucrados en filas con nulo:")
    print(filas_con_nulo["cluster_origem"].dropna().unique())
    print(f"\nClusters de destino involucrados en filas con nulo:")
    print(filas_con_nulo["cluster_destino"].dropna().unique())

    # ¿Hay algún patrón en n_usuarios o n_viagens para estas filas?
    print(f"\nEstadísticas de n_usuarios en filas con nulo:")
    print(filas_con_nulo["n_usuarios"].describe())

    # Muestra completa de las filas problemáticas para inspección manual
    print(f"\nMuestra de filas con nulo (primeras 10):")
    print(filas_con_nulo.head(10).to_string())
    
    
def main() -> None:
    """Punto de entrada principal del script."""
    print("==================================================================")
    print("INICIANDO PIPELINE DE CALIDAD DE DATOS (BACKEND AI)")
    print("==================================================================")

    auditar_antenas(DATA_DIR / "antenas_flp.csv")
    auditar_assinantes(DATA_DIR / "assinantes.csv")
    auditar_concentracao(DATA_DIR / "tensor_concentracao.csv")
    auditar_od(DATA_DIR / "tensor_od.csv")
    analizar_nulos_od_en_detalle(DATA_DIR / "tensor_od.csv")
    auditar_fluxo_vias(DATA_DIR / "tensor_fluxo_vias.csv")
    auditar_mobilidade(DATA_DIR / "tensor_mobilidade.csv")

    print("\nProceso de auditoría finalizado.")


if __name__ == "__main__":
    main()