import os
import argparse
import subprocess
import string
import time

def main():

        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=str, help= "path del archivo de texto", required=True)
        args = parser.parse_args()

        with open(args.f) as archivo:
            numero = sum(1 for line in archivo)
        
        archivo = open(args.f, "r")
        lineas = archivo.readlines()

        padre = os.getpid()

        contador = 0

        for contador in range(numero):

            r, w = os.pipe()
            r2, w2 = os.pipe()

            os.fork()
            
            if os.getpid() == padre:                   # Proceso padre

                # primero el padre escribe
                os.close(r)
                w = os.fdopen(w, 'w')
                # print("Padre escribiendo: {}".format(lineas[contador]))
                w.write(lineas[contador])
                w.close()

            if os.getpid() != padre:         

                # primero el hijo lee
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

                os._exit(0)

            if os.getpid() == padre: 

                # ahora empieza a leer el padre

                os.close(w2)
                r2 = os.fdopen(r2)
                string2 = r2.read()
                # print("\nPadre leyendo: \n{}\n".format(string2))
                print(string2)

                                   
        for i in range(numero):
            os.wait()    

if __name__=="__main__":
    main()

# Correr con p ej6.py -f /Users/martinreyes/Downloads/texto.txt