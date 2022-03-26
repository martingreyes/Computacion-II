# Crear una calculadora, donde se pase como argumentos luego de la opción -o el operador que se va a ejecutar (+,-,*,/), luego de -n el primer número de la operación, y de -m el segundo número.
# Ejemplo:
# python3 calc.py -o + -n 5 -m 6
# 5 + 6 = 11
# Considerar que el usuario puede ingresar los argumentos en cualquier orden. El programa deberá verificar que los argumentos sean válidos (no repetidos, números enteros, y operaciones válidas.

import getopt
import sys



(opt,arg)=getopt.getopt(sys.argv[1:],'o:n:m:')

for o, a in opt:
    if o == "-o":
        op = a
    elif o == "-n":
       primer = int(a)
    elif o == "-m":
        segundo = int(a)
    else:
        print("Error")

print(eval(str(primer) + op + str(segundo)))



