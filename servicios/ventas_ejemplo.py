def construir_ventas_ejemplo():
    ventas = [
        {
            "id": "v-1",
            "empleado_id": "e-1",
            "empleado_nombre": "Laura Gomez",
            "cliente_id": "c-1",
            "cliente_nombre": "Carlos Ruiz",
            "estado": "PAGADA",
            "fecha": "2026-04-10",
            "productos": [
                {"producto_id": "p-1", "producto_nombre": "Camisa oversize", "cantidad": 5, "precio_unitario": 70000},
                {"producto_id": "p-2", "producto_nombre": "Pantalon vintage", "cantidad": 2, "precio_unitario": 95000},
            ],
        },
        {
            "id": "v-2",
            "empleado_id": "e-2",
            "empleado_nombre": "Mateo Perez",
            "cliente_id": "c-2",
            "cliente_nombre": "Ana Gil",
            "estado": "PAGADA",
            "fecha": "2026-04-11",
            "productos": [
                {"producto_id": "p-2", "producto_nombre": "Pantalon vintage", "cantidad": 1, "precio_unitario": 95000},
                {"producto_id": "p-3", "producto_nombre": "Buso clasico", "cantidad": 6, "precio_unitario": 85000},
            ],
        },
        {
            "id": "v-3",
            "empleado_id": "e-3",
            "empleado_nombre": "Sara Rios",
            "cliente_id": "c-1",
            "cliente_nombre": "Carlos Ruiz",
            "estado": "PAGADA",
            "fecha": "2026-04-12",
            "productos": [
                {"producto_id": "p-1", "producto_nombre": "Camisa oversize", "cantidad": 1, "precio_unitario": 70000},
                {"producto_id": "p-4", "producto_nombre": "Gorra urbana", "cantidad": 1, "precio_unitario": 40000},
            ],
        },
    ]

    for venta in ventas:
        venta["total"] = sum(item["cantidad"] * item["precio_unitario"] for item in venta["productos"])

    return ventas
