import unittest
from unittest.mock import patch

import requests
from fastapi.testclient import TestClient

import main


class MockResponse:
    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self._data = data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._data


class RobustezApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)
        self.body = {
            "filtros_usuarios": {"nombres": "", "apellidos": "", "correo": ""},
            "filtros_productos": {
                "nombre": "",
                "minPrecio": 0,
                "maxPrecio": 0,
                "categorias": [],
                "descuento": 0,
                "color": "",
            },
            "ventas": [],
            "usar_datos_ejemplo": False,
            "ensuciar_resultado": False,
            "limpiar_datos": True,
        }

    def test_extrae_ventas_desde_respuesta_envuelta(self):
        def mock_get(url, json=None, timeout=None):
            if url.endswith("/usuarios/listar"):
                return MockResponse(data=[])
            if url.endswith("/productos/buscar"):
                return MockResponse(data=[])
            if url.endswith("/ordenes/listar"):
                return MockResponse(
                    data={
                        "data": [
                            {
                                "id": "v1",
                                "total": 10,
                                "cliente_nombre": "Ana",
                                "empleado_nombre": "Luis",
                                "productos": [],
                            }
                        ]
                    }
                )
            return MockResponse(status_code=404, data={"error": "not found"})

        with patch("servicios.backend_cliente.requests.get", side_effect=mock_get):
            respuesta = self.client.post("/analisis/completo", json=self.body)

        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos["resumen"]["total_ventas"], 1)
        self.assertEqual(datos["resumen"]["total_ingresos"], 10.0)
        self.assertEqual(datos["resumen"]["total_unidades_vendidas"], 0.0)
        self.assertIn("/ordenes/listar", datos["mensajes"][0])

    def test_valores_invalidos_no_tumban_la_api(self):
        def mock_get(url, json=None, timeout=None):
            if url.endswith("/usuarios/listar"):
                return MockResponse(
                    data=[{"id": "u1", "nombres": "Ana", "apellidos": "Diaz", "rol": "CLIENTE"}]
                )
            if url.endswith("/productos/buscar"):
                return MockResponse(
                    data=[{"id": "p1", "nombre": "Camisa", "precio": "abc", "stock": [{"cantidad": "x"}]}]
                )
            return MockResponse(status_code=404, data={"error": "not found"})

        with patch("servicios.backend_cliente.requests.get", side_effect=mock_get):
            respuesta = self.client.post("/analisis/completo", json=self.body)

        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos["resumen"]["total_productos"], 1)
        self.assertEqual(datos["resumen"]["total_ventas"], 0)
        self.assertEqual(datos["productos_analizados"], [])
        self.assertIn("No se encontraron ventas", " ".join(datos["mensajes"]))

    def test_respuesta_dict_suelto_no_inventa_ventas(self):
        def mock_get(url, json=None, timeout=None):
            if url.endswith("/usuarios/listar"):
                return MockResponse(data=[])
            if url.endswith("/productos/buscar"):
                return MockResponse(data=[])
            if url.endswith("/ordenes/listar"):
                return MockResponse(data={"mensaje": "sin datos"})
            return MockResponse(status_code=404, data={"error": "not found"})

        with patch("servicios.backend_cliente.requests.get", side_effect=mock_get):
            respuesta = self.client.post("/analisis/completo", json=self.body)

        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertEqual(datos["resumen"]["total_ventas"], 0)
        self.assertEqual(datos["clientes_top_compradores"], [])

    def test_salud_endpoint(self):
        respuesta = self.client.get("/salud")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json(), {"estado": "ok"})

    def test_analisis_resumen_endpoint(self):
        def mock_get(url, json=None, timeout=None):
            return MockResponse(data=[])

        with patch("servicios.backend_cliente.requests.get", side_effect=mock_get):
            respuesta = self.client.post("/analisis/resumen", json=self.body)

        self.assertEqual(respuesta.status_code, 200)
        datos = respuesta.json()
        self.assertIn("resumen", datos)
        self.assertEqual(datos["resumen"]["total_ventas"], 0)
        self.assertNotIn("clientes_top_compradores", datos)


if __name__ == "__main__":
    unittest.main()
