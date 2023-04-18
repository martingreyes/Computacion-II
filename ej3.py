# Escribir un programa que reciba por argumentos de línea de comandos los siguientes modificadores:
# -c command
# -o output_file
# -l log_file

# El código deberá crear los archivos pasados por los argumentos -o y -l en el caso de que no existan.
# El código deberá ejecutar el comando haciendo uso de subprocess.Popen, y almacenar su salida en el archivo pasado en el parámetro -f. 
# En el archivo pasado por el modificador -l deberá almacenar el mensaje “fechayhora: Comando XXXX ejecutado correctamente” o en su defecto el mensaje de error generado por el comando si este falla.

# Por ejemplo:
# python ejecutor.py -c “ip a” -o /tmp/salida -l /tmp/log

# El archivo /tmp/salida deberá contener la salida del comando, y /tmp/log deberá contener:

# fechayhora: Comando “ip a” ejecutado correctamente.

# Otro ejemplo:

# python ejecutor.py -c “ls /cualquiera” -o /tmp/salida -l /tmp/log

# El archivo /tmp/salida no contendrá nada nuevo, ya que el comando fallará. El archivo /tmp/log contendrá:
# fechayhora: ls: cannot access '/cualquiera': No such file or directory

"""
Diferencia entre sdtin, stdout, stderr:
https://blog.carreralinux.com.ar/2017/07/descriptores-de-archivo-stdin-stdout-stderr/
"""

def main():

    import argparse
    import sys
    import os
    import subprocess
    import codecs

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, help="command")          #Hay que hacer un add por cada opcion.
    parser.add_argument("-o", type=str, help="output file")
    parser.add_argument("-l", type=str, help="log file")
    args = parser.parse_args()

    output_file = args.o

    log_file = args.l

    comando = args.c

    with open(output_file, "w") as output:

        process = subprocess.Popen(comando.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        stdout, stderr = process.communicate()
        process2 = subprocess.Popen("date ", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout2, stderr2 = process2.communicate()
        output.write(stdout)
        
        
    with open(log_file, "a") as log:
        if stderr == b"":
            log.write(stdout2[:-2] + b": Comando " + bytes(comando, encoding = "utf-8"  ) + b" ejecutado correctamente.\n")
        
        else:
            log.write(stdout2[:-2] + b" " + stderr)


if __name__ == "__main__":
    main()









