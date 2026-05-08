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

def normalizar_talla(talla):
    if not isinstance(talla, str): return talla
    # Limpieza extrema de espacios
    t = talla.lower().strip()
    t = re.sub(r'\s+', '', t) # Quitamos TODO espacio interno para tallas (ej: "X L" -> "XL")
    
    # Diccionario expandido de equivalencias
    mapeo = {
        "extraextra": "XXL",
        "supergrande": "XL", "extragrande": "XL", "grandote": "XL", "muygrande": "XL",
        "grande": "L", "gran": "L",
        "mediano": "M", "mediana": "M", "medio": "M",
        "pequeño": "S", "pequeña": "S", "chico": "S", "chica": "S", "pequeñito": "S", "peque": "S",
        "muypequeño": "XS", "muypequeña": "XS", "mini": "XS", "chiquito": "XS", "chiquita": "XS"
    }
    
    for clave, valor in mapeo.items():
        if clave in t:
            return valor
            
    # Si ya es un código estándar, lo limpiamos y devolvemos en mayúsculas
    # Buscamos patrones como XL, M, S, XS dentro del texto
    for codigo in ["XXL", "XL", "XS", "S", "M", "L"]:
        if codigo.lower() in t:
            return codigo

    return t.upper() # Fallback final limpio

def limpiar_datos_dataframe(datos_crudos):
    if not datos_crudos:
        return pd.DataFrame()
    
    df = pd.DataFrame(datos_crudos)
    
    # RESPALDO: Guardar columnas que son listas (como detalles de productos) para que Pandas no las rompa
    columnas_lista = {}
    for col in df.columns:
        # Si el primer elemento no nulo es una lista, la respaldamos
        first_valid = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
        if isinstance(first_valid, list):
            columnas_lista[col] = df[col].copy()
    
    # Rellenar nulos antes de procesar para evitar errores de tipo
    df = df.replace({np.nan: None}) 
    
    columnas_texto = df.select_dtypes(include=['object', 'string']).columns
    for col in columnas_texto:
        if col not in columnas_lista:
            df[col] = df[col].fillna("No Registra").apply(str).apply(limpiar_texto)
    
    # Aplicar normalización de talla si existe la columna
    if 'talla' in df.columns:
        df['talla'] = df['talla'].apply(normalizar_talla)
    
    columnas_num = df.select_dtypes(include=[np.number, 'object']).columns
    for col in columnas_num:
        if col not in columnas_lista:
            if 'precio' in col.lower() or 'cantidad' in col.lower() or 'stock' in col.lower() or 'total' in col.lower():
                def limpiar_a_numero(v):
                    if pd.isna(v) or v is None: return 0
                    if isinstance(v, (int, float)): return int(v)
                    import re
                    nums = re.sub(r'[^0-9]', '', str(v))
                    return int(nums) if nums else 0
                df[col] = df[col].apply(limpiar_a_numero)
    
    # RESTAURAR: Devolver las listas originales
    for col, data in columnas_lista.items():
        df[col] = data
            
    # Garantizar que no queden NaNs de Pandas que rompen el JSON
    return df.where(pd.notnull(df), None)

def limpiar_datos(dato):
    if isinstance(dato, list):
        df_limpio = limpiar_datos_dataframe(dato)
        return df_limpio.to_dict(orient='records')
    return dato
