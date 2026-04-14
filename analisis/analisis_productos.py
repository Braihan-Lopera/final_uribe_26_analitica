def analizar_productos_modular(ventas):
    acumulado = {}

    for venta in ventas:
        for producto in venta.get("productos", []):
            llave = producto.get("producto_id") or producto.get("producto_nombre") or "SIN_PRODUCTO"

            if llave not in acumulado:
                acumulado[llave] = {
                    "producto_id": producto.get("producto_id"),
                    "producto_nombre": producto.get("producto_nombre", "Producto sin nombre"),
                    "unidades_vendidas": 0,
                    "ingresos_generados": 0,
                    "veces_vendido": 0,
                }

            cantidad = float(producto.get("cantidad", 0) or 0)
            precio_unitario = float(producto.get("precio_unitario", 0) or 0)
            subtotal = float(producto.get("subtotal", cantidad * precio_unitario))

            acumulado[llave]["unidades_vendidas"] += cantidad
            acumulado[llave]["ingresos_generados"] += subtotal
            acumulado[llave]["veces_vendido"] += 1

    ranking = sorted(acumulado.values(), key=lambda item: (item["unidades_vendidas"], item["ingresos_generados"]), reverse=True)
    ranking_inverso = sorted(acumulado.values(), key=lambda item: (item["unidades_vendidas"], item["ingresos_generados"]))

    return {
        "productos_mas_vendidos": ranking[:5],
        "productos_menos_vendidos": ranking_inverso[:5],
    }
