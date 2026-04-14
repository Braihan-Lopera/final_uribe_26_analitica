def analizar_empleados_modular(ventas):
    acumulado = {}

    for venta in ventas:
        llave = venta.get("empleado_id") or venta.get("empleado_nombre") or "SIN_EMPLEADO"

        if llave not in acumulado:
            acumulado[llave] = {
                "empleado_id": venta.get("empleado_id"),
                "empleado_nombre": venta.get("empleado_nombre", "Sin vendedor"),
                "ventas_realizadas": 0,
                "unidades_vendidas": 0,
                "ingresos_generados": 0,
            }

        acumulado[llave]["ventas_realizadas"] += 1
        acumulado[llave]["ingresos_generados"] += float(venta.get("total", 0) or 0)

        for producto in venta.get("productos", []):
            acumulado[llave]["unidades_vendidas"] += float(producto.get("cantidad", 0) or 0)

    ranking = sorted(acumulado.values(), key=lambda item: (item["ingresos_generados"], item["unidades_vendidas"]), reverse=True)
    ranking_inverso = sorted(acumulado.values(), key=lambda item: (item["ingresos_generados"], item["unidades_vendidas"]))

    return {
        "empleados_que_mas_venden": ranking[:5],
        "empleados_que_menos_venden": ranking_inverso[:5],
    }
