import pandas as pd
import io

def generar_excel_reporte(datos_analiticos):
    output = io.BytesIO()
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Asegurar que siempre exista al menos una hoja inicial
            pd.DataFrame({"Fecha Reporte": [pd.Timestamp.now()]}).to_excel(writer, sheet_name='Info General', index=False)

            # Empleados
            if 'empleados_que_mas_venden' in datos_analiticos:
                df_e = pd.DataFrame(datos_analiticos['empleados_que_mas_venden'])
                if not df_e.empty:
                    df_e.to_excel(writer, sheet_name='Productividad Equipo', index=False)

            # Productos
            if 'productos_mas_vendidos' in datos_analiticos:
                df_p = pd.DataFrame(datos_analiticos['productos_mas_vendidos'])
                if not df_p.empty:
                    df_p.to_excel(writer, sheet_name='Inventario y Ventas', index=False)

            # Clientes
            if 'clientes_que_mas_compran' in datos_analiticos:
                df_c = pd.DataFrame(datos_analiticos['clientes_que_mas_compran'])
                if not df_c.empty:
                    df_c.to_excel(writer, sheet_name='Ranking Clientes', index=False)
                    
            # Estadísticas (Requerimiento Pandas)
            if 'estadisticas' in datos_analiticos:
                for key, val in datos_analiticos['estadisticas'].items():
                    if val:
                        # Convertir diccionario de describe() a DataFrame
                        df_s = pd.DataFrame(val)
                        df_s.to_excel(writer, sheet_name=f'Stats {key.capitalize()}', index=True)

        return output.getvalue()
    except Exception as e:
        print(f"Error generando Excel: {e}")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame({"Error": [str(e)]}).to_excel(writer, sheet_name='Error', index=False)
        return output.getvalue()
