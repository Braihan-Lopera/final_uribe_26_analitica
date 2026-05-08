import requests
import json

def test_api():
    url = "http://127.0.0.1:8000/analisis/completo"
    payload = {"usar_datos_ejemplo": False}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        print("--- API TEST RESULT ---")
        print(f"Status Code: {response.status_code}")
        print(f"Mensajes: {data.get('mensajes', [])}")
        
        resumen = data.get('resumen', {})
        print(f"Total Ventas (Resumen): {resumen.get('total_ventas')}")
        print(f"Total Ingresos: {resumen.get('total_ingresos')}")
        
        ranking = data.get('productos_mas_vendidos', [])
        print(f"Productos en Ranking: {len(ranking)}")
        if ranking:
            print(f"Top Producto: {ranking[0].get('producto_nombre')}")
        
        ventas = data.get('ventas', []) # Ojo: ¿el endpoint devuelve 'ventas' o solo el analisis?
        # Revisando armar_respuesta_completa_modular, NO devuelve la lista de ventas crudas.
        
        if ranking:
            print("\nSUCCESS: Data is being generated correctly by Python.")
        else:
            print("\nFAILURE: Data is empty.")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_api()
