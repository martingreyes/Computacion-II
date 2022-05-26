
# Escribir un programa que genere dos hilos utilizando threading.

# Uno de los hilos debera leer desde stdin texto introducido por el usuario, y debera escribirlo en un pipe (threading).

# El segundo hijo debera leer desde el pipe el contenido de texto, lo encriptara utilizando el algoritmo ROT13, 
# y lo almacenara en una cola de mensajes (queue).

# El primer hijo debera leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.

import threading, sys, multiprocessing, string, queue

def leer(pipe_w, cola):
    sys.stdin = open(0)
    while True:                                       
        print("\nIngrese una línea: ", end="") 
        linea = sys.stdin.readline().rstrip("\n")                                 
        pipe_w.send(linea.lower())
        encriptado = cola.get()
        if encriptado == "bye":
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break
        print(encriptado)
    

def encriptar(pipe_r, cola):
    while True:
        linea = pipe_r.recv()
        if linea.lower() == "bye":
            cola.put("bye")
            cola.task_done()
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break
        encriptado = ""
        for letra in linea:                               
                letra = string.ascii_letters[string.ascii_letters.index(letra) + 13 ].upper()
                encriptado = encriptado + letra
        cola.put(encriptado)
        

def main():
    r,w = multiprocessing.Pipe()
    cola = queue.Queue()
    hilo1 = threading.Thread(target=leer,args= (w, cola) , name= "hilo1" , daemon=True)
    hilo2 = threading.Thread(target=encriptar, args= (r, cola), name= "hilo2", daemon=True)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("\nHilo {} muriendo".format(threading.current_thread().name))

if __name__ == "__main__":
    main()
