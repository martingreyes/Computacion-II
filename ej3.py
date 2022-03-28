# Escribir un programa que reciba por argumentos de línea de comandos los siguientes modificadores:
# -c command
# -o output_file
# -l log_file

# El código deberá crear los archivos pasados por los argumentos -o y -l en el caso de que no existan.
# El código deberá ejecutar el comando haciendo uso de subprocess.Popen, y almacenar su salida en el archivo pasado en el parámetro -f. 
# En el archivo pasado por el modificador -l deberá almacenar el mensaje “fechayhora: Comando XXXX ejecutado correctamente” o en su defecto el mensaje de error generado por el comando si este falla.

# Por ejemplo:
# python ejecutor.py -c “ip a” -o /tmp/salida -l /tmp/log

# El archivo /tmp/salida deberá contener la salida del comando, y /tmp/log deberá contener:

# fechayhora: Comando “ip a” ejecutado correctamente.

# Otro ejemplo:

# python ejecutor.py -c “ls /cualquiera” -o /tmp/salida -l /tmp/log

# El archivo /tmp/salida no contendrá nada nuevo, ya que el comando fallará. El archivo /tmp/log contendrá:
# fechayhora: ls: cannot access '/cualquiera': No such file or directory

import argparse
import sys
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str, help="command")          #Hay que hacer un add por cada opcion.
parser.add_argument("-o", type=str, help="output file")
parser.add_argument("-i", type=str, help="log file")
args = parser.parse_args()

output_file = args.o

log_file = args.i

comando = args.c

log = open("/Users/martinreyes/Documents/Facultad/3ro/Computacion_II//Computacion-II/log.txt", "w+")    # 'w':  Opens a file for writing. Creates a new file if it does not exist or truncates the file if it exists.

out = open("/Users/martinreyes/Documents/Facultad/3ro/Computacion_II//Computacion-II/out.txt", "a+")    # 'a':  Opens a file for appending at the end of the file without truncating it. Creates a new file if it does not exist.
                                                                            
        

x = subprocess.Popen(comando.split(),stdout=out,stderr=log)










