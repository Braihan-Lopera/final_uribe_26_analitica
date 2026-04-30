import pandas as pd
import numpy as np

def analizar_productos_modular(ventas):
    if not ventas:
        return {
            "productos_analizados": [],
            "productos_populares": [],
            "descripcion_estadistica": {},
            "mensaje": "No hay datos de ventas"
        }

    registros_productos = []
    for v in ventas:
        for p in v.get('productos', []):
            p['venta_id'] = v.get('id')
            registros_productos.append(p)
            
    if not registros_productos:
        return {
            "productos_analizados": [],
            "productos_populares": [],
            "descripcion_estadistica": {},
            "mensaje": "No se encontraron detalles de productos en las ventas"
        }
        
    df = pd.DataFrame(registros_productos)
    
    analisis = df.groupby('producto_nombre').agg({
        'cantidad': 'sum',
        'precio_unitario': 'mean',
        'venta_id': 'count'
    }).rename(columns={
        'cantidad': 'unidades_vendidas',
        'precio_unitario': 'precio_promedio',
        'venta_id': 'veces_vendido'
    }).reset_index()
    
    analisis['ingresos_generados'] = analisis['unidades_vendidas'] * analisis['precio_promedio']
    
    populares = analisis.query("unidades_vendidas > 5")
    
    return {
        "productos_analizados": analisis.sort_values(by='unidades_vendidas', ascending=False).fillna(0).to_dict(orient='records'),
        "productos_populares": populares.fillna(0).to_dict(orient='records'),
        "descripcion_estadistica": analisis.describe().fillna(0).to_dict()
    }
