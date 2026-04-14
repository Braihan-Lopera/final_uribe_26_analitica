from __future__ import annotations

import re
import unicodedata
from typing import Any


PATRON_RUIDO = re.compile(r"[@#%¿?*~]")


def limpiar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)
    texto = PATRON_RUIDO.sub("", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def limpiar_numero(numero: int | float) -> int | float:
    return abs(numero)


def limpiar_datos(dato: Any) -> Any:
    if isinstance(dato, dict):
        return {llave: limpiar_datos(valor) for llave, valor in dato.items()}

    if isinstance(dato, list):
        return [limpiar_datos(item) for item in dato]

    if isinstance(dato, str):
        return limpiar_texto(dato)

    if isinstance(dato, bool):
        return dato

    if isinstance(dato, (int, float)):
        return limpiar_numero(dato)

    return dato
