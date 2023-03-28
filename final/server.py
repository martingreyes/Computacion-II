import argparse, socketserver, pickle, subprocess, os, threading, socket, sqlite3, multiprocessing

class MyTCPHandler(socketserver.BaseRequestHandler):
    

    def handle(self):

        mensaje = "- Hola soy el server"
        mensaje = pickle.dumps(mensaje)
        self.request.sendall(mensaje)

        while True:
        
            respuesta = self.request.recv(1024)
            respuesta = pickle.loads(respuesta)

            print("\nDireccion: {}:{} | Proceso: {} ({})| Hilo: {}" .format(self.client_address[0], self.client_address[1], os.getppid(),os.getpid(), threading.current_thread().name))
            print("--> {}".format(respuesta))
            
            if respuesta == "exit":
                mensaje = pickle.dumps("- Chau chau")
                self.request.sendall(mensaje) 
                break                               #TODO Verificar que efectivamente el server cerro la conexion con ese cliente
    
            mensaje = "- OK"
            mensaje = pickle.dumps(mensaje)
            self.request.sendall(mensaje) 




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

    print("\nProceso: {} Hilo: {}" .format(os.getpid(), threading.current_thread().name))
    for direccion in direcciones:
        print("\nLevantado server en {}: {} ...".format(direccion[4][0], direccion[4][1]))
        threading.Thread(target=abrir_socket_procesos, args=(direccion,)).start()   # Lanzo un hilo para sokcet IPv4 y otro para IPv6

#? Correr con p server.py -p 1234








