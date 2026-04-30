import random
import numpy as np

CARACTERES_RAROS = ["@", "#", "$", "%", "&", "*", "?", "!"]

def ensuciar_datos(dato):
    if isinstance(dato, list):
        resultado = []
        for item in dato:
            if isinstance(item, dict):
                nuevo_item = {}
                for k, v in item.items():
                    prob = random.random()
                    if prob < 0.1:
                        nuevo_item[k] = None
                    elif prob < 0.2 and isinstance(v, str):
                        car = random.choice(CARACTERES_RAROS)
                        nuevo_item[k] = f"  {car}{v}{car}  "
                    elif prob < 0.3 and isinstance(v, (int, float)):
                        nuevo_item[k] = -abs(v)
                    else:
                        nuevo_item[k] = v
                resultado.append(nuevo_item)
            else:
                resultado.append(item)
        return resultado
    return dato
