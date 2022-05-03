"""
Escribir un programa que genere dos hijjos utilizando multiprocessing.
Uno de los hijos deberá leer desde stdin texto introducido por el usuario, 
y deberá escribirlo en un pipe (multiprocessing).
El segundo hijo deberá leer desde el pipe el contenido de texto, lo encriptará utilizando 
el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).
El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.
"""

import multiprocessing, sys, os, string, time

def primer_hijo(pipe_w, cola):
    linea = "klm"                    #TODO stdin                                      # 1) Hijo 1 lee  
    pipe_w.send(linea.lower())                                                         # 2) Hijo 1 escribe en pipe 

    print(cola.get())                                                                   # 5) Hijo 1 lee contenido de la cola y lo muestra por pantalla
    # print("Hijo 1 ({}) muriendo".format(os.getpid()))

def segundo_hijo(cola, pipe_r):
    linea = pipe_r.recv()                                                               # 3) Hijo 2 lee el pipe
    encriptado = ""
    for letra in linea:
        letra = string.ascii_letters[string.ascii_lowercase.index(letra) + 13 ].upper()
        encriptado = encriptado + letra                                               
    cola.put(encriptado)                                                                # 4) Hijo 2 almacena en cola de mensajes el texto leido encriptado
    # print("Hijo 2 ({}) muriendo".format(os.getpid()))
    
        
if __name__ == "__main__":
    r,w = multiprocessing.Pipe()
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target= primer_hijo, args=(w, q))
    p2 = multiprocessing.Process(target= segundo_hijo, args=(q, r))
    p1.start() 
    p2.start()
    p1.join()
    p2.join()
    # print("Padre ({}) muriendo".format(os.getpid()))
    