import json

# Diccionario de la base de datos del banco
base_de_datos_BANK_OF_NAO = {
    "usuarios": [
        {
            "nombre_completo": "Jenny Remolina",
            "cedula": "30.000.000",
            "usuario_banco": "jennyr",
            "clave_usuario_banco": 123,
            "saldo_Bs": 50000,
            "tipo_de_cuenta": "ahorro"
        },
        {
            "nombre_completo": "Anderson Perdomo",
            "cedula": "30.170.300",
            "usuario_banco": "andper",
            "clave_usuario_banco": 456,
            "saldo_Bs": 10000,
            "tipo_de_cuenta": "corriente"
        }
    ]
}

# Guardar el diccionario en formato JSON
with open('datos.json', 'w') as f:
    json.dump(base_de_datos_BANK_OF_NAO, f, indent=5)

# Función para cargar los datos del archivo JSON
def cargar_datos():
    with open('datos.json', 'r') as f:
        return json.load(f)

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

def transferencia(usuario, monto, usuario_destino):
    if monto > usuario['saldo_Bs']:
        return "Fondos insuficientes"
    else:
        usuario['saldo_Bs'] -= monto
        usuario_destino['saldo_Bs'] += monto
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
def buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['usuario_banco'] == usuario_banco and usuario['clave_usuario_banco'] == clave_usuario_banco:
            return usuario
    return None

# Nueva función: Buscar usuario por cédula
def buscar_usuario_por_cedula(cedula):
    datos = cargar_datos()
    for usuario in datos['usuarios']:
        if usuario['cedula'] == cedula:
            return usuario
    return None

# Función principal
def main():
    while True:
        usuario_banco = input("Ingrese su nombre de usuario: ")
        clave_usuario_banco = int(input("Ingrese su clave de usuario: "))

        usuario_actual = buscar_usuario_por_credenciales(usuario_banco, clave_usuario_banco)

        if usuario_actual:
            print(f"Bienvenido, {usuario_actual['nombre_completo']}")

            while True:
                opcion = menu()

                if opcion == 1:  # Estado de cuenta
                    print(f"Estado de cuenta: {estado_cuenta(usuario_actual)}")
                elif opcion == 2:  # Depósito
                    monto = int(input("Ingrese el monto a depositar: "))
                    print(f"Nuevo saldo: {deposito(usuario_actual, monto)}")
                elif opcion == 3:  # Retiro
                    monto = int(input("Ingrese el monto a retirar: "))
                    resultado = retiro(usuario_actual, monto)
                    print(resultado if isinstance(resultado, str) else f"Nuevo saldo: {resultado}")
                elif opcion == 4:  # Transferencia
                    monto = int(input("Ingrese el monto a transferir: "))
                    cedula_destino = input("Ingrese la cédula del usuario de destino: ")

                    # Buscar el usuario de destino por cédula
                    usuario_destino = buscar_usuario_por_cedula(cedula_destino)

                    if usuario_destino:
                        resultado = transferencia(usuario_actual, monto, usuario_destino)
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

        # Preguntar si desea realizar otra operación bancaria
        continuar = input("¿Quieres realizar otra operación bancaria? (si/no): ").lower()
        if continuar != "si":
            break

# Ejecutar el programa
main()
