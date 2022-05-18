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
    archivo.write("1, 2, 3 \n4, 5, 6\n6, 7, 8")


def raiz(fila):
    resultado = []
    for x in fila:
        if x.isdigit():
            resultado.append(math.sqrt(int(x))) 
    resultado.append("--> pid: {}".format(str(os.getpid())))
    resultado.append("\n")
    return resultado
    

def pot(fila):
    resultado = []
    for x in fila:
        if x.isdigit():
            resultado.append(int(x) ** int(x)) 
    resultado.append("--> pid: {}".format(str(os.getpid())))
    resultado.append("\n")
    return resultado
    

def log(fila):
    resultado = []
    for x in fila:
        if x.isdigit():
            resultado.append(math.log(int(x)))
    resultado.append("-->pid: {}".format(str(os.getpid())))
    resultado.append("\n")
    return resultado

def nada(fila):
    resultado = []
    for x in fila:
        if x.isdigit():
            resultado.append(x) 
    resultado.append("pid: {}".format(str(os.getpid())))
    resultado.append("\n")
    return resultado



def sobrescribir_archivo(ruta, matriz):
    archivo = open(ruta, "w+")
    escritura = ""
    for fila in matriz:
        for x in fila:
            escritura = escritura + str(x) + " "
    archivo.write(escritura)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help="cantidad de procesos",  required=True)
    parser.add_argument("-f", type=str, help= "path del archivo de texto", default= "/tmp/matriz.txt")
    parser.add_argument("-c", type=str, help="calculo a realizar sobre los elementos de la matriz",  required=True)
    args = parser.parse_args()


    archivo = open(args.f, "r")
    filas = archivo.readlines()

    pool = get_context("fork").Pool(args.p)

    if args.c == "raiz":
        matriz = pool.map(raiz, filas)
    
    elif args.c == "pot":
        matriz = pool.map(pot, filas)

    elif args.c == "log":
        matriz = pool.map(log, filas)
    
    else:
        matriz = pool.map(nada, filas)
        matriz.append("\nLa operacion {} no existe".format(args.c))
    

    sobrescribir_archivo(args.f, matriz)



if __name__=="__main__":
    crear_archivo()
    main()

# Correr con: p ej9.py -p 4 -c log