import pandas as pd

def analizar_resumen(usuarios, productos, ventas):
    df_usuarios = pd.DataFrame(usuarios)
    df_productos = pd.DataFrame(productos)
    df_ventas = pd.DataFrame(ventas)
    
    if df_ventas.empty:
        return {
            "total_usuarios": len(usuarios),
            "total_productos": len(productos),
            "total_ventas": 0,
            "total_ingresos": 0,
            "total_unidades_vendidas": 0,
            "promedio_por_venta": 0,
            "usuarios_por_rol": {},
            "descripcion_estadistica_ventas": {}
        }

    usuarios_por_rol = {}
    if not df_usuarios.empty and 'rol' in df_usuarios.columns:
        usuarios_por_rol = df_usuarios['rol'].value_counts().to_dict()

    total_ingresos = df_ventas['total'].sum()
    promedio_venta = df_ventas['total'].mean()

    total_unidades = 0
    if 'productos' in df_ventas.columns:
        for productos_lista in df_ventas['productos']:
            if isinstance(productos_lista, list):
                for p in productos_lista:
                    if isinstance(p, dict):
                        total_unidades += p.get('cantidad', 0)

    return {
        "total_usuarios": len(usuarios),
        "total_productos": len(productos),
        "total_ventas": len(ventas),
        "total_ingresos": float(total_ingresos),
        "total_unidades_vendidas": float(total_unidades),
        "promedio_por_venta": float(promedio_venta),
        "usuarios_por_rol": usuarios_por_rol,
        "descripcion_estadistica_ventas": df_ventas['total'].describe().fillna(0).to_dict()
    }
