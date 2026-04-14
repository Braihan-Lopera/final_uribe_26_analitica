def extraer_lista_principal(datos, permitir_dict_suelto=False):
    if isinstance(datos, list):
        return [dato for dato in datos if isinstance(dato, dict)]

    if isinstance(datos, dict):
        for llave in ["data", "datos", "result", "resultado", "content", "items"]:
            valor = datos.get(llave)
            if isinstance(valor, list):
                return [dato for dato in valor if isinstance(dato, dict)]

        if permitir_dict_suelto:
            return [datos]

    return []


def tomar_primer_valor(registro, posibles_llaves, valor_default=None):
    for llave in posibles_llaves:
        if llave in registro and registro[llave] not in (None, ""):
            return registro[llave]
    return valor_default


def convertir_a_float(valor, valor_default=0):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return valor_default


def normalizar_usuarios(usuarios_crudos):
    usuarios_normalizados = []

    for usuario in usuarios_crudos:
        nombres = tomar_primer_valor(usuario, ["nombres", "nombre", "firstName"], "")
        apellidos = tomar_primer_valor(usuario, ["apellidos", "apellido", "lastName"], "")
        nombre_completo = f"{nombres} {apellidos}".strip()

        usuarios_normalizados.append(
            {
                "id": tomar_primer_valor(usuario, ["id", "uuid", "usuarioId"]),
                "nombre": nombre_completo or tomar_primer_valor(usuario, ["correo", "email"], "Sin nombre"),
                "correo": tomar_primer_valor(usuario, ["correo", "email"], ""),
                "rol": str(tomar_primer_valor(usuario, ["rol", "role", "tipo"], "DESCONOCIDO")).upper(),
            }
        )

    return usuarios_normalizados


def normalizar_productos(productos_crudos):
    productos_normalizados = []

    for producto in productos_crudos:
        stock = producto.get("stock", [])
        if not isinstance(stock, list):
            stock = []

        stock_total = 0
        for item_stock in stock:
            if isinstance(item_stock, dict):
                cantidad = tomar_primer_valor(item_stock, ["cantidad", "stock", "units"], 0)
                try:
                    stock_total += float(cantidad)
                except (TypeError, ValueError):
                    continue

        productos_normalizados.append(
            {
                "id": tomar_primer_valor(producto, ["id", "uuid", "productoId"]),
                "nombre": tomar_primer_valor(producto, ["nombre", "name"], "Producto sin nombre"),
                "precio": convertir_a_float(tomar_primer_valor(producto, ["precio", "price"], 0) or 0),
                "categorias": producto.get("categorias", []),
                "stock_total": stock_total,
            }
        )

    return productos_normalizados


def normalizar_ventas(ventas_crudas):
    ventas_normalizadas = []

    for venta in ventas_crudas:
        detalle = tomar_primer_valor(venta, ["productos", "detalle", "items", "detalles"], [])
        if not isinstance(detalle, list):
            detalle = []

        productos = []
        total_calculado = 0

        for item in detalle:
            if not isinstance(item, dict):
                continue

            cantidad = convertir_a_float(tomar_primer_valor(item, ["cantidad", "units", "cantidadVendida"], 0) or 0)
            precio_unitario = convertir_a_float(
                tomar_primer_valor(item, ["precio_unitario", "precioUnitario", "precio"], 0) or 0
            )
            subtotal = cantidad * precio_unitario
            total_calculado += subtotal

            productos.append(
                {
                    "producto_id": tomar_primer_valor(item, ["producto_id", "productoId", "idProducto", "id"]),
                    "producto_nombre": tomar_primer_valor(item, ["producto_nombre", "nombre", "productoNombre"], "Producto sin nombre"),
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal,
                }
            )

        total = tomar_primer_valor(venta, ["total", "valorTotal", "montoTotal"], total_calculado)

        ventas_normalizadas.append(
            {
                "id": tomar_primer_valor(venta, ["id", "uuid", "ordenId", "ventaId"]),
                "empleado_id": tomar_primer_valor(venta, ["empleado_id", "empleadoId", "vendedor_id", "vendedorId"]),
                "empleado_nombre": tomar_primer_valor(venta, ["empleado_nombre", "empleado", "vendedor", "asesor"], "Sin vendedor"),
                "cliente_id": tomar_primer_valor(venta, ["cliente_id", "clienteId", "usuarioId"]),
                "cliente_nombre": tomar_primer_valor(venta, ["cliente_nombre", "cliente", "usuario"], "Sin cliente"),
                "total": convertir_a_float(total or 0),
                "estado": tomar_primer_valor(venta, ["estado", "status"], "DESCONOCIDO"),
                "fecha": tomar_primer_valor(venta, ["fecha", "createdAt", "fechaVenta"]),
                "productos": productos,
            }
        )

    return ventas_normalizadas
