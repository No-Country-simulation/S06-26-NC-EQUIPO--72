from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_RESULT_DIR = BASE_DIR / "data_resultado"

CHUNK_SIZE = 500_000

# Definir tipos de datos
DTYPES = {
    "antenas": {"ecgi": str},
    "concentracao": {"ecgi": str},
    "mobilidade": {"ecgi": str, "assinante_hash": "int32", "income_cluster": str, "age_group": str, "rat_type": str}
}


def mostrar_encabezado(titulo: str) -> None:
    print("\n" + "=" * 90)
    print(f"{titulo}")
    print("=" * 90 + "\n")


def responder_pregunta_1(antenas_df: pd.DataFrame) -> pd.DataFrame:
    """
    PREGUNTA 1: ¿Dónde hay concentración de personas pero cobertura de red precaria?
    """
    mostrar_encabezado("PREGUNTA 1: CONCENTRACIÓN ALTA + COBERTURA PRECARIA")
    
    df_conc = pd.read_csv(DATA_DIR / "tensor_concentracao.csv", dtype=DTYPES["concentracao"])
    
    # Paso 1: Calcular métricas por cluster (promedio general)
    cluster_metrics = df_conc.groupby(["cluster", "municipio"]).agg(
        avg_usuarios=("n_usuarios", "mean"),
        avg_congestion=("congestionamento_medio", "mean"),
        avg_drop=("drop_pct_medio", "mean")
    ).reset_index()
    
    # Paso 2: Obtener tecnología predominante por cluster
    print("Calculando tecnología predominante por cluster...")
    rat_type_list = []
    for chunk in pd.read_csv(DATA_DIR / "tensor_mobilidade.csv", chunksize=CHUNK_SIZE, dtype=DTYPES["mobilidade"]):
        chunk_rat = chunk.groupby(["cluster", "ecgi"])["rat_type"].agg(
            lambda x: x.mode()[0] if len(x.mode()) > 0 else None
        ).reset_index()
        rat_type_list.append(chunk_rat)
    
    df_rat = pd.concat(rat_type_list)
    cluster_tech = df_rat.groupby("cluster")["rat_type"].agg(
        lambda x: x.mode()[0] if len(x.mode()) > 0 else None
    ).reset_index()
    cluster_tech.columns = ["cluster", "tecnologia_predominante"]
    
    # Unir datos
    cluster_final = cluster_metrics.merge(cluster_tech, on="cluster", how="left")
    
    # Paso 3: Definir criterios de "cobertura precaria" y "alta concentración"
    # Usamos percentiles dinámicos
    umbral_usuarios = cluster_final["avg_usuarios"].quantile(0.60)  # Top 40% más concentrados
    umbral_congestion = cluster_final["avg_congestion"].quantile(0.70)  # Top 30% más congestionados
    umbral_drop = cluster_final["avg_drop"].quantile(0.70)  # Top 30% más drop
    
    print(f"\nCriterios definidos:")
    print(f"- Alta concentración: ≥ {umbral_usuarios:.0f} usuarios (percentil 60)")
    print(f"- Congestión alta: ≥ {umbral_congestion:.4f} (percentil 70)")
    print(f"- Drop alto: ≥ {umbral_drop:.4f} (percentil 70)")
    print(f"- Tecnología precaria: WCDMA (3G) como predominante")
    
    # Filtrar clusters prioritarios
    prioritarios = cluster_final[
        (cluster_final["avg_usuarios"] >= umbral_usuarios) &
        (
            (cluster_final["avg_congestion"] >= umbral_congestion) |
            (cluster_final["avg_drop"] >= umbral_drop) |
            (cluster_final["tecnologia_predominante"] == "WCDMA")
        )
    ].sort_values("avg_usuarios", ascending=False)
    
    print(f"\nZONAS PRIORITARIAS ENCONTRADAS: {len(prioritarios)}")
    if len(prioritarios) > 0:
        print("\nDETALLE DE ZONAS PRIORITARIAS:")
        print(prioritarios.to_string(index=False))
        
        # Guardar resultados
        prioritarios.to_csv(DATA_RESULT_DIR / "zonas_prioritarias_pregunta1.csv", index=False)
        print(f"\nResultados guardados en: {DATA_RESULT_DIR / 'zonas_prioritarias_pregunta1.csv'}")
    
    return prioritarios


