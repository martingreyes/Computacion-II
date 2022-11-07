"""
Realizar un programa en python que reciba por argumentos:
-f /ruta/al/archivo_matriz.txt
-c funcion_calculo
El programa deberá leer una matriz almacenada en el archivo de texto pasado por argumento -f, y deberá calcular la funcion_calculo para cada uno de sus elementos.
Para aumentar la performance, el programa utilizará un Celery, que recibirá mediante una cola de mensajes Redis, cada una de las tareas a ejecutar.
La funcion_calculo, modelada como tareas de Celery, podrá ser una de las siguientes:
raiz: calcula la raíz cuadrada del elemento.
pot: calcula la potencia del elemento elevado a si mismo.
log: calcula el logaritmo decimal de cada elemento.
Ejemplo de uso:
Suponiendo que el archivo /tmp/matriz.txt tenga este contenido:
1, 2, 3
4, 5, 6
python3 calculo_matriz -f /tmp/matriz.txt -c pot
1, 4, 9
16, 25, 36
"""
import argparse, os, celery_task
from celery import Celery
from celery_task import pot, log, raiz



def crear_archivo():
    archivo = open("/tmp/matriz.txt", "w")
    archivo.write("1, 2, 3 \n4, 5, 6")


def sobrescribir_archivo(ruta, matriz):
    archivo = open(ruta, "w+")
    escritura = " "
    for elemento in matriz:
            escritura = escritura + str(elemento) + " "
    archivo.write(escritura)



def main():
    crear_archivo()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help= "path del archivo de texto", default= "/tmp/matriz.txt")
    parser.add_argument("-c", type=str, help="calculo a realizar sobre los elementos de la matriz",  required=True)
    args = parser.parse_args()


    archivo = open(args.f, "r")
    filas = archivo.readlines()



    if args.c == "raiz":
        matriz =  raiz.delay(filas) 
    
    elif args.c == "pot":
        matriz = pot.delay(filas) 

    elif args.c == "log":
        matriz = log.delay(filas) 

    
    else:
        matriz = nada(filas)
        matriz.append("\nLa operacion {} no existe".format(args.c))

    # ! Nunca entra a redis para hacer la operacion
    print(matriz.ready())
    



    # sobrescribir_archivo(args.f, matriz)



if __name__=="__main__":
    main()


# docker run --rm -p 6379:6379 redis
# celery -A celery_confg worker --loglevel=INFO -c4
# python3 ej17.py -c log