from fastapi import FastAPI, Response, File, UploadFile
import pandas as pd
import io
import requests
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from servicios.simulador_inventario import generar_inventario_sucio
from analisis.analisis_clientes import analizar_clientes_modular
from analisis.analisis_general import armar_respuesta_completa_modular
from analisis.analisis_empleados import analizar_empleados_modular
from analisis.analisis_productos import analizar_productos_modular
from analisis.analisis_resumen import analizar_resumen
from servicios.ensuciador_datos import ensuciar_datos
from servicios.limpiador_datos import limpiar_datos, limpiar_datos_dataframe
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
    respuesta = construir_respuesta_analitica(solicitud)
    return {
        "fuente_backend": respuesta["fuente_backend"],
        "mensajes": respuesta["mensajes"],
        "resumen": respuesta["resumen"],
    }

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

@app.get("/utilidades/prendas-reales-sucias")
def endpoint_prendas_reales_sucias():
    try:
        # 1. Traer productos reales del backend
        res = requests.get(f"{URL_BACKEND}/productos/buscar", timeout=5)
        productos = extraer_lista_principal(res.json())
        
        if not productos:
            return {"resultado": generar_inventario_sucio(10)} # Fallback si está vacío
            
        # 2. "Ensuciarlos" para la vista de normalización
        resultado = []
        import random
        for p in productos:
            # Inyectamos casos extremos: espacios, textos largos, términos coloquiales
            resultado.append({
                "id": p.get("id"),
                "nombre": f"   {p.get('nombre', '').lower()}   ",
                "precio": f"  {p.get('precio')}  COP  ",
                "talla": random.choice(["  GRANDOTE  ", "súper   grande", "  pequeñito  ", "  X  L  ", "chiquito"]),
                "categoria": "  General  "
            })
        return {"resultado": resultado}
    except Exception:
        return {"resultado": generar_inventario_sucio(10)}

@app.post("/utilidades/subir-catalogo")
async def subir_catalogo(archivo: UploadFile = File(...)):
    try:
        # 1. Leer Excel
        contenido = await archivo.read()
        df = pd.read_excel(io.BytesIO(contenido))
        
        # 2. Limpiar con Pandas (reutilizando lógica existente)
        # Convertimos NaN a valores vacíos para evitar errores de JSON
        df = df.fillna("")
        registros_crudos = df.to_dict(orient='records')
        
        # Limpieza profunda de texto
        df_limpio = limpiar_datos_dataframe(registros_crudos)
        registros = df_limpio.to_dict(orient='records')
        
        resultados = []
        
        # 3. Enviar al Backend Java
        import random
        for reg in registros:
            # Extracción robusta de números (precio y cantidad)
            def extraer_numero(v):
                if isinstance(v, (int, float)): return int(v)
                import re
                nums = re.sub(r'[^0-9]', '', str(v))
                return int(nums) if nums else 0

            # Añadimos un sufijo aleatorio para evitar el error 400 por nombre duplicado (Unique Constraint en DB)
            nombre_unico = f"{str(reg.get('nombre', 'Sin Nombre'))} #{random.randint(100, 999)}"

            payload = {
                "nombre": nombre_unico,
                "precio": extraer_numero(reg.get("precio", 0)),
                "categorias": [str(reg.get("categoria", "General"))],
                "stock": [
                    {
                        "talla": str(reg.get("talla", "M")),
                        "cantidad": extraer_numero(reg.get("cantidad", 0)),
                        "color": str(reg.get("color", "N/A"))
                    }
                ]
            }
            
            try:
                res_back = requests.post(f"{URL_BACKEND}/productos/guardar", json=payload, timeout=5)
                if res_back.status_code == 200:
                    resultados.append({"nombre": payload["nombre"], "estado": "Guardado"})
                else:
                    # Capturamos el mensaje de error del backend para que el usuario sepa qué falló
                    error_msg = res_back.text[:50] # Limitamos el tamaño por estética
                    resultados.append({"nombre": payload["nombre"], "estado": f"Error: {error_msg}"})
            except Exception as e:
                resultados.append({"nombre": payload["nombre"], "estado": f"No hay conexión con Backend"})
                
        return {"mensaje": "Procesamiento completado", "detalles": resultados}
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response(content=f"Error al procesar Excel: {str(e)}", status_code=400)
