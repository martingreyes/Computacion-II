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
        lineas = archivo.readlines()    # lista donde c/elemento es una linea del .txt

        nbytes = []

        for x in lineas:
            nbytes.append(len(x))
        
    
        padre = os.getpid()

        r, w = os.pipe()
        r2, w2 = os.pipe()

        

        for contador in range(numero):

            os.fork()
            
            if os.getpid() != padre:

                

                # el hijo lee
                os.close(w)
                r = os.fdopen(r)
                string = r.readline(20)
                print("leyendo {} ({})".format(string, os.getpid()))

                # el hijo escribe
                os.close(r2)
                w2 = os.fdopen(w2, 'w')
                pid = os.getpid()
                w2.write("{}".format(string[::-1]))
                w2.close() 

                os._exit(0)           # evito nietos
        
       # escribe el padre
        os.close(r)
        w = os.fdopen(w, 'w')
        for l in lineas:
            w.write(l)
        w.close()

        # lee el padre 
        # os.close(w2)
        # r2 = os.fdopen(r2)
        # while True:
        #     string2 = r2.read()
        #     if len(string2) == 0:
        #         break
        #     print(string2)

        for i in range(numero):
            os.wait()    

if __name__=="__main__":
    crear_archivo()
    main()

# Correr con: p ej6.py -f /tmp/texto.txt