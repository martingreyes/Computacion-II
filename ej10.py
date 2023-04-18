
# Escribir un programa que genere dos hilos utilizando threading.

# Uno de los hilos debera leer desde stdin texto introducido por el usuario, y debera escribirlo en un pipe (threading).

# El segundo hijo debera leer desde el pipe el contenido de texto, lo encriptara utilizando el algoritmo ROT13, 
# y lo almacenara en una cola de mensajes (queue).

# El primer hijo debera leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

#? Thread (hilos) sirve mas para las tareas de entrada y salida, mientras que los procesos hijos sirven mas para tareas de mayor procesamiento de datos
#? Use Queue para IPC y no multiprocessing.pipe ya que esta ultima no es thread safe

import threading, sys, string, queue

def leer(cola, cola2):
    sys.stdin = open(0)
    while True:                                       
        print("\nIngrese una línea: ", end="") 
        linea = sys.stdin.readline().rstrip("\n") 
        cola.put(linea.lower())
        encriptado = cola2.get()
        if encriptado == "bye":
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break
        print(encriptado)
    
 
def encriptar(cola, cola2):
    while True:
        linea = cola.get()
        if linea.lower() == "bye":
            cola2.put("bye")
            cola2.task_done()
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break
        encriptado = ""
        for letra in linea:                               
                letra = string.ascii_letters[string.ascii_letters.index(letra) + 13 ].upper()
                encriptado = encriptado + letra
        cola2.put(encriptado)
        

def main():
    cola = queue.Queue()
    cola2 = queue.Queue()
    hilo1 = threading.Thread(target=leer,args= (cola, cola2) , name= "hilo1" , daemon=True)
    hilo2 = threading.Thread(target=encriptar, args= (cola, cola2), name= "hilo2", daemon=True)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("\nHilo {} muriendo".format(threading.current_thread().name))

if __name__ == "__main__":
    main()