def responder_pregunta_2(antenas_df: pd.DataFrame) -> pd.DataFrame:
    """
    PREGUNTA 2: ¿Qué regiones tienen más personas en horario laboral pero menos empleo formal registrado?
    NOTA: No tenemos datos DIRECTOS de empleo formal. Este análisis:
          1. Identifica zonas con alta concentración en horario laboral
          2. Indica qué datos EXTERNOS se necesitan para completar la respuesta
    """
    mostrar_encabezado("PREGUNTA 2: CONCENTRACIÓN LABORAL + EMPLEO FORMAL")
    
    df_conc = pd.read_csv(DATA_DIR / "tensor_concentracao.csv", dtype=DTYPES["concentracao"])
    
    # Paso 1: Filtrar solo horario laboral (MANHA: 6-12h, TARDE: 12-18h)
    laboral = df_conc[df_conc["periodo"].isin(["MANHA", "TARDE"])]
    
    # Paso 2: Calcular concentración laboral por cluster
    cluster_laboral = laboral.groupby(["cluster", "municipio"]).agg(
        avg_usuarios_laboral=("n_usuarios", "mean"),
        max_usuarios_laboral=("n_usuarios", "max"),
        total_registros=("n_usuarios", "count")
    ).reset_index().sort_values("avg_usuarios_laboral", ascending=False)
    
    print(f"\nTOP 15 ZONAS CON MAYOR CONCENTRACIÓN EN HORARIO LABORAL:")
    print(cluster_laboral.head(15).to_string(index=False))
    
    print("\nIMPORTANTE: LIMITACIÓN DEL DATASET")
    print("""
    El dataset NO incluye datos de empleo formal. Para responder completamente:
    NECESITAS DATOS EXTERNOS como:
    - Censo económico (IBGE)
    - Registro de empresas (CNPJ)
    - Datos de seguro de desempleo
    - Encuestas de hogares
    
    Con estos datos, podrías:
    1. Calcular la tasa de empleo formal por cluster
    2. Compararla con la concentración laboral del dataset
    3. Encontrar zonas con alta concentración pero baja tasa de empleo formal
    """)
    
    # Guardar resultados
    cluster_laboral.to_csv(DATA_RESULT_DIR / "concentracion_laboral_pregunta2.csv", index=False)
    print(f"\nDatos de concentración laboral guardados en: {DATA_RESULT_DIR / 'concentracion_laboral_pregunta2.csv'}")
    
    return cluster_laboral


def responder_pregunta_3(antenas_df: pd.DataFrame, zonas_prioritarias_p1: pd.DataFrame) -> pd.DataFrame:
    """
    PREGUNTA 3: ¿Dónde falta infraestructura de conectividad antes de que lleguen los programas sociales?
    Combina:
    1. Zonas con mala conectividad (de la pregunta 1)
    2. (Recomendación) Datos de necesidades sociales externas
    """
    mostrar_encabezado("PREGUNTA 3: INFRAESTRUCTURA PARA PROGRAMAS SOCIALES")
    
    if zonas_prioritarias_p1 is None or len(zonas_prioritarias_p1) == 0:
        print("No hay zonas prioritarias de la pregunta 1 para analizar")
        return None
    
    print("ZONAS DONDE PRIORIZAR INFRAESTRUCTURA ANTES DE PROGRAMAS SOCIALES:")
    print("(Ordenadas por concentración de usuarios, de mayor a menor)")
    print("\n" + zonas_prioritarias_p1[["cluster", "municipio", "avg_usuarios", "avg_congestion", "avg_drop", "tecnologia_predominante"]].to_string(index=False))
    
    print("\nRECOMENDACIONES PARA PROGRAMAS SOCIALES:")
    print("""
    1. PRIMERO: Mejorar la infraestructura en las zonas listadas
       - Aumentar capacidad de antenas congestionadas
       - Migrar de 3G a LTE/5G
       - Reducir la tasa de drop
    
    2. SEGUNDO: Implementar programas sociales en estas zonas
       - Programas de educación digital
       - Servicios públicos online
       - Telemedicina
       - Capacitación laboral
    
    3. DATOS EXTERNOS RECOMENDADOS para priorizar mejor:
       - Índice de vulnerabilidad social (IBGE)
       - Ubicación de escuelas y centros de salud
       - Datos de programas sociales existentes
    """)
    
    # Guardar recomendaciones
    zonas_prioritarias_p1.to_csv(DATA_RESULT_DIR / "zonas_programas_sociales_pregunta3.csv", index=False)
    print(f"\nZonas para programas sociales guardadas en: {DATA_RESULT_DIR / 'zonas_programas_sociales_pregunta3.csv'}")
    
    return zonas_prioritarias_p1


def main() -> None:
    print("=" * 90)
    print("ANÁLISIS ENFOCADO EN LAS 3 PREGUNTAS CLAVE DEL DESAFÍO")
    print("=" * 90)
    
    try:
        # Cargar antenas primero
        antenas = pd.read_csv(DATA_DIR / "antenas_flp.csv", dtype=DTYPES["antenas"])
        
        # Pregunta 1
        zonas_prioritarias = responder_pregunta_1(antenas)
        
        # Pregunta 2
        concentracion_laboral = responder_pregunta_2(antenas)
        
        # Pregunta 3
        responder_pregunta_3(antenas, zonas_prioritarias)
        
        print("\n" + "=" * 90)
        print("ANÁLISIS FINALIZADO!")
        print("=" * 90)
        
    except FileNotFoundError as e:
        print(f"\nERROR: No se encontró el archivo - {e}")
        print("Asegúrate de que todos los archivos CSV estén en la carpeta 'data'")
    except Exception as e:
        print(f"\nERROR INESPERADO: {type(e).__name__} - {e}")


if __name__ == "__main__":
    main()
