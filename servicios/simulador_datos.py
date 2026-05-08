import random
import uuid
from datetime import datetime, timedelta

def generar_ventas_simuladas(n=100, productos_reales=None):
    # Lista de productos profesionales para asegurar que el dashboard nunca esté vacío
    productos_quemados = [
        {"id": "p-1", "nombre": "Camisa Polo Slim Fit Azul", "precio": 145000},
        {"id": "p-2", "nombre": "Jean Skinny Negro Premium", "precio": 189900},
        {"id": "p-3", "nombre": "Chaqueta Bomber Verde Olivo", "precio": 245000},
        {"id": "p-4", "nombre": "Camiseta Algodón Orgánico S", "precio": 65000},
        {"id": "p-5", "nombre": "Buso Hoodie Gris Oversize", "precio": 125000},
        {"id": "p-6", "nombre": "Vestido Casual Floral", "precio": 175000},
        {"id": "p-7", "nombre": "Gorra Sport Runner", "precio": 45000},
        {"id": "p-8", "nombre": "Bermuda Cargo Beige", "precio": 95000},
        {"id": "p-9", "nombre": "Chaqueta Cuero Sintético", "precio": 320000},
        {"id": "p-10", "nombre": "Tenis Urban White", "precio": 210000}
    ]

    if productos_reales and len(productos_reales) > 0:
        productos_base = []
        for p in productos_reales:
            productos_base.append({
                "id": p.get("id", str(uuid.uuid4())),
                "nombre": p.get("nombre", "Prenda Genérica"),
                "precio": p.get("precio", 50000)
            })
    else:
        productos_base = productos_quemados

    vendedores = [
        {"id": "e-1", "nombre": "Juan Serna"},
        {"id": "e-2", "nombre": "Angie Saldarriaga"},
        {"id": "e-3", "nombre": "Harold Mejia"},
        {"id": "e-4", "nombre": "Poca Luz"},
        {"id": "e-5", "nombre": "Paloma Gamboa"},
    ]

    clientes = [
        {"id": "c-1", "nombre": "Juan Perez"},
        {"id": "c-2", "nombre": "Maria Lopez"},
        {"id": "c-3", "nombre": "Carlos Ruiz"},
        {"id": "c-4", "nombre": "Ana Garcia"},
        {"id": "c-5", "nombre": "Luis Rodriguez"},
    ]

    tallas = ["XS", "S", "M", "L", "XL", "XXL"]
    fecha_inicio = datetime(2026, 1, 1)
    ventas = []

    for i in range(n):
        vendedor = random.choice(vendedores)
        cliente = random.choice(clientes)
        num_productos = random.randint(1, 3)
        productos_venta = []
        total_venta = 0

        for _ in range(num_productos):
            prod = random.choice(productos_base)
            cantidad = random.randint(1, 5)
            precio = prod["precio"]
            
            # Inyectar errores aleatorios
            prob_error = random.random()
            nombre_prod = prod["nombre"]
            if prob_error < 0.1:
                nombre_prod = f"  {nombre_prod}  "
            elif prob_error < 0.2:
                nombre_prod = nombre_prod.upper()
            
            subtotal = cantidad * precio
            total_venta += subtotal
            
            productos_venta.append({
                "producto_id": f"p-{random.randint(1, 100)}",
                "producto_nombre": nombre_prod,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "subtotal": subtotal,
                "talla": random.choice(tallas)
            })

        fecha = fecha_inicio + timedelta(days=random.randint(0, 100))
        
        ventas.append({
            "id": str(uuid.uuid4()),
            "empleado_id": vendedor["id"],
            "empleado_nombre": vendedor["nombre"],
            "cliente_id": cliente["id"],
            "cliente_nombre": cliente["nombre"],
            "total": total_venta,
            "estado": "COMPLETADA",
            "fecha": fecha.strftime("%Y-%m-%d"),
            "productos": productos_venta
        })

    return ventas
