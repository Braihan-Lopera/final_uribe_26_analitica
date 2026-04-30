import pandas as pd

def analizar_empleados_modular(ventas):
    if not ventas:
        return {
            "ranking_general": [],
            "empleados_alto_rendimiento": [],
            "estadisticas_ventas": {},
            "mensaje": "No hay ventas para analizar"
        }
    
    df = pd.DataFrame(ventas)
    
    if 'empleado_nombre' not in df.columns:
        df['empleado_nombre'] = 'Desconocido'
    
    analisis = df.groupby('empleado_nombre').agg({
        'total': ['sum', 'count'],
        'id': 'nunique'
    })
    
    analisis.columns = ['ingresos_generados', 'ventas_realizadas', 'unidades_vendidas']
    analisis = analisis.reset_index()
    
    ranking = analisis.sort_values(by='ingresos_generados', ascending=False)
    
    promedio_ventas = ranking['ingresos_generados'].mean()
    empleados_top = ranking.query("ingresos_generados > @promedio_ventas")
    
    return {
        "ranking_general": ranking.fillna(0).to_dict(orient='records'),
        "empleados_alto_rendimiento": empleados_top.fillna(0).to_dict(orient='records'),
        "estadisticas_ventas": df['total'].describe().fillna(0).to_dict()
    }
