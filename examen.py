import json
import time

with open("dataBase.json", "r", encoding="utf-8") as archivo:
    data = json.load(archivo)

print("Sistema Medellin Recicla")
time.sleep(1)

# ---------------------------
# SELECCIONAR EMPRESA
# ---------------------------

empresas = list(data["empresas"].keys())

print("\nEmpresas disponibles:")
for i in range(len(empresas)):
    print(i + 1, "-", empresas[i])

while True:
    try:
        opcion_empresa = int(input("Seleccione empresa: "))
        if 1 <= opcion_empresa <= len(empresas):
            empresa_seleccionada = empresas[opcion_empresa - 1]
            break
        else:
            print("Opcion invalida")
    except:
        print("Ingrese un numero valido")

empresa = data["empresas"][empresa_seleccionada]

print("\nEmpresa seleccionada:", empresa_seleccionada)
time.sleep(1)

# ---------------------------
# LOGIN O REGISTRO
# ---------------------------

print("\n1 - Iniciar sesion")
print("2 - Registrarse")

opcion = input("Seleccione opcion: ")

usuario_logueado = None

if opcion == "1":

    intentos = 3

    while intentos > 0:
        correo = input("Correo: ")
        password = input("Password: ")

        for usuario in empresa["usuarios"]:
            if usuario["correo"] == correo and usuario["password"] == password:
                usuario_logueado = usuario
                break

        if usuario_logueado:
            break
        else:
            intentos -= 1
            print("Credenciales incorrectas")
            print("Intentos restantes:", intentos)

    if not usuario_logueado:
        print("Acceso denegado")
        exit()

elif opcion == "2":

    nombre = input("Nombre: ")
    correo = input("Correo: ")
    password = input("Password: ")

    dominio_empresa = empresa_seleccionada.lower().replace(" ", "")

    if dominio_empresa not in correo.lower():
        print("El correo debe pertenecer a la empresa seleccionada")
        exit()

    for usuario in empresa["usuarios"]:
        if usuario["correo"] == correo:
            print("El correo ya esta registrado")
            exit()

    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "password": password,
        "rol": "Gestor"
    }

    empresa["usuarios"].append(nuevo_usuario)

    with open("dataBase.json", "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4)

    print("Usuario registrado correctamente")
    time.sleep(1)
    usuario_logueado = nuevo_usuario

else:
    print("Opcion invalida")
    exit()

print("\nBienvenido", usuario_logueado["nombre"])
time.sleep(1)

# ---------------------------
# REGISTRO DE MEDICIONES
# ---------------------------

print("\nRegistro de recolecciones para", empresa_seleccionada)
time.sleep(1)

CANTIDAD_MEDICIONES = 20

for material in empresa["recolecciones"]:
    print("\nMaterial:", material)
    print("Se solicitaran", CANTIDAD_MEDICIONES, "registros para este material")

    contador = 0

    while contador < CANTIDAD_MEDICIONES:
        try:
            kg = float(input("Ingrese kg: "))
            if kg >= 0:
                empresa["recolecciones"][material].append(kg)
                contador += 1
                faltan = CANTIDAD_MEDICIONES - contador
                print("Registros faltantes:", faltan)
            else:
                print("No puede ser negativo")
        except:
            print("Ingrese un numero valido")

with open("dataBase.json", "w", encoding="utf-8") as archivo:
    json.dump(data, archivo, indent=4)

print("\nGenerando reporte...")
time.sleep(2)

# ---------------------------
# REPORTE
# ---------------------------

promedios = []

for material in empresa["recolecciones"]:
    lista = empresa["recolecciones"][material]

    if len(lista) > 0:
        promedio = sum(lista) / len(lista)
    else:
        promedio = 0

    promedios.append(promedio)

    if promedio < 8:
        estado = "Bajo"
    elif promedio <= 15:
        estado = "Estable"
    else:
        estado = "Alto"

    print("\nMaterial:", material)
    print("Promedio:", round(promedio, 2))
    print("Estado:", estado)

if len(promedios) > 0:
    promedio_global = sum(promedios) / len(promedios)
else:
    promedio_global = 0

if promedio_global < 10:
    estado_global = "Alerta"
elif promedio_global < 15:
    estado_global = "Operacion normal"
else:
    estado_global = "Jornada sobresaliente"

print("\nResumen global")
print("Promedio global:", round(promedio_global, 2))
print("Estado global:", estado_global)