from analisis.analisis_clientes import analizar_clientes_modular
from analisis.analisis_empleados import analizar_empleados_modular
from analisis.analisis_productos import analizar_productos_modular
from analisis.analisis_resumen import analizar_resumen
import pandas as pd

def safe_serialize(data):
    if isinstance(data, pd.Series):
        return data.to_dict()
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    return data

def armar_respuesta_completa_modular(usuarios, productos, ventas, mensajes, fuente_backend):
    resumen = analizar_resumen(usuarios, productos, ventas)
    empleados = analizar_empleados_modular(ventas)
    productos_analisis = analizar_productos_modular(ventas)
    clientes = analizar_clientes_modular(ventas)

    respuesta = {
        "fuente_backend": fuente_backend,
        "mensajes": mensajes,
        "resumen": resumen,
        "empleados_que_mas_venden": empleados.get("ranking_general", []),
        "empleados_que_menos_venden": list(reversed(empleados.get("ranking_general", []))),
        "productos_mas_vendidos": productos_analisis.get("productos_analizados", []),
        "productos_menos_vendidos": list(reversed(productos_analisis.get("productos_analizados", []))),
        "clientes_que_mas_compran": clientes.get("clientes_top_compradores", []),
        "clientes_que_menos_compran": list(reversed(clientes.get("clientes_top_compradores", []))),
        "productos_analizados": productos_analisis.get("productos_analizados", []),
        "clientes_top_compradores": clientes.get("clientes_top_compradores", []),
        "estadisticas": {
            "ventas": safe_serialize(resumen.get("descripcion_estadistica_ventas", {})),
            "empleados": safe_serialize(empleados.get("estadisticas_ventas", {})),
            "productos": safe_serialize(productos_analisis.get("descripcion_estadistica", {})),
            "clientes": safe_serialize(clientes.get("descripcion_estadistica_clientes", {}))
        }
    }

    return respuesta
