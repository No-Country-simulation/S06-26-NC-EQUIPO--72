import pandas as pd
import os

print("==================================================================")
print("🔍 AUDITORÍA DE CALIDAD DE DATOS - GENERADOR DE REPORTES")
print("==================================================================\n")

def cargar_o_simular_vias(nombre_archivo):
    if os.path.exists(nombre_archivo):
        print(f"✅ ¡Archivo real '{nombre_archivo}' detectado! Cargando datos...")
        return pd.read_csv(nombre_archivo, dtype={"ecgi_origem": str, "ecgi_destino": str})
    
    print(f"⚠️ '{nombre_archivo}' no encontrado en la carpeta. Generando muestra de simulación para pruebas...")
    datos_prueba = {
        "ecgi_origem": ["12345", "12345", "67890", "11111", None],
        "municipio_origem": ["Florianopolis", "Florianopolis", "São José", "Florianópolis", "Palhoça"],
        "ecgi_destino": ["67890", "67890", "55555", "22222", "33333"],
        "n_usuarios": [150, 150, -10, 80, 45],
        "dist_km": [5.4, 5.4, 12.3, 350.0, 2.1]
    }
    return pd.DataFrame(datos_prueba)

df_vias = cargar_o_simular_vias("tensor_fluxo_vias.csv")

print("\n--- INICIANDO ESCANEO DE ANOMALÍAS ---")

nulos = df_vias.isnull().sum()
print("\n[1] Chequeo de campos vacíos (Nulos):")
print(nulos[nulos > 0] if nulos.sum() > 0 else "   ✅ No hay valores faltantes.")

dup = df_vias.duplicated().sum()
print(f"\n[2] Registros idénticos repetidos: {dup}")
if dup > 0:
    print("   ⚠️ Alerta: Hay filas duplicadas que están inflando las estadísticas.")

print("\n[3] Análisis de coherencia en los datos:")
anomalia_usuarios = df_vias[df_vias['n_usuarios'] < 0]
anomalia_distancia = df_vias[df_vias['dist_km'] > 200]

print(f"   - Registros con cantidad de usuarios inválida (negativa): {len(anomalia_usuarios)}")
print(f"   - Registros con distancias exageradas (> 200 km): {len(anomalia_distancia)}")

print("\n[4] Lista de municipios para control de texto y acentos:")
print(df_vias['municipio_origem'].dropna().unique())