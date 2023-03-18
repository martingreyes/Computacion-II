import argparse, socketserver, pickle, subprocess, os, threading, socket
from pregunta_random import pregunta_random

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        while True:

            # pregunta, respuesta1, respuesta2 = pregunta_random()

            pregunta = "¿Como me llamo?"
            respuesta1 = "Juan"
            respuesta2 = "Pepe"

            # mensaje = "{} \n- Opción 1: {} \n- Opción 2: {}".format(pregunta["pregunta"], respuesta1["respuesta"], respuesta2["respuesta"])
            mensaje = "{} \n- Opción 1: {} \n- Opción 2: {}".format(pregunta, respuesta1, respuesta2)

            mensaje = pickle.dumps(mensaje)
            self.request.sendall(mensaje)

            respuesta = self.request.recv(1024)
            respuesta = pickle.loads(respuesta)

            # print("\n", threading.current_thread().ident) # Para ver que si es IPv4 es atendido por un hilo y si es IPv6 es atendido por otro
            print("-{}: {} (pid: {}) : {}".format(self.client_address[0], self.client_address[1] ,os.getpid(), respuesta))
            
            if respuesta == "exit":
                mensaje = pickle.dumps("Chau chau")
                self.request.sendall(mensaje) 
                break    
                        

            # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
            # salida, error = p.communicate()
            
            # if salida == "":
            #     dato =  {"ERROR" :error} 
            #     dato = pickle.dumps(dato)
            #     self.request.sendall(dato)
            
            # if error == "":
            #     dato =  {"OK" :salida} 
            #     dato = pickle.dumps(dato)
            #     self.request.sendall(dato)


class ForkedTCPServer4(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ForkedTCPServer6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass

def abrir_socket_procesos(direccion):
    socketserver.TCPServer.allow_reuse_address = True

    if direccion[0] == socket.AF_INET:
        with ForkedTCPServer4(direccion[4], MyTCPHandler) as server:
                server.serve_forever()

    elif direccion[0] == socket.AF_INET6:
        with ForkedTCPServer6(direccion[4], MyTCPHandler) as server:
            server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
    args = parser.parse_args()

    puerto = args.p

    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET, 1)[0])
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET6, 1)[0])


    # print("\nProceso padre", os.getpid(), "\n")
    for direccion in direcciones:
        print("Server levantado en {}: {} \n".format(direccion[4][0], direccion[4][1]))
        threading.Thread(target=abrir_socket_procesos, args=(direccion,)).start()   # Lanzo un hilo para sokcet IPv4 y otro para IPv6

#? Correr con p server.py -p 1234








