# Modificar el código de shell remota realizado con anterioridad ([serversocket]) para que atienda en todas las IP's del sistema operativo, 
# independientemente de que se trate de IPv4 o IPv6.
# Lance un thread para cada socket (un thread para IPv4 y otro para IPv6).
# El servidor de shell debe mantener la concurrencia para atender a varios clientes, ya sea por procesos o hilos, dependiendo del parámetro pasado por argumento "-c".

import argparse, socketserver, pickle, subprocess, os, threading, socket

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        while True:

            command = self.request.recv(1024)
            command = pickle.loads(command)

            if args.c == "p":
                print("- {} {} ({} {}) : {} (Proceso hijo {})".format(self.client_address[0], self.client_address[1] ,threading.current_thread().name, threading.get_native_id(), command, os.getpid(),))
            if args.c == "t":
                if len(self.client_address) == 2:
                    print("- {} {} ({} {}) : {} ({}: {})".format(self.client_address[0], self.client_address[1], nombre_hilo4, numero_hilo4,  command, threading.current_thread().name, threading.get_native_id()))
                elif len(self.client_address) == 4:
                    print("- {} {} ({} {}) : {} ({}: {})".format(self.client_address[0], self.client_address[1], nombre_hilo6, numero_hilo6,  command, threading.current_thread().name, threading.get_native_id()))
            
            if command == "exit":
                dato = pickle.dumps("Chau chau")
                self.request.sendall(dato) 
                break    
                        

            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
            salida, error = p.communicate()
            
            if salida == "":
                dato =  {"ERROR" :error} 
                dato = pickle.dumps(dato)
                self.request.sendall(dato)
            
            if error == "":
                dato =  {"OK" :salida} 
                dato = pickle.dumps(dato)
                self.request.sendall(dato)


        
class ForkedTCPServer4(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ForkedTCPServer6(socketserver.ForkingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass


class ThreadedTCPServer4(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET
    pass

class ThreadedTCPServer6(socketserver.ThreadingMixIn, socketserver.TCPServer):
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

def abrir_socket_hilos(direccion):
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






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
    parser.add_argument("-c",type=str, help= "modo de concurrencia", choices=["p", "t"])
    args = parser.parse_args()

    puerto = args.p
    concurrencia = args.c

    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET, 1)[0])
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET6, 1)[0])


    if concurrencia.lower() == "p":
        print("\nProceso padre", os.getpid(), "\n")
        for direccion in direcciones:
            print("Server: ", direccion[4], " levantado\n")
            threading.Thread(target=abrir_socket_procesos, args=(direccion,)).start()


    if concurrencia.lower() == "t":
        print("\n", threading.current_thread().name, threading.get_native_id(), "\n")
        socketserver.TCPServer.allow_reuse_address = True
        for direccion in direcciones:
            print("Server: ", direccion[4], " levantado\n")
            threading.Thread(target=abrir_socket_hilos, args=(direccion,)).start()

           
   

#? Correr con p server.py -p 1234 -c p



