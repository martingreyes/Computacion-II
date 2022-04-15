# Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
# El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
# El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
# Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
# El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.

# Ejemplo:
# Contenido del archivo /tmp/texto.txt
# Hola Mundo
# que tal
# este es un archivo
# de ejemplo.

# Ejecución:
# python3 inversor.py -f /tmp/texto.txt
# ovihcra nu se etse
# .olpmeje ed
# lat euq
# odnuM aloH

import argparse
import subprocess
import os
import string
import time

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help= "path del archivo de texto", required=True)
    args = parser.parse_args()

    archivo = open(args.f, "r")

    numero = sum(1 for line in archivo)

    padre = os.getpid()

    for x in range(numero):
      
        os.fork()

        if os.getpid() != padre:      # Lo que esta dentro de este if solamente lo hacen los hijos


            os._exit(0) 

    
    for i in range(args.n):
        os.wait()                     # padre espera a hijos (?) 

if __name__=="__main__":
    main()

# Correr con p ej6.py -f /Users/martinreyes/Downloads/texto.txt
