# Escribir un programa que reciba dos nombres de archivos por línea de órdenes utilizando los parámetros “-i” y “-o” procesados con argparse.

# El programa debe verificar que el archivo pasado a “-i” exista en el disco. De ser así, lo abrirá en modo de solo lectura, leerá su contenido, y copiará dicho contenido en un archivo nuevo
# cuyo nombre será el pasado a “-o”. Si el archivo nuevo ya existe, deberá sobreescribirlo.

# Ejemplo:
# python3 copiar.py -i existente.txt -o nuevo.txt

import argparse
import sys
from ast import arg

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="Input file")      #Hay que hacer un add por cada opcion.
parser.add_argument("-o", type=str, help="Destination file")
args = parser.parse_args()

with open(args.i, 'r') as inputfile:
    mensaje = inputfile.read()
    with open(args.o, 'w') as output:
        output.write(mensaje)         #Si el archivo no existe, es creado.

# "archivo1.close()"" no es necesaria por la utilizacion del "with open...""

print("El archivo", args.i, "se copió a", args.o)