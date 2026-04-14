# API de analisis para ecommerce



La API esta pensada como una capa intermedia entre backend y frontend. Su trabajo es:

- consultar usuarios, productos y ventas
- limpiar y normalizar los datos si hace falta
- calcular resumenes y rankings
- devolver una respuesta simple, estable y lista para frontend

## Objetivo general

Esta API busca responder preguntas basicas del negocio sin que el frontend tenga que hacer calculos:

- cuantos usuarios existen
- cuantos productos existen
- cuanto se ha vendido
- cuanto se vende por venta en promedio
- que productos se venden mas y menos
- que clientes compran mas y menos
- que empleados venden mas y menos

Si el backend todavia no expone ventas reales, la API igual debe comportarse bien:

- no se debe caer
- no debe inventar ventas
- debe informar claramente cuando faltan datos
- puede aceptar ventas manuales o usar datos de ejemplo para pruebas

## Requisitos

- Python `3.12` o compatible
- backend base disponible en `http://localhost:8080` o en la URL que configures

## Instalacion y arranque

### 1. Entrar al proyecto

Ubicate en la carpeta del proyecto:

```powershell
cd "C:\Users\aprendizpeoplea1\OneDrive - GCO\Escritorio\workspace\final_uribe_26_analitica"
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

Dependencias usadas:

- `fastapi`
- `uvicorn`
- `requests`
- `pydantic`

### 3. Iniciar la API

```powershell
uvicorn main:app --reload
```

Si arranca bien, `uvicorn` mostrara algo parecido a esto:

```text
Uvicorn running on http://127.0.0.1:8000
```

## Variables de entorno

Si el backend corre en otra ruta, puedes cambiarlo asi:

```powershell
$env:URL_BACKEND="http://localhost:8080"
```

Tiempo maximo de espera al backend:

```powershell
$env:TIMEOUT_BACKEND="10"
```

Luego arrancas `uvicorn` normalmente.

## Como saber si la API esta escuchando

### Opcion 1. Abrir la documentacion

Cuando la API este arriba, abre:

```text
http://127.0.0.1:8000/docs
```

Si esa pagina carga, la API esta escuchando.

### Opcion 2. Probar el endpoint de salud

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/salud"
```

Respuesta esperada:

```json
{
  "estado": "ok"
}
```

