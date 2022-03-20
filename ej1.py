# Crear una calculadora, donde se pase como argumentos luego de la opción -o el operador que se va a ejecutar (+,-,*,/), luego de -n el primer número de la operación, y de -m el segundo número.
# Ejemplo:
# python3 calc.py -o + -n 5 -m 6
# 5 + 6 = 11
# Considerar que el usuario puede ingresar los argumentos en cualquier orden. El programa deberá verificar que los argumentos sean válidos (no repetidos, números enteros, y operaciones válidas.

string = "-n 54666r6 5 -m 64444m3 -o + 4444 "

numeros = ["0","1","2", "3", "4", "5", "6", "7", "8", "9"]

lista = []

o = None
n = None
m = None

for x in string:
    lista.append(x)

indice = 0

operacion = None

for x in lista:

    if x == "-":

        if lista[indice + 1] == "n":

            es_numero = True

            numero = ""

            contador = 3

            while es_numero:

                if lista[indice + contador] in numeros:

                    numero = numero + lista[indice + contador]
            
                else:

                    es_numero = False

                contador = contador + 1

            n = numero
            
        elif lista[indice + 1] == "m":

            es_numero = True

            numero = ""

            contador = 3

            while es_numero:

                if lista[indice + contador] in numeros:

                    numero = numero + lista[indice + contador]
            
                else:

                    es_numero = False

                contador = contador + 1

            m = numero

        elif lista[indice + 1] == "o":

            o = lista[indice + 3]

            if lista[indice + 3] == "+":

                operacion = int(str(n)) + int(str(m))

            if lista[indice + 3] == "-":

                operacion = int(str(n)) - int(str(m))

            if lista[indice + 3] == "*":

                operacion = int(str(n)) * int(str(m))

            if lista[indice + 3] == "/":

                operacion = int(str(n)) / int(str(m))
            
    
    indice = indice + 1

print("\n {} {} {} = {}".format(n, o, m, operacion))
