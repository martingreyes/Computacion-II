# Escribir un programa que reciba por argumento la opción -f acompañada de un path_file.

# Etapa 1:
# El programa deberá crear una memoria compartida (variable global, queue, etc.), y generar dos hilos: H1 y H2
# El hilo H1 leerá desde el stdin línea por línea lo que ingrese el usuario.
# Cada vez que el usuario ingrese una línea, H1 la almacenará en la memoria compartida, y notificará, mediante event/condition, al hilo H2.
# El hilo H2 al recibir la notificación leerá la línea desde la memoria compartida la línea, y la almacenará en mayúsculas en el archivo pasado por argumento (path_file).

# Etapa 2 (opcional):

# Cuando el usuario introduzca "bye" por terminal, el hilo H1 notificará a los otros dos hilos y terminará.
# El hilo principal y el hilo H2 terminarán también.

import argparse, queue, threading, sys
from threading import Event, Thread

def crear_archivo():
    archivo = open("/tmp/archivo.txt", "w")


def leer(cola, event):
    sys.stdin = open(0)
    while True:                                       
        print("\nIngrese una línea: ", end="") 
        linea = sys.stdin.readline().rstrip("\n") 
        cola.put(linea)
        
        if linea == "bye":
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break

        event.wait()
        event.clear()
    
 
def escribir(cola, ruta, event):
    while True:
        linea = cola.get()
        if linea.lower() == "bye":
            # cola.task_done()
            print("\nHilo {} muriendo".format(threading.current_thread().name))
            break
        
        archivo = open(ruta, "a")
        archivo.write(linea.upper())
        event.set()
        

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help= "path del archivo de texto", default= "/tmp/archivo.txt")
    args = parser.parse_args()

    event = Event()

    ruta = args.f

    cola = queue.Queue()

    hilo1 = threading.Thread(target=leer, args= (cola, event), name= "hilo1" , daemon=True)
    hilo2 = threading.Thread(target=escribir, args= (cola, ruta, event), name= "hilo2", daemon=True)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("\nHilo {} muriendo".format(threading.current_thread().name))

if __name__ == "__main__":
    crear_archivo()
    main()
