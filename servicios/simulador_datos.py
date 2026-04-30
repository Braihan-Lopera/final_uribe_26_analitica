import random
import uuid
from datetime import datetime, timedelta

def generar_ventas_simuladas(n=100):
    productos_base = [
        {"nombre": "Camisa Polo Slim Fit", "precio": 150000},
        {"nombre": "Camisa Polo Classic Fit", "precio": 200000},
        {"nombre": "Jean Skinny Fit", "precio": 490000},
        {"nombre": "Jean Rider Slim", "precio": 357000},
        {"nombre": "Chaqueta Bomber Acolchada", "precio": 1500000},
        {"nombre": "Chaqueta Windbreaker", "precio": 680000},
        {"nombre": "Chaqueta Trucker Denim", "precio": 820000},
        {"nombre": "Camiseta Basica Algodon", "precio": 65000},
        {"nombre": "Buso Hoodie Oversize", "precio": 185000},
        {"nombre": "Gorra Sport Classic", "precio": 45000},
    ]

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
