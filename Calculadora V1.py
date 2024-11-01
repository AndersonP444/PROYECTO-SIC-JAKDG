def calculator():
    while True:
        num1 = float(input("Introduzca la primera cifra: "))
        operator = input("Introduzca el operador (+, -, *, /): ")
        num2 = float(input("Introduzca la segunda cifra: "))
        if operator == '+':
            resultado = num1 + num2
        elif operator == '-':
            resultado = num1 - num2
        elif operator == '*':
            resultado = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error")
            else:
                resultado = num1 / num2
        else:
            print("operacion invalida")
            continue

        print("Resultado:", resultado)

        continue_choice = input("¿Quieres realizar otra operación? (si/no): ")
        if continue_choice.lower() != 'si':
            break

calculator() 