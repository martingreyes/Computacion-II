"""
Escribir un programa que genere dos hijjos utilizando multiprocessing.
Uno de los hijos deberá leer desde stdin texto introducido por el usuario, 
y deberá escribirlo en un pipe (multiprocessing).
El segundo hijo deberá leer desde el pipe el contenido de texto, lo encriptará utilizando 
el algoritmo ROT13, y lo almacenará en una cola de mensajes (multiprocessing).
El primer hijo deberá leer desde dicha cola de mensajes y mostrar el contenido cifrado por pantalla.
"""

import multiprocessing, sys, os, string, time, signal

def primer_hijo(pipe_w, cola):
    sys.stdin = open(0)
    while True:                                       
        print("Ingrese una línea: ") 
        linea = sys.stdin.readline().rstrip("\n")                                           # 1) Hijo 1 lee (tambien le quito el salto de linea al readline)
        pipe_w.send(linea.lower())                                                          # 2) Hijo 1 escribe en pipe 
        
        leido = cola.get()                                                                  # 5) Hijo 1 lee contenido de la cola
        if leido == "bye":
            print("Hijo 1 ({}) muriendo".format(os.getpid()))
            break
        
        print(leido)                                                                        # 6) Hijo 1 lo muestra por pantalla
        
    

def segundo_hijo(cola, pipe_r):
    continuar = True
    while True:
        linea = pipe_r.recv()                                                                # 3) Hijo 2 lee el pipe
        if linea.lower() == "bye":
            cola.put("bye")
            break
        encriptado = ""
        for letra in linea:                               
                letra = string.ascii_letters[string.ascii_letters.index(letra) + 13 ].upper()
                encriptado = encriptado + letra 
                                            
        cola.put(encriptado)                                                                # 4) Hijo 2 almacena en cola de mensajes el texto leido encriptado
    
    print("Hijo 2 ({}) muriendo".format(os.getpid()))
    
if __name__ == "__main__":
    r,w = multiprocessing.Pipe()
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target= primer_hijo, args=(w, q))
    p2 = multiprocessing.Process(target= segundo_hijo, args=(q, r))
    p1.start() 
    p2.start()
    p1.join()
    p2.join()
    
    print("Padre ({}) muriendo".format(os.getpid()))
    