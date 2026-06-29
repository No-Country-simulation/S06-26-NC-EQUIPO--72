from pathlib import Path
import csv
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def limpiar_municipio(nombre):
    return re.sub(r'\s*\(SC\)\s*', '', nombre).strip()

def limpiar_valor(valor):
    if valor == '-':
        return '0'
    return valor.strip()

def formatear_tabela10261():
    entrada = DATA_DIR / "tabela10261.csv"
    salida = DATA_DIR / "tabela10261.csv"
    
    encabezados = [
        'municipio',
        'cor_ou_raca',
        'total',
        'total_homens',
        'total_mulheres',
        'empregado_setor_privado_sem_carteira',
        'empregado_setor_privado_sem_carteira_homens',
        'empregado_setor_privado_sem_carteira_mulheres',
        'trabalhador_domestico',
        'trabalhador_domestico_homens',
        'trabalhador_domestico_mulheres',
        'conta_propria_sem_cnpj',
        'conta_propria_sem_cnpj_homens',
        'conta_propria_sem_cnpj_mulheres',
        'trabalhador_familiar_auxiliar',
        'trabalhador_familiar_auxiliar_homens',
        'trabalhador_familiar_auxiliar_mulheres'
    ]
    
    datos = []
    
    with open(entrada, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lineas = list(reader)
        
        for fila in lineas[6:10]:
            municipio = limpiar_municipio(fila[0])
            cor_ou_raca = fila[1].strip()
            valores = [limpiar_valor(v) for v in fila[2:]]
            datos.append([municipio, cor_ou_raca] + valores)
    
    with open(salida, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        writer.writerows(datos)
    
    print(f'Tabela 10261 formateada correctamente')

def formatear_tabela6580():
    entrada = DATA_DIR / "tabela6580.csv"
    salida = DATA_DIR / "tabela6580.csv"
    
    encabezados = [
        'municipio',
        'grupo_idade',
        'total',
        'total_homens',
        'total_mulheres',
        'forca_trabalho',
        'forca_trabalho_homens',
        'forca_trabalho_mulheres',
        'forca_trabalho_ocupada',
        'forca_trabalho_ocupada_homens',
        'forca_trabalho_ocupada_mulheres',
        'forca_trabalho_desocupada',
        'forca_trabalho_desocupada_homens',
        'forca_trabalho_desocupada_mulheres',
        'fora_da_forca_trabalho',
        'fora_da_forca_trabalho_homens',
        'fora_da_forca_trabalho_mulheres'
    ]
    
    datos = []
    
    with open(entrada, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lineas = list(reader)
        
        for fila in lineas[6:10]:
            municipio = limpiar_municipio(fila[0])
            grupo_idade = fila[1].strip()
            valores = [limpiar_valor(v) for v in fila[2:]]
            datos.append([municipio, grupo_idade] + valores)
    
    with open(salida, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        writer.writerows(datos)
    
    print(f'Tabela 6580 formateada correctamente')

if __name__ == '__main__':
    formatear_tabela10261()
    formatear_tabela6580()
