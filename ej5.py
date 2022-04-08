# Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:

# -n <N>
# -r <R>
# -h
# -f <ruta_archivo>
# -v

# El programa deberá abrir (crear si no existe) un archivo de texto cuyo path ha sido pasado por argumento con -f.
# El programa debe generar <N> procesos hijos. Cada proceso estará asociado a una letra del alfabeto (el primer proceso con la "A", el segundo con la "B", etc). 
# Cada proceso almacenará en el archivo su letra <R> veces con un delay de un segundo entre escritura y escritura (realizar flush() luego de cada escritura).
# El proceso padre debe esperar a que los hijos terminen, luego de lo cual deberá leer el contenido del archivo y mostrarlo por pantalla.
# La opción -h mostrará ayuda. La opción -v activará el modo verboso, en el que se mostrará antes de escribir cada letra en el archivo: Proceso <PID> escribiendo letra 'X'.


#Ejemplo 1:

# ./escritores.py -n 3 -r 4 -f /tmp/letras.txt
# ABCACBABCBAC

# Ejemplo 2:

# ./escritores.py -n 3 -r 5 -f /tmp/letras.txt -v
# Proceso 401707 escribiendo letra 'A'
# Proceso 401708 escribiendo letra 'B'
# Proceso 401709 escribiendo letra 'C'
# Proceso 401708 escribiendo letra 'B'
# Proceso 401707 escribiendo letra 'A'
# Proceso 401709 escribiendo letra 'C'
# Proceso 401707 escribiendo letra 'A'
# Proceso 401708 escribiendo letra 'B'
# Proceso 401709 escribiendo letra 'C'
# Proceso 401707 escribiendo letra 'A'
# Proceso 401708 escribiendo letra 'B'
# Proceso 401709 escribiendo letra 'C'
# Proceso 401707 escribiendo letra 'A'
# Proceso 401708 escribiendo letra 'B'
# Proceso 401709 escribiendo letra 'C'
# ABCBACABCABCABC

import argparse
from subprocess import Popen
import os

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="el programa generará n procesos hijos.", required=True)
    parser.add_argument("-r", type=int, help= "cada proceso almacenará en el archivo su letra r veces", required=True)
    parser.add_argument("-f", type=str, help= "path del archivo de texto", required=True)
    parser.add_argument("-v", help="ponga -v para activar el modo verboso", action='store_true', default=False)
    args = parser.parse_args()

if __name__=="__main__":
    main()