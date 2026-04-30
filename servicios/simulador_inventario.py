import random

def generar_inventario_sucio(n=20):
    prendas = [
        "Camisa Polo", "Jean Skinny", "Chaqueta Bomber", "Camiseta Basica", 
        "Buso Hoodie", "Gorra Sport", "Bermuda Cargo", "Vestido Casual"
    ]
    tallas_reales = ["XS", "S", "M", "L", "XL"]
    tallas_error = ["Grandote", "Pequeñito", "Extra Mega", "Medio", "Súper Grande", "N/A"]
    
    inventario = []
    for i in range(n):
        nombre_base = random.choice(prendas)
        precio_base = random.randint(50000, 200000)
        
        prob_nombre = random.random()
        if prob_nombre < 0.3:
            nombre = f"  {nombre_base.upper()}  "
        elif prob_nombre < 0.6:
            nombre = nombre_base.lower().replace(" ", "   ")
        else:
            nombre = nombre_base
            
        prob_precio = random.random()
        if prob_precio < 0.2:
            precio = -precio_base
        elif prob_precio < 0.4:
            precio = str(precio_base) + " COP"
        else:
            precio = precio_base
            
        prob_talla = random.random()
        if prob_talla < 0.5:
            talla = random.choice(tallas_error)
        else:
            talla = random.choice(tallas_reales)
            
        inventario.append({
            "id": f"item-{i+1}",
            "nombre": nombre,
            "precio": precio,
            "talla": talla,
            "categoria": "General",
            "stock": random.randint(-5, 50)
        })
    return inventario
