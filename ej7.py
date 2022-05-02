"""
    Escribir un programa que reciba por argumento la 
    opción -f acompañada de un path_file.
    >Etapa 1:
    El programa deberá crear un segmento de memoria
    compartida anónima, y generar dos hijos: H1 y H2
    El H1 leerá desde el stdin línea por línea lo que 
    ingrese el usuario.
    Cada vez que el usuario ingrese una línea, H1 la 
    almacenará en el segmento de memoria compartida, 
    y enviará la señal USR1 al proceso padre.
    El proceso padre, en el momento en que reciba la 
    señal USR1 deberá mostrar por pantalla el contenido 
    de la línea ingresada por el H1 en la memoria 
    compartida, y deberá notificar al H2 usando la 
    señal USR1.
    El H2 al recibir la señal USR1 leerá la línea 
    desde la memoria compartida la línea, y la 
    almacenará en mayúsculas en el archivo pasado 
    por argumento (path_file).
    >Etapa 2:
    Cuando el usuario introduzca "bye" por terminal, 
    el hijo H1 enviará la señal USR2 al padre indicando 
    que va a terminar, y terminará.
    El padre, al recibir la señal USR2 la enviará al 
    H2, que al recibirla terminará también.
    El padre esperará a que ambos hijos hayan 
    terminado, y terminará también.
"""

import os, mmap, argparse, sys, signal

def handler_padre(signum, frame):
    
    if signum == signal.SIGUSR1:
        print(memoria.read(1024).decode().upper())
        memoria.seek(0)
        os.kill(h2, signal.SIGUSR1)
    
    if signum == signal.SIGUSR2:
        os.kill(h2, signal.SIGUSR2)
        for i in range(2):
            os.wait()
        print("Padre terminado ({}) ".format(os.getpid()))
        sys.exit(0)

def handler_h2(signum, frame):

    if signum == signal.SIGUSR1:
        leido = memoria.read(1024)
        memoria.seek(0)
        with open(args.f, 'w+') as archivo:
            archivo.write(leido.decode().upper())
   
    if signum == signal.SIGUSR2:
        print("Terminando segundo hijo ({})".format(os.getpid()))
        sys.exit(0) 

parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, help= "ruta de archivo txt", required=True)
args = parser.parse_args()

memoria = mmap.mmap(-1, 1024 )

for x in range(2):

    pid = os.fork()

    if x == 0:      # esto hace h1 
        
        h1 = pid   
        if h1 == 0:
            
            for linea in sys.stdin:
                    
                if linea.lower() == "bye\n":
                    print("Terminando primer hijo ({})".format(os.getpid()))
                    os.kill(os.getppid(), signal.SIGUSR2)
                    sys.exit(0) 

                memoria.write(linea.encode())
                os.kill(os.getppid(), signal.SIGUSR1) # --> arreglar esto que no anda
            
                
    elif x == 1:    # esto hace h2
                    
        h2 = pid   
        if h2 == 0:

            while True:
                signal.signal(signal.SIGUSR1, handler_h2)
                signal.signal(signal.SIGUSR2, handler_h2)
                signal.pause()
                
while True:
    signal.signal(signal.SIGUSR1, handler_padre)
    signal.signal(signal.SIGUSR2, handler_padre)
    signal.pause()

# p ej7.py -f /tmp/archivo.txt