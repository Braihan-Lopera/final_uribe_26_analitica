from servicios.simulador_inventario import generar_inventario_sucio
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from analisis.analisis_clientes import analizar_clientes_modular
from analisis.analisis_general import armar_respuesta_completa_modular
from analisis.analisis_empleados import analizar_empleados_modular
from analisis.analisis_productos import analizar_productos_modular
from analisis.analisis_resumen import analizar_resumen
from servicios.ensuciador_datos import ensuciar_datos
from servicios.limpiador_datos import limpiar_datos
from servicios.backend_cliente import URL_BACKEND
from servicios.preparador_datos import preparar_datos_para_analisis_modular
from servicios.exportador_datos import generar_excel_reporte

app = FastAPI(
    title="API de analisis para ecommerce",
    version="1.2.0",
    description="API avanzada para analisis con Pandas y exportacion a Excel.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class FiltroVendedores(BaseModel):
    nombre: str = ""
    id: str = ""

class SolicitudAnalisis(BaseModel):
    filtros_usuarios: FiltroUsuarios = Field(default_factory=FiltroUsuarios)
    filtros_productos: FiltroProductos = Field(default_factory=FiltroProductos)
    filtros_vendedores: FiltroVendedores = Field(default_factory=FiltroVendedores)
    ventas: list = Field(default_factory=list)
    usar_datos_ejemplo: bool = False
    ensuciar_resultado: bool = False
    limpiar_datos: bool = True

class SolicitudTransformacion(BaseModel):
    registros: list = Field(default_factory=list)

def construir_respuesta_analitica(solicitud):
    usuarios, productos, ventas, mensajes = preparar_datos_para_analisis_modular(solicitud)
    
    # Aplicar filtro de vendedores si existe
    if solicitud.filtros_vendedores.nombre:
        nombre_f = solicitud.filtros_vendedores.nombre.lower()
        ventas = [v for v in ventas if nombre_f in v.get('empleado_nombre', '').lower()]
        mensajes.append(f"Filtrado por vendedor: {solicitud.filtros_vendedores.nombre}")

    respuesta = armar_respuesta_completa_modular(usuarios, productos, ventas, mensajes, URL_BACKEND)
    if solicitud.ensuciar_resultado:
        respuesta = ensuciar_datos(respuesta)
    return respuesta

@app.get("/")
def inicio():
    return {
        "mensaje": "API de analisis lista con soporte de Pandas.",
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
def analisis_resumen_endpoint(solicitud: SolicitudAnalisis):
    return construir_respuesta_analitica(solicitud) # Usamos el general para consistencia

@app.post("/analisis/empleados")
def analisis_empleados_endpoint(solicitud: SolicitudAnalisis):
    return construir_respuesta_analitica(solicitud)

@app.post("/analisis/productos")
def analisis_productos_endpoint(solicitud: SolicitudAnalisis):
    return construir_respuesta_analitica(solicitud)

@app.post("/analisis/clientes")
def analisis_clientes_endpoint(solicitud: SolicitudAnalisis):
    return construir_respuesta_analitica(solicitud)

@app.post("/analisis/exportar/excel")
def exportar_excel(solicitud: SolicitudAnalisis):
    datos = construir_respuesta_analitica(solicitud)
    excel_content = generar_excel_reporte(datos)
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reporte_analitico.xlsx"}
    )

@app.post("/utilidades/ensuciar")
def endpoint_ensuciar(solicitud: SolicitudTransformacion):
    return {"resultado": ensuciar_datos(solicitud.registros)}

@app.post("/utilidades/limpiar")
def endpoint_limpiar(solicitud: SolicitudTransformacion):
    return {"resultado": limpiar_datos(solicitud.registros)}

@app.get("/utilidades/simular-inventario-sucio")
def endpoint_simular_inventario():
    return {"resultado": generar_inventario_sucio(24)}
