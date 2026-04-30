import pandas as pd
import numpy as np
import re
import unicodedata

def limpiar_texto(texto):
    if not isinstance(texto, str): return texto
    texto = unicodedata.normalize('NFKC', texto)
    texto = re.sub(r'[@#\$%&\*\?!]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip().title()

def limpiar_datos_dataframe(datos_crudos):
    if not datos_crudos:
        return pd.DataFrame()
    
    df = pd.DataFrame(datos_crudos)
    
    columnas_texto = df.select_dtypes(include=['object']).columns
    for col in columnas_texto:
        df[col] = df[col].apply(limpiar_texto)
    
    columnas_num = df.select_dtypes(include=[np.number]).columns
    for col in columnas_num:
        df[col] = df[col].apply(lambda x: abs(x) if pd.notnull(x) else 0)
    
    for col in df.columns:
        if 'fecha' in col.lower() or 'nacimiento' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('No Registra')
        else:
            df[col] = df[col].fillna(0)
            
    return df

def limpiar_datos(dato):
    if isinstance(dato, list):
        df_limpio = limpiar_datos_dataframe(dato)
        return df_limpio.to_dict(orient='records')
    return dato
