from fastapi import FastAPI
from pydantic import BaseModel, Field

from analisis.analisis_clientes import analizar_clientes_modular
from analisis.analisis_general import armar_respuesta_completa_modular
from analisis.analisis_empleados import analizar_empleados_modular
from analisis.analisis_productos import analizar_productos_modular
from servicios.ensuciador_datos import ensuciar_datos
from servicios.limpiador_datos import limpiar_datos
from servicios.backend_cliente import URL_BACKEND
from servicios.preparador_datos import preparar_datos_para_analisis_modular


app = FastAPI(
    title="API de analisis para ecommerce",
    version="1.1.0",
    description="API sencilla para analisis academicos sobre un ecommerce.",
)


class FiltroUsuarios(BaseModel):
    nombres: str = ""
    apellidos: str = ""
    correo: str = ""


class FiltroProductos(BaseModel):
    nombre: str = ""
    minPrecio: float = 0
    maxPrecio: float = 0
    categorias: list = Field(default_factory=list)
    descuento: float = 0
    color: str = ""


class SolicitudAnalisis(BaseModel):
    filtros_usuarios: FiltroUsuarios = Field(default_factory=FiltroUsuarios)
    filtros_productos: FiltroProductos = Field(default_factory=FiltroProductos)
    ventas: list = Field(default_factory=list)
    usar_datos_ejemplo: bool = False
    ensuciar_resultado: bool = False
    limpiar_datos: bool = True


class SolicitudTransformacion(BaseModel):
    registros: list = Field(default_factory=list)


def construir_respuesta_analitica(solicitud):
    usuarios, productos, ventas, mensajes = preparar_datos_para_analisis_modular(solicitud)

    respuesta = armar_respuesta_completa_modular(usuarios, productos, ventas, mensajes, URL_BACKEND)

    if solicitud.ensuciar_resultado:
        respuesta = ensuciar_datos(respuesta)

    return respuesta


@app.get("/")
def inicio():
    return {
        "mensaje": "API de analisis lista para ecommerce universitario.",
        "backend_configurado": URL_BACKEND,
        "documentacion": "/docs",
    }


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.post("/analisis/completo")
def analisis_completo(solicitud: SolicitudAnalisis):
    return construir_respuesta_analitica(solicitud)


@app.post("/analisis/resumen")
def analisis_resumen(solicitud: SolicitudAnalisis):
    datos = construir_respuesta_analitica(solicitud)
    return {
        "fuente_backend": datos["fuente_backend"],
        "mensajes": datos["mensajes"],
        "resumen": datos["resumen"],
    }


@app.post("/analisis/empleados")
def analisis_empleados(solicitud: SolicitudAnalisis):
    usuarios, productos, ventas, mensajes = preparar_datos_para_analisis_modular(solicitud)
    return {
        "fuente_backend": URL_BACKEND,
        "mensajes": mensajes,
        "resumen": {"total_usuarios": len(usuarios), "total_productos": len(productos), "total_ventas": len(ventas)},
        "analisis_empleados": analizar_empleados_modular(ventas),
    }


@app.post("/analisis/productos")
def analisis_productos(solicitud: SolicitudAnalisis):
    usuarios, productos, ventas, mensajes = preparar_datos_para_analisis_modular(solicitud)
    return {
        "fuente_backend": URL_BACKEND,
        "mensajes": mensajes,
        "resumen": {"total_usuarios": len(usuarios), "total_productos": len(productos), "total_ventas": len(ventas)},
        "analisis_productos": analizar_productos_modular(ventas),
    }


@app.post("/analisis/clientes")
def analisis_clientes(solicitud: SolicitudAnalisis):
    usuarios, productos, ventas, mensajes = preparar_datos_para_analisis_modular(solicitud)
    return {
        "fuente_backend": URL_BACKEND,
        "mensajes": mensajes,
        "resumen": {"total_usuarios": len(usuarios), "total_productos": len(productos), "total_ventas": len(ventas)},
        "analisis_clientes": analizar_clientes_modular(ventas),
    }


@app.post("/utilidades/ensuciar")
def endpoint_ensuciar(solicitud: SolicitudTransformacion):
    return {"resultado": ensuciar_datos(solicitud.registros)}


@app.post("/utilidades/limpiar")
def endpoint_limpiar(solicitud: SolicitudTransformacion):
    return {"resultado": limpiar_datos(solicitud.registros)}
