from __future__ import annotations

import random
from typing import Any


CARACTERES_RAROS = ["@", "#", "%", "¿", "?", "*", "~"]


def ensuciar_datos(dato: Any) -> Any:
    if isinstance(dato, dict):
        return {llave: ensuciar_datos(valor) for llave, valor in dato.items()}

    if isinstance(dato, list):
        return [ensuciar_datos(item) for item in dato]

    if isinstance(dato, str):
        caracter = random.choice(CARACTERES_RAROS)
        return f"  {caracter}{dato}{caracter}  "

    if isinstance(dato, bool):
        return dato

    if isinstance(dato, (int, float)):
        return -abs(dato)

    return dato
