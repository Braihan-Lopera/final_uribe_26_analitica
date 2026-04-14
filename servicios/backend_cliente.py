import os

import requests
from fastapi import HTTPException

from servicios.normalizador_datos import extraer_lista_principal


URL_BACKEND = os.getenv("URL_BACKEND", "http://localhost:8080")
TIMEOUT_BACKEND = int(os.getenv("TIMEOUT_BACKEND", "10"))

RUTAS_BACKEND = {
    "usuarios": "/usuarios/listar",
    "productos": "/productos/buscar",
}

RUTAS_VENTAS_CANDIDATAS = [
    "/ordenes/listar",
    "/ordenes/buscar",
    "/ventas/listar",
    "/ventas/buscar",
]


def consumir_endpoint_get(ruta, cuerpo=None):
    url = f"{URL_BACKEND}{ruta}"

    try:
        respuesta = requests.get(url, json=cuerpo, timeout=TIMEOUT_BACKEND)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as error:
        raise HTTPException(status_code=502, detail=f"No fue posible consumir {url}: {error}") from error
    except ValueError as error:
        raise HTTPException(status_code=502, detail=f"El backend no devolvio JSON valido en {url}") from error


def intentar_consumir_ventas():
    for ruta in RUTAS_VENTAS_CANDIDATAS:
        url = f"{URL_BACKEND}{ruta}"
        try:
            respuesta = requests.get(url, timeout=TIMEOUT_BACKEND)
            respuesta.raise_for_status()
            ventas = extraer_lista_principal(respuesta.json())
            if ventas:
                return ventas, ruta
        except (requests.RequestException, ValueError):
            continue

    return [], None
