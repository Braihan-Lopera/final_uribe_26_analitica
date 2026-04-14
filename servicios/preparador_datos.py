from servicios.backend_cliente import RUTAS_BACKEND
from servicios.backend_cliente import consumir_endpoint_get
from servicios.backend_cliente import intentar_consumir_ventas
from servicios.limpiador_datos import limpiar_datos
from servicios.normalizador_datos import extraer_lista_principal
from servicios.normalizador_datos import normalizar_productos
from servicios.normalizador_datos import normalizar_usuarios
from servicios.normalizador_datos import normalizar_ventas
from servicios.ventas_ejemplo import construir_ventas_ejemplo


def preparar_datos_para_analisis_modular(solicitud):
    mensajes = []

    usuarios_crudos = extraer_lista_principal(
        consumir_endpoint_get(RUTAS_BACKEND["usuarios"], solicitud.filtros_usuarios.model_dump())
    )
    productos_crudos = extraer_lista_principal(
        consumir_endpoint_get(RUTAS_BACKEND["productos"], solicitud.filtros_productos.model_dump())
    )

    ventas_crudas = list(solicitud.ventas)

    if not ventas_crudas:
        ventas_crudas, ruta_ventas = intentar_consumir_ventas()
        if ventas_crudas:
            mensajes.append(f"Las ventas se tomaron desde {ruta_ventas}.")

    if not ventas_crudas and solicitud.usar_datos_ejemplo:
        ventas_crudas = construir_ventas_ejemplo()
        mensajes.append("Se usaron ventas de ejemplo porque el backend no expone un listado claro en la coleccion.")

    if not ventas_crudas:
        mensajes.append("No se encontraron ventas en el backend. Puedes enviar ventas en el body o activar usar_datos_ejemplo.")

    if solicitud.limpiar_datos:
        usuarios_crudos = limpiar_datos(usuarios_crudos)
        productos_crudos = limpiar_datos(productos_crudos)
        ventas_crudas = limpiar_datos(ventas_crudas)
        mensajes.append("Los datos fueron limpiados antes del analisis.")

    usuarios = normalizar_usuarios(usuarios_crudos)
    productos = normalizar_productos(productos_crudos)
    ventas = normalizar_ventas(ventas_crudas)

    return usuarios, productos, ventas, mensajes
