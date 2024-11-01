import json

# Diccionario de la base de datos del banco
base_de_datos_BANK_OF_NAO = {
    "usuarios": [

    ]
}

# Guardar el diccionario en formato JSON
def guardar_datos(datos):
    with open('datos.json', 'w') as f:
        json.dump(datos, f, indent=5)

# Cargar los datos desde el archivo JSON
def cargar_datos():
    with open('datos.json', 'r') as f:
        return json.load(f)

# Función para crear un nuevo usuario
def crear_usuario(datos):
    print("Creando un nuevo usuario...")
    nombre_completo = input("Ingrese el nombre completo: ")
    cedula = input("Ingrese la cédula: ")
    usuario_banco = input("Ingrese el nombre de usuario para el banco: ")
    clave_usuario_banco = int(input("Ingrese la clave de usuario: "))
    saldo_Bs = float(input("Ingrese el saldo inicial en Bs: "))
    tipo_de_cuenta = input("Ingrese el tipo de cuenta (ahorro/corriente): ").lower()

    # Crear el nuevo usuario
    nuevo_usuario = {
        "nombre_completo": nombre_completo,
        "cedula": cedula,
        "usuario_banco": usuario_banco,
        "clave_usuario_banco": clave_usuario_banco,
        "saldo_Bs": saldo_Bs,
        "tipo_de_cuenta": tipo_de_cuenta
    }

    # Agregar el nuevo usuario a la lista de usuarios
    datos['usuarios'].append(nuevo_usuario)
    
    # Guardar los datos actualizados
    guardar_datos(datos)

    print(f"Usuario {nombre_completo} creado exitosamente.")

# Funciones para realizar las operaciones bancarias
def estado_cuenta(usuario):
    return usuario['saldo_Bs']

def deposito(usuario, monto):
    usuario['saldo_Bs'] += monto
    return usuario['saldo_Bs']

def retiro(usuario, monto):
    if monto > usuario['saldo_Bs']:
        return "Fondos insuficientes"
    else:
        usuario['saldo_Bs'] -= monto
        return usuario['saldo_Bs']

def transferencia(usuario, monto, usuario_destino, datos):
    if monto > usuario['saldo_Bs']:
        return "Fondos insuficientes"
    else:
        usuario['saldo_Bs'] -= monto
        usuario_destino['saldo_Bs'] += monto
        # Guardar los datos actualizados en el archivo JSON
        guardar_datos(datos)
        return usuario['saldo_Bs'], usuario_destino['saldo_Bs']

# Menú de opciones
def menu():
    print("¿Qué operación desea realizar?")
    print("1. Estado de cuenta")
    print("2. Depósito")
    print("3. Retiro")
    print("4. Transferencia")
    print("5. Salir")
    return int(input("Ingrese una opción: "))

# Función para buscar usuario por credenciales (usuario_banco y clave_usuario_banco)
def buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, datos):
    for usuario in datos['usuarios']:
        if usuario['usuario_banco'] == usuario_banco and usuario['clave_usuario_banco'] == clave_usuario_banco:
            return usuario
    return None

# Nueva función: Buscar usuario por cédula
def buscar_usuario_por_cedula(cedula, datos):
    for usuario in datos['usuarios']:
        if usuario['cedula'] == cedula:
            return usuario
    return None

# Función principal
def main():
    datos = cargar_datos()  # Cargar los datos inicialmente

    while True:
        print("1. Iniciar sesión")
        print("2. Crear un nuevo usuario")
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:  # Iniciar sesión
            usuario_banco = input("Ingrese su nombre de usuario: ")
            clave_usuario_banco = int(input("Ingrese su clave de usuario: "))

            usuario_actual = buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco, datos)

            if usuario_actual:
                print(f"Bienvenido, {usuario_actual['nombre_completo']}")

                while True:
                    opcion = menu()

                    if opcion == 1:  # Estado de cuenta
                        print(f"Estado de cuenta: {estado_cuenta(usuario_actual)}")
                    elif opcion == 2:  # Depósito
                        monto = int(input("Ingrese el monto a depositar: "))
                        print(f"Nuevo saldo: {deposito(usuario_actual, monto)}")
                        guardar_datos(datos)  # Guardar los cambios después de la operación
                    elif opcion == 3:  # Retiro
                        monto = int(input("Ingrese el monto a retirar: "))
                        resultado = retiro(usuario_actual, monto)
                        print(resultado if isinstance(resultado, str) else f"Nuevo saldo: {resultado}")
                        guardar_datos(datos)  # Guardar los cambios después de la operación
                    elif opcion == 4:  # Transferencia
                        monto = int(input("Ingrese el monto a transferir: "))
                        cedula_destino = input("Ingrese la cédula del usuario de destino: ")

                        # Buscar el usuario de destino por cédula
                        usuario_destino = buscar_usuario_por_cedula(cedula_destino, datos)

                        if usuario_destino:
                            resultado = transferencia(usuario_actual, monto, usuario_destino, datos)
                            print(resultado if isinstance(resultado, str) else f"Transferencia exitosa. Nuevo saldo: {resultado[0]}")
                        else:
                            print("Usuario de destino no encontrado.")
                    elif opcion == 5:  # Salir
                        print("Gracias por usar el sistema bancario del BANK OF NAO.")
                        break
                    else:
                        print("Opción no válida, intenta nuevamente.")

                    # Preguntar si desea realizar otra operación
                    continuar = input("¿Quieres realizar otra operación en tu cuenta? (si/no): ").lower()
                    if continuar != "si":
                        break
            else:
                print("Usuario o clave incorrecta, intenta nuevamente.")
        elif opcion == 2:  # Crear un nuevo usuario
            crear_usuario(datos)  # Llamar a la función para crear un nuevo usuario
        else:
            print("Opción no válida, intenta nuevamente.")

        # Preguntar si desea realizar otra operación bancaria
        continuar = input("¿Quieres realizar otra operación bancaria? (si/no): ").lower()
        if continuar != "si":
            break

# Guardar los datos iniciales en el archivo
guardar_datos(base_de_datos_BANK_OF_NAO)

# Ejecutar el programa
main()
