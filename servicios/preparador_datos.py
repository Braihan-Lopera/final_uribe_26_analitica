from servicios.simulador_datos import generar_ventas_simuladas
from servicios.backend_cliente import RUTAS_BACKEND, consumir_endpoint_get, intentar_consumir_ventas
from servicios.limpiador_datos import limpiar_datos
from servicios.normalizador_datos import extraer_lista_principal, normalizar_productos, normalizar_usuarios, normalizar_ventas

def preparar_datos_para_analisis_modular(solicitud):
    mensajes = []
    
    # 1. Obtener Usuarios y Productos
    try:
        usuarios_crudos = extraer_lista_principal(consumir_endpoint_get(RUTAS_BACKEND["usuarios"]))
    except Exception:
        usuarios_crudos = []

    try:
        productos_crudos = extraer_lista_principal(consumir_endpoint_get(RUTAS_BACKEND["productos"]))
    except Exception:
        productos_crudos = []

    # 2. Obtener o Generar Ventas
    ventas_crudas = list(solicitud.ventas)
    
    if solicitud.usar_datos_ejemplo:
        ventas_crudas = generar_ventas_simuladas(n=300)
        mensajes.append("Sistema operando con 300 registros simulados de alto rendimiento.")
    elif not ventas_crudas:
        ventas_crudas, _ = intentar_consumir_ventas()

    # 3. Aplicar Filtro de Vendedores (ANTES del análisis pero DESPUÉS de obtener las ventas)
    if hasattr(solicitud, 'filtros_vendedores') and solicitud.filtros_vendedores.nombre:
        nombre_buscado = solicitud.filtros_vendedores.nombre.lower()
        ventas_crudas = [v for v in ventas_crudas if nombre_buscado in v.get('empleado_nombre', '').lower() or nombre_buscado in v.get('vendedor', '').lower()]
        mensajes.append(f"Filtro ejecutivo aplicado para: {solicitud.filtros_vendedores.nombre}")

    # 4. Limpieza (Si se solicita)
    if solicitud.limpiar_datos:
        usuarios_crudos = limpiar_datos(usuarios_crudos)
        productos_crudos = limpiar_datos(productos_crudos)
        ventas_crudas = limpiar_datos(ventas_crudas)
        mensajes.append("Capa de limpieza Pandas ejecutada: Normalización completa.")

    # 5. Normalización Final
    usuarios = normalizar_usuarios(usuarios_crudos)
    productos = normalizar_productos(productos_crudos)
    ventas = normalizar_ventas(ventas_crudas)

    return usuarios, productos, ventas, mensajes
