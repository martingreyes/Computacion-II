import argparse, socketserver, pickle, subprocess, os, threading, socket, sqlite3
from pregunta_random import pregunta_random

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        global conexion

        print(conexion)

        alias = self.request.recv(1024)

        alias = pickle.loads(alias)

        print("\n¡ {} se ha unido!".format(alias))

        contador = 1

        puntaje = 0

        while True:

            if contador == 6:
                break

            pregunta, respuesta1, respuesta2 = pregunta_random(conexion)

            mensaje = "{}) {} \n     A) {} \n     B) {}".format(contador,pregunta["pregunta"], respuesta1["respuesta"], respuesta2["respuesta"])

            mensaje = pickle.dumps(mensaje)
            self.request.sendall(mensaje)

            respuesta = self.request.recv(1024)
            respuesta = pickle.loads(respuesta)

            print("\nAlias: {} | Direccion: {}:{} | Proceso: {} | Hilo: {}" .format(alias, self.client_address[0], self.client_address[1], os.getpid(), threading.current_thread().name))
            print("{}: {}".format(pregunta["pregunta"],respuesta))
            
            if respuesta == "exit":
                mensaje = pickle.dumps("Chau chau")
                self.request.sendall(mensaje) 
                print("\n¡ {} se ha ido!".format(alias))
                break   

            if respuesta == "A":
                if respuesta1["correcta"] == 1:
                    puntaje = puntaje + 20

            else:
                if respuesta2["correcta"] == 1:
                    puntaje = puntaje + 20


            contador = contador + 1

        mensaje = pickle.dumps("FIN. Gracias por participar!\n")
        self.request.sendall(mensaje)
        #TODO Mostrarle al cliente su puntaje y la tabla de posiciones
        print("\n¡ {} ha finalizado!".format(alias))

#TODO Arreglar

# class ForkedTCPServer4(socketserver.ForkingMixIn, socketserver.TCPServer):
#     address_family = socket.AF_INET
#     pass

# class ForkedTCPServer6(socketserver.ForkingMixIn, socketserver.TCPServer):
#     address_family = socket.AF_INET6
#     pass

# def abrir_socket_procesos(direccion):
#     socketserver.TCPServer.allow_reuse_address = True

#     if direccion[0] == socket.AF_INET:
#         with ForkedTCPServer4(direccion[4], MyTCPHandler) as server:
#                 server.serve_forever()

#     elif direccion[0] == socket.AF_INET6:
#         with ForkedTCPServer6(direccion[4], MyTCPHandler) as server:
#             server.serve_forever()


#! Si en vez de usar hilos uso procesos (lo que esta comentado) tira error cuando llamo a
#! pregunta_random(conexion) ya que habrian dos procesos (proceso padre y proceso hijo) 
#! que utilizan la conexion al mismo tiempo.

#? PROVISORIO

class ThreadedTCPServer4(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ThreadedTCPServer6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass

def abrir_socket_procesos(direccion):
    socketserver.TCPServer.allow_reuse_address = True

    if direccion[0] == socket.AF_INET:
        global nombre_hilo4
        nombre_hilo4 = threading.current_thread().name
        global numero_hilo4
        numero_hilo4 = threading.get_native_id()
        with ThreadedTCPServer4(direccion[4], MyTCPHandler) as server:
            server.serve_forever()

    elif direccion[0] == socket.AF_INET6:

        global nombre_hilo6
        nombre_hilo6 = threading.current_thread().name
        global numero_hilo6
        numero_hilo6 = threading.get_native_id()

        with ThreadedTCPServer6(direccion[4], MyTCPHandler) as server:
            server.serve_forever()

#? FIN PROVISORIO


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
    args = parser.parse_args()

    conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db", check_same_thread=False)

    puerto = args.p

    pregunta, respuesta1, respuesta2 = pregunta_random(conexion)

    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET, 1)[0])
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET6, 1)[0])

    print("\nProceso: {} Hilo: {}" .format(os.getpid(), threading.current_thread().name))
    for direccion in direcciones:
        print("\nLevantado server en {}: {} ...".format(direccion[4][0], direccion[4][1]))
        threading.Thread(target=abrir_socket_procesos, args=(direccion,)).start()   # Lanzo un hilo para sokcet IPv4 y otro para IPv6

#? Correr con p server.py -p 1234