### Opcion 3. Probar el endpoint raiz

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/"
```

Respuesta esperada:

```json
{
  "mensaje": "API de analisis lista para ecommerce universitario.",
  "backend_configurado": "http://localhost:8080",
  "documentacion": "/docs"
}
```

## Como saber si esta funcionando de verdad

Que la API responda no significa automaticamente que ya tenga datos reales. Hay tres niveles para revisarla:

### 1. La API de analisis esta viva

Se valida con `GET /salud`.

### 2. La API de analisis esta procesando solicitudes

Se valida llamando un endpoint como `POST /analisis/completo`.

Ejemplo:

```powershell
$body = @{
  filtros_usuarios = @{
    nombres = ""
    apellidos = ""
    correo = ""
  }
  filtros_productos = @{
    nombre = ""
    minPrecio = 0
    maxPrecio = 0
    categorias = @()
    descuento = 0
    color = ""
  }
  ventas = @()
  usar_datos_ejemplo = $false
  ensuciar_resultado = $false
  limpiar_datos = $true
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/analisis/completo" -ContentType "application/json" -Body $body
```

### 3. La API esta logrando consumir informacion util del backend

Esto se valida revisando el campo `mensajes` de la respuesta:

- si dice `Las ventas se tomaron desde ...`, logro consumir ventas reales desde una ruta candidata
- si dice `No se encontraron ventas en el backend...`, la API esta bien pero el backend aun no entrega ventas listables
- si usas `usar_datos_ejemplo = true`, dira que uso ventas de ejemplo

Mientras no existan datos reales, es normal que la respuesta venga vacia. Eso no es error. El error seria que:

- se cayera la API
- devolviera 500
- inventara ventas donde no existen

## Endpoints del backend que consume esta API

La API usa como base la coleccion `Back.endpoints_proyecto`.

Rutas usadas para usuarios y productos:

- `GET /usuarios/listar`
- `GET /productos/buscar`

Rutas candidatas para intentar encontrar ventas:

- `GET /ordenes/listar`
- `GET /ordenes/buscar`
- `GET /ventas/listar`
- `GET /ventas/buscar`

### Nota importante sobre ventas

En la coleccion original no aparece una ruta clara y definitiva para listar ventas ya preparadas para analitica. Por eso la API:

1. primero intenta consumir ventas desde esas rutas candidatas
2. si no encuentra ventas, acepta ventas manuales en el body
3. si se activa `usar_datos_ejemplo`, usa ventas de prueba

## Endpoints disponibles en esta API

### `GET /`

Devuelve informacion general del proyecto.

### `GET /salud`

Devuelve el estado rapido del servicio.

Uso:

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/salud"
```

### `POST /analisis/completo`

Devuelve:

- fuente del backend
- mensajes de contexto
- resumen general
- ranking de empleados
- ranking de productos
- ranking de clientes

### `POST /analisis/resumen`

Devuelve solo:

- fuente del backend
- mensajes
- resumen general

### `POST /analisis/empleados`

Devuelve:

- fuente del backend
- mensajes
- resumen basico
- `analisis_empleados`

### `POST /analisis/productos`

Devuelve:

- fuente del backend
- mensajes
- resumen basico
- `analisis_productos`

### `POST /analisis/clientes`

Devuelve:

- fuente del backend
- mensajes
- resumen basico
- `analisis_clientes`

### `POST /utilidades/ensuciar`

Recibe una lista de registros y devuelve una version ensuciada para pruebas.

### `POST /utilidades/limpiar`

Recibe una lista de registros y devuelve una version limpiada.

## Cuerpo base para los endpoints de analisis

Todos los endpoints `POST /analisis/...` reciben este formato:

```json
{
  "filtros_usuarios": {
    "nombres": "",
    "apellidos": "",
    "correo": ""
  },
  "filtros_productos": {
    "nombre": "",
    "minPrecio": 0,
    "maxPrecio": 0,
    "categorias": [],
    "descuento": 0,
    "color": ""
  },
  "ventas": [],
  "usar_datos_ejemplo": false,
  "ensuciar_resultado": false,
  "limpiar_datos": true
}
```

### Que significa cada campo

- `filtros_usuarios`: filtros que se envian al backend para listar usuarios
- `filtros_productos`: filtros que se envian al backend para buscar productos
- `ventas`: ventas manuales enviadas directamente a la API
- `usar_datos_ejemplo`: si es `true`, usa ventas de ejemplo cuando el backend no trae ventas
- `ensuciar_resultado`: si es `true`, altera la respuesta para probar escenarios de datos malos
- `limpiar_datos`: si es `true`, limpia texto y numeros antes del analisis

## Ejemplos de uso

### Ejemplo 1. Analisis completo con datos de ejemplo

```json
POST /analisis/completo
{
  "filtros_usuarios": {
    "nombres": "",
    "apellidos": "",
    "correo": ""
  },
  "filtros_productos": {
    "nombre": "",
    "minPrecio": 0,
    "maxPrecio": 0,
    "categorias": [],
    "descuento": 0,
    "color": ""
  },
  "ventas": [],
  "usar_datos_ejemplo": true,
  "ensuciar_resultado": false,
  "limpiar_datos": true
}
```

### Ejemplo 2. Analisis completo con ventas manuales

```json
POST /analisis/completo
{
  "filtros_usuarios": {
    "nombres": "",
    "apellidos": "",
    "correo": ""
  },
  "filtros_productos": {
    "nombre": "",
    "minPrecio": 0,
    "maxPrecio": 0,
    "categorias": [],
    "descuento": 0,
    "color": ""
  },
  "ventas": [
    {
      "id": "v-1",
      "empleado_nombre": "Laura Gomez",
      "cliente_nombre": "Carlos Ruiz",
      "total": 120000,
      "estado": "PAGADA",
      "fecha": "2026-04-10",
      "productos": [
        {
          "producto_nombre": "Camisa oversize",
          "cantidad": 2,
          "precio_unitario": 60000
        }
      ]
    }
  ],
  "usar_datos_ejemplo": false,
  "ensuciar_resultado": false,
  "limpiar_datos": true
}
```

## Como interpretar la respuesta

Una respuesta de `POST /analisis/completo` trae normalmente estas llaves:

- `fuente_backend`
- `mensajes`
- `resumen`
- `empleados_que_mas_venden`
- `empleados_que_menos_venden`
- `productos_mas_vendidos`
- `productos_menos_vendidos`
- `clientes_que_mas_compran`
- `clientes_que_menos_compran`

### Respuesta correcta sin ventas reales

Si aun no hay ventas, la API puede responder algo como esto:

```json
{
  "fuente_backend": "http://localhost:8080",
  "mensajes": [
    "No se encontraron ventas en el backend. Puedes enviar ventas en el body o activar usar_datos_ejemplo.",
    "Los datos fueron limpiados antes del analisis."
  ],
  "resumen": {
    "total_usuarios": 0,
    "total_productos": 0,
    "total_ventas": 0,
    "total_ingresos": 0,
    "total_unidades_vendidas": 0,
    "promedio_por_venta": 0,
    "usuarios_por_rol": {}
  },
  "empleados_que_mas_venden": [],
  "empleados_que_menos_venden": [],
  "productos_mas_vendidos": [],
  "productos_menos_vendidos": [],
  "clientes_que_mas_compran": [],
  "clientes_que_menos_compran": []
}
```

Eso significa que la API se comporto bien aunque todavia no tenga materia prima para analizar.

## Estructura del proyecto

- `main.py`: entrada principal de la API y definicion de endpoints
- `analisis/analisis_resumen.py`: calculo del resumen general
- `analisis/analisis_empleados.py`: ranking de empleados
- `analisis/analisis_productos.py`: ranking de productos
- `analisis/analisis_clientes.py`: ranking de clientes
- `analisis/analisis_general.py`: une todos los analisis en una sola respuesta
- `servicios/backend_cliente.py`: consumo del backend y busqueda de rutas de ventas
- `servicios/preparador_datos.py`: orquesta lectura, limpieza, normalizacion y mensajes
- `servicios/normalizador_datos.py`: adapta usuarios, productos y ventas a un formato comun
- `servicios/limpiador_datos.py`: limpia texto y numeros
- `servicios/ensuciador_datos.py`: genera datos ruidosos para pruebas
- `servicios/ventas_ejemplo.py`: ventas base para demostracion
- `Back.endpoints_proyecto`: coleccion de referencia del backend
- `tests/test_robustez_api.py`: pruebas basicas de robustez

## Funciones importantes y como trabajan

### `construir_respuesta_analitica`

Ubicacion: `main.py`

Hace esto:

1. llama a `preparar_datos_para_analisis_modular`
2. llama a `armar_respuesta_completa_modular`
3. si se pide, ensucia el resultado para pruebas

Es la puerta principal del analisis.

### `preparar_datos_para_analisis_modular`

Ubicacion: `servicios/preparador_datos.py`

Hace esto:

1. consulta usuarios al backend
2. consulta productos al backend
3. toma ventas manuales si llegaron en el body
4. si no llegaron ventas manuales, intenta encontrarlas en rutas candidatas
5. si no encuentra ventas y `usar_datos_ejemplo` esta activo, usa ventas de ejemplo
6. agrega mensajes para explicar de donde salieron los datos
7. limpia datos si `limpiar_datos` esta activo
8. normaliza todo a una forma comun

Es la funcion mas importante de preparacion.

### `consumir_endpoint_get`

Ubicacion: `servicios/backend_cliente.py`

Metodo usado:

- `GET`

Hace una llamada al backend con `requests.get(...)`.

Si el backend falla o responde mal:

- lanza `HTTPException 502`

### `intentar_consumir_ventas`

Ubicacion: `servicios/backend_cliente.py`

Metodo usado:

- `GET`

Prueba varias rutas hasta encontrar una que realmente entregue una lista de ventas.

Comportamiento actual:

- si una ruta devuelve una lista valida, la usa
- si una ruta devuelve un objeto suelto sin lista, no inventa ventas
- si ninguna sirve, devuelve lista vacia

### `extraer_lista_principal`

Ubicacion: `servicios/normalizador_datos.py`

Sirve para volver mas tolerante el consumo del backend.

Acepta respuestas como:

- una lista directa
- un objeto con `data`
- un objeto con `datos`
- un objeto con `result`
- un objeto con `resultado`
- un objeto con `content`
- un objeto con `items`

Si no encuentra una lista real, devuelve vacio. Eso evita analitica falsa.

### `convertir_a_float`

Ubicacion: `servicios/normalizador_datos.py`

Convierte valores numericos sin romper la API.

Ejemplos:

- si llega `100`, devuelve `100.0`
- si llega `"100"`, devuelve `100.0`
- si llega `"abc"`, devuelve `0`

### `normalizar_usuarios`

Ubicacion: `servicios/normalizador_datos.py`

Toma distintas posibles llaves del backend y las convierte a una estructura comun:

- `id`
- `nombre`
- `correo`
- `rol`

### `normalizar_productos`

Ubicacion: `servicios/normalizador_datos.py`

Convierte productos del backend a una forma unica:

- `id`
- `nombre`
- `precio`
- `categorias`
- `stock_total`

Tambien suma cantidades de stock y tolera numeros invalidos.

### `normalizar_ventas`

Ubicacion: `servicios/normalizador_datos.py`

Convierte ventas a una estructura comun:

- `id`
- `empleado_id`
- `empleado_nombre`
- `cliente_id`
- `cliente_nombre`
- `total`
- `estado`
- `fecha`
- `productos`

Tambien calcula subtotales por producto y evita errores si faltan numeros o vienen sucios.

### `analizar_resumen`

Ubicacion: `analisis/analisis_resumen.py`

Calcula:

- total de usuarios
- total de productos
- total de ventas
- total de ingresos
- total de unidades vendidas
- promedio por venta
- usuarios por rol

### `analizar_empleados_modular`

Ubicacion: `analisis/analisis_empleados.py`

Calcula:

- empleados que mas venden
- empleados que menos venden
- ventas realizadas
- unidades vendidas
- ingresos generados

### `analizar_productos_modular`

Ubicacion: `analisis/analisis_productos.py`

Calcula:

- productos mas vendidos
- productos menos vendidos
- unidades vendidas
- ingresos generados
- veces vendido

### `analizar_clientes_modular`

Ubicacion: `analisis/analisis_clientes.py`

Calcula:

- clientes que mas compran
- clientes que menos compran
- compras realizadas
- monto total comprado

### `armar_respuesta_completa_modular`

Ubicacion: `analisis/analisis_general.py`

Une en un solo objeto:

- fuente backend
- mensajes
- resumen
- analisis de empleados
- analisis de productos
- analisis de clientes

## Robustez y controles ya implementados

La API ya queda preparada para escenarios reales en los que el backend empiece a poblarse poco a poco:

- si no hay ventas, responde vacio con mensajes claros
- si el backend devuelve un objeto sin lista, no lo interpreta como venta real
- si el backend devuelve ventas dentro de `data` o llaves parecidas, las extrae
- si llegan numeros malos, no se cae la API
- si no se puede consumir una ruta, intenta con otra

## Pruebas

Se dejaron pruebas basicas de robustez en `tests/test_robustez_api.py`.

Para ejecutarlas:

```powershell
python -m unittest discover -s tests -v
```

Que validan:

- lectura de ventas desde respuestas envueltas
- no inventar ventas cuando la respuesta no trae lista valida
- no caerse con datos numericos invalidos

## Archivo de referencia del backend

La coleccion original del backend esta en `Back.endpoints_proyecto`.

Sirve para entender:

- que rutas existen en el backend
- que parametros se esperan
- que cuerpos de ejemplo habia en Postman

## Resumen final

Para usar este proyecto de forma basica:

1. instalar dependencias con `pip install -r requirements.txt`
2. iniciar la API con `uvicorn main:app --reload`
3. comprobar `GET /salud`
4. abrir `http://127.0.0.1:8000/docs`
5. probar `POST /analisis/completo`
6. revisar el campo `mensajes` para saber si la API encontro ventas reales, uso ejemplo o no encontro informacion

Con eso el proyecto queda listo para empezar a recibir informacion real del backend sin caerse ni devolver analitica enganosa.
