# Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una computadora remota.
# Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar un cliente (administrador) que permita conectarse al servidor mediante sockets STREAM.
# El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.
# Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:
# la salida estándar resultante de la ejecución del comando
# la salida de error resultante de la ejecución del comando.
# El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que se haya realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.
# El servidor debe poder recibir las siguientes opciones:
# -p <port>: puerto donde va a atender el servidor.
# El servidor deberá poder atender varios clientes simultáneamente utilizando AsyncIO.
# El cliente debe poder recibir las siguientes opciones:
# -h <host> : dirección IP o nombre del servidor al que conectarse.
# -p <port> : número de puerto del servidor.
# Para leer estos argumentos se recomienda usar módulos como argparse o click.
# Ejemplo de ejecución del cliente (la salida de los comandos corresponden a la ejecución en el equipo remoto.
# diego@cryptos$ python3 ejecutor_cliente.py -h 127.0.0.1 -p 2222
# > pwd
# OK
# /home/diego
# > ls -l /home
# OK
# drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
# drwx------   2 root  root  16384 May 28  2014 lost+found
# drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
# > ls /cualquiera
# ERROR
# ls: cannot access '/cualquiera': No such file or directory
# >

import asyncio, time, argparse, subprocess, pickle

async def handle(reader, writer):

    while True:
        
        command = await reader.read(1000)
        command = pickle.loads(command)

        addr = writer.get_extra_info('peername')

        print("\n- {} : {}".format(addr, command))

        if command == "exit":
            writer.write(pickle.dumps("Chau chau"))
            await writer.drain()
            break

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
        salida, error = p.communicate()
            
        if salida == "":
            respuesta = {"ERROR" :error} 
            
        if error == "":
            respuesta =  {"OK" :salida} 

        respuesta = pickle.dumps(respuesta)
        writer.write(respuesta)
        await writer.drain()
        
        
    writer.close()
            

async def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
    args = parser.parse_args()
    puerto = args.p

    server = await asyncio.start_server(handle, '127.0.0.1', puerto)

    address = server.sockets[0].getsockname()

    async with server:
        print("\nTarea: {}".format(asyncio.current_task().get_name()))
        print("\n Serving on ", address)
        await server.serve_forever()


if __name__ == '__main__':

    asyncio.run(main())

#? Correr con: p server.py -p 8888