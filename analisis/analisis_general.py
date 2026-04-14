from analisis.analisis_clientes import analizar_clientes_modular
from analisis.analisis_empleados import analizar_empleados_modular
from analisis.analisis_productos import analizar_productos_modular
from analisis.analisis_resumen import analizar_resumen


def armar_respuesta_completa_modular(usuarios, productos, ventas, mensajes, fuente_backend):
    respuesta = {
        "fuente_backend": fuente_backend,
        "mensajes": mensajes,
        "resumen": analizar_resumen(usuarios, productos, ventas),
    }

    respuesta.update(analizar_empleados_modular(ventas))
    respuesta.update(analizar_productos_modular(ventas))
    respuesta.update(analizar_clientes_modular(ventas))

    return respuesta
