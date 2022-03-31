# Escribir un programa en Python que reciba los siguientes argumentos por línea de comandos:
#     -n <numero>
#     -h
#     -v

# El programa debe generar <numero> procesos hijos, y cada proceso calculará la suma de 
# todos los números enteros pares entre 0 y su número de PID.

# El programa deberá mostrar por pantalla:
#     PID – PPID : <suma_pares>
#     El proceso padre debe esperar a que todos sus hijos terminen.
#     La opción -h mostrará ayuda de uso, y la opción -v habilitará el modo verboso de la aplicación. 
#     El modo verboso debe mostrar, además de la suma, un mensaje al inicio y al final de la ejecución de cada proceso hijo, que indique su inicio y fin.


# Ejemplos 1:
# ./sumapares.py -n 2
# 32803 – 4658: 269009202
# 32800 – 4658: 268943600

# Ejemplos 2:
# ./sumapares.py -n 2 -v
# Starting process 32800
# Starting process 32803
# Ending process 32803
# 32803 – 4658: 269009202
# Ending process 32800
# 32800 – 4658: 268943600


import os, argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="seguido de -n ponga el numero de procesos que se generaran", required=True)         
    parser.add_argument("-v", help="ponga -v para activar el modo verboso", action='store_true', default=False)
    args = parser.parse_args()

    numero = args.n
    verboso = args.v
    padre = os.getpid()

    def suma(pid):

        sumatoria = 0

        for x in range((pid)):

            if x % 2 == 0:

                sumatoria = sumatoria + x
            
        return sumatoria
    
    for x in range(numero):
      
            os.fork()

            if os.getpid() != padre:    # Lo que esta dentro de este if solamente lo hacen los hijos

                if verboso is True:

                    print("\nStarting process ", os.getpid())
                    
                    print("\nEnding process ", os.getpid())

                    print("\n", os.getpid(), " - ", os.getppid(), ": ", suma(os.getpid()))
                    
                else:
                    
                    print("\n", os.getpid(), " - ", os.getppid(), ": ", suma(os.getpid()) )
                
                os._exit(0)             # Evita nietos (?)

            os.wait()                   # Padre espera a que termine el hijo
    
    # print("Termino el padre")         # Si descomento esta linea se puede ver como el proceso padre espera a que se ejecuten todos los procesos hijos. El proceso padre es el ultimo en terminar.

if __name__=="__main__":
    main()
