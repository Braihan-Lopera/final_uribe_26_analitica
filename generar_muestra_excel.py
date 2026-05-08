import pandas as pd
import os

def crear_excel_ejemplo(ruta="catalogo_ejemplo.xlsx"):
    datos = [
        {
            "nombre": "  camisa POLO  ",
            "precio": "120000 COP",
            "talla": "XL",
            "color": "Azul",
            "categoria": "Masculino",
            "cantidad": 50
        },
        {
            "nombre": "jean skinny negro",
            "precio": -85000,
            "talla": "M",
            "color": "Negro",
            "categoria": "Unisex",
            "cantidad": 30
        },
        {
            "nombre": "CHAQUETA BOMBER",
            "precio": 250000,
            "talla": "pequeñito",
            "color": "Verde",
            "categoria": "General",
            "cantidad": 15
        },
        {
            "nombre": "camiseta basica",
            "precio": 45000,
            "talla": "S",
            "color": "Blanco",
            "categoria": "Femenino",
            "cantidad": 100
        }
    ]
    df = pd.DataFrame(datos)
    df.to_excel(ruta, index=False)
    print(f"Excel creado en: {os.path.abspath(ruta)}")

if __name__ == "__main__":
    crear_excel_ejemplo()
