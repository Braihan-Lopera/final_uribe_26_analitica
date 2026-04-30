import pandas as pd

def analizar_clientes_modular(ventas):
    if not ventas:
        return {
            "clientes_top_compradores": [],
            "descripcion_estadistica_clientes": {},
            "mensaje": "No hay ventas de clientes"
        }
        
    df = pd.DataFrame(ventas)
    
    
    analisis = df.groupby('cliente_nombre').agg({
        'total': ['sum', 'count']
    })
    
    analisis.columns = ['monto_total_comprado', 'compras_realizadas']
    analisis = analisis.reset_index()
    
    
    ranking = analisis.sort_values(by='monto_total_comprado', ascending=False)
    
    return {
        "clientes_top_compradores": ranking.fillna(0).to_dict(orient='records'),
        "descripcion_estadistica_clientes": analisis.describe().fillna(0).to_dict()
    }
