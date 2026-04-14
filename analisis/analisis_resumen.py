def contar_usuarios_por_rol(usuarios):
    conteo = {}

    for usuario in usuarios:
        rol = str(usuario.get("rol", "DESCONOCIDO")).upper()
        conteo[rol] = conteo.get(rol, 0) + 1

    return conteo


def analizar_resumen(usuarios, productos, ventas):
    total_ingresos = 0
    total_unidades = 0

    for venta in ventas:
        total_ingresos += float(venta.get("total", 0) or 0)

        for producto in venta.get("productos", []):
            total_unidades += float(producto.get("cantidad", 0) or 0)

    promedio = 0
    if ventas:
        promedio = round(total_ingresos / len(ventas), 2)

    return {
        "total_usuarios": len(usuarios),
        "total_productos": len(productos),
        "total_ventas": len(ventas),
        "total_ingresos": total_ingresos,
        "total_unidades_vendidas": total_unidades,
        "promedio_por_venta": promedio,
        "usuarios_por_rol": contar_usuarios_por_rol(usuarios),
    }
