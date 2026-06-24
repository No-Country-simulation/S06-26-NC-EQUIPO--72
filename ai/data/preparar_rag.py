import json
import os
import pandas as pd
import tiktoken

PATH_DATASET = r"E:\S06-26-NC-EQUIPO--72\ai\data\tensor_mobilidade.csv"  
PATH_SALIDA = r"E:\S06-26-NC-EQUIPO--72\ai\data\dataset_sprint3_rag.json"

N_MUESTRAS_POR_GRUPO = 100  

REGIONES = ["São Paulo", "Buenos Aires", "Bogotá", "CDMX", "Santiago"]
PILAREAS = ["Formación", "Empleabilidad", "Experiencias", "Mentorías", "Salud Mental"]

enc = tiktoken.get_encoding("cl100k_base")

def recortar_a_tokens(texto, max_tokens=500):
    tokens = enc.encode(str(texto))
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return enc.decode(tokens)

def main():
    if not os.path.exists(PATH_DATASET):
        return

    columnas_necesarias = [
        "municipio", "income_cluster", "age_group", "download_bytes", 
        "upload_bytes", "rg_streaming", "rg_social", "rg_game", "rg_comunicacao"
    ]
    
    conteos_por_grupo = { (r, p): 0 for r in REGIONES for p in PILAREAS }
    chunks_procesados = []
    
    for chunk in pd.read_csv(PATH_DATASET, usecols=columnas_necesarias, chunksize=100000):
        m = chunk["municipio"].astype(str).str.lower()
        chunk["region"] = "Santiago"
        chunk.loc[m.str.contains("sao|paulo|sp", na=False), "region"] = "São Paulo"
        chunk.loc[m.str.contains("buenos|aires|ba", na=False), "region"] = "Buenos Aires"
        chunk.loc[m.str.contains("bogota", na=False), "region"] = "Bogotá"
        chunk.loc[m.str.contains("cdmx|mexico", na=False), "region"] = "CDMX"
        
        chunk["indicador"] = "Salud Mental"
        chunk.loc[chunk["rg_streaming"] > 50, "indicador"] = "Formación"
        chunk.loc[chunk["rg_social"] > 50, "indicador"] = "Empleabilidad"
        chunk.loc[chunk["rg_game"] > 50, "indicador"] = "Experiencias"
        chunk.loc[chunk["rg_comunicacao"] > 50, "indicador"] = "Mentorías"
        
        for (region, indicador), sub_df in chunk.groupby(["region", "indicador"]):
            if (region, indicador) not in conteos_por_grupo:
                continue
                
            actuales = conteos_por_grupo[(region, indicador)]
            if actuales >= N_MUESTRAS_POR_GRUPO:
                continue
                
            faltantes = N_MUESTRAS_POR_GRUPO - actuales
            muestras_a_tomar = min(len(sub_df), faltantes)
            
            if muestras_a_tomar > 0:
                muestra_estrato = sub_df.sample(n=muestras_a_tomar, random_state=42)
                conteos_por_grupo[(region, indicador)] += muestras_a_tomar
                
                for _, fila in muestra_estrato.iterrows():
                    dl_mb = round(fila["download_bytes"] / (1024 * 1024), 2)
                    ul_mb = round(fila["upload_bytes"] / (1024 * 1024), 2)
                    
                    texto_original = (
                        f"Usuario del segmento socioeconómico {fila['income_cluster']} y rango de edad {fila['age_group']}. "
                        f"Registra un consumo de red de {dl_mb} MB de descarga y {ul_mb} MB de subida. "
                        f"Muestra una alta correlación de uso en plataformas de conectividad orientadas al pilar de {indicador}, "
                        f"con un índice de tráfico de streaming de {fila['rg_streaming']} y social de {fila['rg_social']}."
                    )
                    
                    prefijo = f"[Región: {region}][Indicador: {indicador}] "
                    tokens_prefijo = len(enc.encode(prefijo))
                    tokens_disponibles = 500 - tokens_prefijo
                    
                    texto_recortado = recortar_a_tokens(texto_original, max_tokens=tokens_disponibles)
                    chunks_procesados.append({
                        "region": region,
                        "indicador": indicador,
                        "texto": f"{prefijo}{texto_recortado}"
                    })
        
        if all(cant >= N_MUESTRAS_POR_GRUPO for cant in conteos_por_grupo.values()):
            break

    with open(PATH_SALIDA, "w", encoding="utf-8") as f:
        json.dump(chunks_procesados, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()