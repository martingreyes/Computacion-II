import argparse, socketserver, pickle, subprocess, os, threading, socket, sqlite3, multiprocessing, sys

class MyTCPHandler(socketserver.BaseRequestHandler):
    

    def handle(self):           #HIJO 

        conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")

        bienvenida = "- Hola soy el server. Decime tu alias por favor"
        dato = pickle.dumps(bienvenida)
        self.request.sendall(dato)

        print("\n----------- {}:{} ENTRÓ A LA SALA -----------".format(self.client_address[0], self.client_address[1]))

        dato = self.request.recv(1024)
        alias = pickle.loads(dato)

        ip = str(self.client_address[0])

        puerto = str(self.client_address[1])

        existe = conexion.execute("SELECT * FROM jugadores WHERE alias = '{}'".format(alias)).fetchone()

        if existe == None:

            respuesta = "- NEW PLAYER!. Ingrese la contraseña que utilizará para el player '{}'".format(alias)
            dato = pickle.dumps(respuesta)
            self.request.sendall(dato)

            dato = self.request.recv(1024)
            password = pickle.loads(dato)

            conexion.execute("INSERT INTO jugadores (ip, puerto, alias, password) VALUES (?,?,?,?)",(ip, puerto, alias, password))

            conexion.commit()
                    
            conexion.close()

            comienzo = "- Comenzemos a jugar!"
            dato = pickle.dumps(comienzo)
            self.request.sendall(dato)  


        else:

            respuesta = "- WELCOME '{}'!. Ingrese su contraseña".format(alias)
            dato = pickle.dumps(respuesta)
            self.request.sendall(dato)

            dato = self.request.recv(1024)
            password = pickle.loads(dato)

            check = conexion.execute("SELECT * FROM jugadores WHERE alias = '{}' AND password = '{}'".format(alias, password)).fetchone()

            if check == None:                       #TODO Cierro bien la conexion ??
                despedida = pickle.dumps("- Chau chau")
                self.request.sendall(despedida)    
                print("\n----------- {}:{} SALIÓ DE LA SALA -----------".format(self.client_address[0], self.client_address[1]))
                sys.exit()

            else:
                comienzo = "- Comenzemos a jugar!"
                dato = pickle.dumps(comienzo)
                self.request.sendall(dato) 
                    
            conexion.close()

            
 

        while True:

            respuesta = self.request.recv(1024)
            respuesta = pickle.loads(respuesta)

            print("\nDireccion: {}:{} | Proceso: {} ({})| Hilo: {}" .format(self.client_address[0], self.client_address[1], os.getppid(),os.getpid(), threading.current_thread().name))
            print("--> {}".format(respuesta))
            
            if respuesta == "exit":                     #TODO Verificar que efectivamente el server cerro la conexion con ese cliente
                mensaje = pickle.dumps("- Chau chau")
                self.request.sendall(mensaje) 
                print("\n----------- {}:{} SALIÓ DE LA SALA -----------".format(self.client_address[0], self.client_address[1]))
                break                               
    
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








