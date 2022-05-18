"""
Realizar un programa en python que reciba por argumentos:
    -p cantidad_procesos
    -f /ruta/al/archivo_matriz.txt
    -c funcion_calculo

El programa deberá leer una matriz almacenada en el archivo de texto pasado por argumento -f, y deberá calcular la funcion_calculo 
para cada uno de sus elementos.

Para aumentar la performance, el programa utilizará un Pool de procesos, y cada proceso del pool realizará los cálculos sobre 
una de las filas de la matriz.

La funcion_calculo podrá ser una de las siguientes:
    raiz: calcula la raíz cuadrada del elemento.
    pot: calcula la potencia del elemento elevado a si mismo.
    log: calcula el logaritmo decimal de cada elemento.

Ejemplo de uso:

Suponiendo que el archivo /tmp/matriz.txt tenga este contenido:
1, 2, 3
4, 5, 6
python3 calculo_matriz -f /tmp/matriz.txt -p 4 -c pot
1, 4, 9
16, 25, 36
"""

from multiprocessing import get_context
import argparse, math, os


def crear_archivo():
    archivo = open("/tmp/matriz.txt", "w")
    archivo.write("1, 2, 3\n4, 5, 6")


def raiz(n):
    return "{} ({})".format(str(math.sqrt(n)), os.getpid())

def pot(n):
    return "{} ({})".format(str(n ** n), os.getpid())

def log(n):
    return "{} ({})".format(str(math.log(n)), os.getpid())

def sobrescribir_archivo(ruta, celdas_matriz_new):
    archivo = open(ruta, "w+")
    archivo.write(" {}, {}, {}\n{}, {}, {}".format(celdas_matriz_new[0], celdas_matriz_new[1], celdas_matriz_new[2], celdas_matriz_new[3], celdas_matriz_new[4], celdas_matriz_new[5]))

    
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help="cantidad de procesos",  required=True)
    parser.add_argument("-f", type=str, help= "path del archivo de texto", default= "/tmp/matriz.txt")
    parser.add_argument("-c", type=str, help="calculo a realizar sobre los elementos de la matriz",  required=True)
    args = parser.parse_args()

    
    archivo = open(args.f, "r")
    celdas_matriz = []
    for linea in archivo.readlines():
        for x in linea:
            if x.isdigit():
                celdas_matriz.append(int(x))



    pool = get_context("fork").Pool(args.p)

    if args.c == "raiz":
        celdas_matriz_new = pool.map(raiz, celdas_matriz)

    elif args.c == "pot":
        celdas_matriz_new = pool.map(pot, celdas_matriz)
    
    elif args.c == "log":
        celdas_matriz_new = pool.map(log, celdas_matriz)
    
    sobrescribir_archivo(args.f, celdas_matriz_new)
    


if __name__=="__main__":
    crear_archivo()
    main()