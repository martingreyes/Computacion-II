import argparse
import subprocess
import os
import string
import time

def main():

        parser = argparse.ArgumentParser()
        parser.add_argument("-f", type=str, help= "path del archivo de texto", required=True)
        args = parser.parse_args()

        archivo = open(args.f, "r")

        lineas = archivo.readlines()

        numero = sum(1 for line in archivo)

        padre = os.getpid()

        r, w = os.pipe()

        r2, w2 = os.pipe()

        contador = 0
        
        os.fork()

        if os.getpid() == padre:

            # primero el padre escribe

            os.close(r)

            w = os.fdopen(w, 'w')

            print("Padre escribiendo: {}".format(lineas[contador]))

            w.write(lineas[contador])

            w.close()

            # ahora empieza a leer el padre

            os.close(w2)

            r2 = os.fdopen(r2)

            string2 = r2.read()

            print("\nPadre leyendo: \n{}".format(string2))

            os._exit(0)

            contador = contador + 1

        if os.getpid() != padre:        # Lo que esta dentro de este if solamente lo hacen los hijos

            # primero el hijo lee

            os.close(w)
            
            r = os.fdopen(r)

            string = r.read()

            print("Hijo {} leyendo: {}".format(os.getpid(), string))

            # ahora empieza a escribir el hijo

            os.close(r2)

            w2 = os.fdopen(w2, 'w')

            print("\nHijo {} escribiendo: \n{}".format(os.getpid(), string[::-1]))

            w2.write(string[::-1])

            w2.close()

            os._exit(0)            

        
if __name__=="__main__":
    main()