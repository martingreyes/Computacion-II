import os
import argparse
import subprocess
import string
import time

def  crear_archivo():
    archivo = open("/tmp/texto.txt", "w+")
    archivo.write("Hola Mundo \nque tal \neste es un archivo \nde ejemplo. ")

def main():

        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=str, help= "path del archivo de texto", required=True)
        args = parser.parse_args()

        with open(args.f) as archivo:
            numero = sum(1 for line in archivo)
        
        archivo = open(args.f, "r")
        lineas = archivo.readlines()

        padre = os.getpid()

        for contador in range(numero):

            r, w = os.pipe()
            r2, w2 = os.pipe()

            os.fork()
            
            if os.getpid() == padre:    # Proceso padre

                # el padre escribe
                os.close(r)
                w = os.fdopen(w, 'w')
                # print("Padre escribiendo: {}".format(lineas[contador]))
                w.write(lineas[contador])
                w.close()

            if os.getpid() != padre:         

                # el hijo lee
                os.close(w)
                r = os.fdopen(r)
                string = r.read()
                # print("Hijo {} leyendo: {}".format(os.getpid(), string))

            if os.getpid() != padre: 
                
                # ahora empieza a escribir el hijo
                os.close(r2)
                w2 = os.fdopen(w2, 'w')
                pid = os.getpid()
                # print("Hijo {} escribiendo: \n{}".format(os.getpid(), string[::-1]))
                w2.write("{} ({})".format(string[::-1], os.getpid()))
                w2.close() 

                os._exit(0)             # puse el os._exit(0) ya que este es lo ultimo que tiene que hacer el hijo, y asi evita nietos

            if os.getpid() == padre: 

                # finalmente lee el padre
                os.close(w2)
                r2 = os.fdopen(r2)
                string2 = r2.read()
                # print("\nPadre leyendo: \n{}\n".format(string2))
                print(string2)
            
        # print("\nTermino padre ({})".format(os.getpid()))        # si descomento esto se puede ver como padre es el ultimo en terminar
                                   
        for i in range(numero):
            os.wait()    

if __name__=="__main__":
    crear_archivo()
    main()

# Correr con: p ej6.py -f /tmp/texto.txt