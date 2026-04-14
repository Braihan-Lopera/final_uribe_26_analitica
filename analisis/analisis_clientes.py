def analizar_clientes_modular(ventas):
    acumulado = {}

    for venta in ventas:
        llave = venta.get("cliente_id") or venta.get("cliente_nombre") or "SIN_CLIENTE"

        if llave not in acumulado:
            acumulado[llave] = {
                "cliente_id": venta.get("cliente_id"),
                "cliente_nombre": venta.get("cliente_nombre", "Sin cliente"),
                "compras_realizadas": 0,
                "monto_total_comprado": 0,
            }

        acumulado[llave]["compras_realizadas"] += 1
        acumulado[llave]["monto_total_comprado"] += float(venta.get("total", 0) or 0)

    ranking = sorted(acumulado.values(), key=lambda item: (item["monto_total_comprado"], item["compras_realizadas"]), reverse=True)
    ranking_inverso = sorted(acumulado.values(), key=lambda item: (item["monto_total_comprado"], item["compras_realizadas"]))

    return {
        "clientes_que_mas_compran": ranking[:5],
        "clientes_que_menos_compran": ranking_inverso[:5],
    }
