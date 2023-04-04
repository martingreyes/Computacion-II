import argparse, socketserver, pickle, os, threading, socket, sqlite3, multiprocessing, sys, signal, psutil, time
from termcolor import colored
from pregunta import pregunta_random
class MyTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):           #? HIJO 

        print(colored("\nProceso HIJO: {} {} Hilo: {} está recibiendo un cliente".format(os.getppid(), os.getpid(), threading.current_thread().name), "cyan"))

        conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")

        bienvenida = "- SERVER: Hola soy el server. ¿Cómo te llamas?"
        dato = pickle.dumps(bienvenida)
        self.request.sendall(dato)

        print("\n----------- {}:{} ENTRÓ A LA SALA -----------".format(self.client_address[0], self.client_address[1]))

        dato = self.request.recv(1024)
        alias = pickle.loads(dato)
        ip = str(self.client_address[0])
        puerto = str(self.client_address[1])

        existe = conexion.execute("SELECT * FROM jugadores WHERE alias = '{}'".format(alias)).fetchone()

        if existe == None:
            respuesta = "- SERVER: NEW PLAYER!. Ingrese la contraseña que utilizará para el player '{}'".format(alias)
            dato = pickle.dumps(respuesta)
            self.request.sendall(dato)

            dato = self.request.recv(1024)
            password = pickle.loads(dato)

            conexion.execute("INSERT INTO jugadores (ip, puerto, alias, password) VALUES (?,?,?,?)",(ip, puerto, alias, password))
            conexion.commit()
            conexion.close()

            comienzo = "- SERVER: Comenzemos a jugar!"
            dato = pickle.dumps(comienzo)
            self.request.sendall(dato)  

        else:
            respuesta = "- WELCOME '{}'!. ¿Cúal es tu contraseña?".format(alias)
            dato = pickle.dumps(respuesta)
            self.request.sendall(dato)

            dato = self.request.recv(1024)
            password = pickle.loads(dato)

            check = conexion.execute("SELECT * FROM jugadores WHERE alias = '{}' AND password = '{}'".format(alias, password)).fetchone()
            if check == None:                      
                despedida = pickle.dumps("- SERVER: Chau chau")
                self.request.sendall(despedida)    
                print("\n-----------  '{}' {}:{} SALIÓ DE LA SALA -----------".format(alias,self.client_address[0], self.client_address[1]))
                print(colored("\nProceso HIJO: {} {} Hilo: {} está muriendo ... ".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))
                sys.exit()

            else:
                comienzo = "- SERVER: Comenzemos a jugar!"
                dato = pickle.dumps(comienzo)
                self.request.sendall(dato) 
                    
            conexion.close()

        r1,w1 = multiprocessing.Pipe()
        r2,w2 = multiprocessing.Pipe()

        pid1 = os.fork()

        contador = 1
        puntaje = 0
        preguntas = True
        hechas = []
    
        while True:

            if pid1 == 0:       #? NIETO 
                conexion = sqlite3.connect("/Users/martinreyes/Documents/Facultad/3ro/Computacion II/Computacion-II/final/trivia.db")
                if preguntas:
                    print(colored("\nProceso NIETO: {} {} Hilo: {} está buscando pregunta en la BD".format(os.getppid(), os.getpid(), threading.current_thread().name), "magenta"))
                    pregunta, respuesta1, respuesta2 = pregunta_random(conexion, hechas)
                    w1.send(pregunta)
                    w1.send(respuesta1)
                    w1.send(respuesta2)

                    msg = r2.recv()

                else:
                    print(colored("\nProceso NIETO: {} {} Hilo: {} está escribiendo puntaje en la BD".format(os.getppid(), os.getpid(), threading.current_thread().name), "magenta"))
                    puntaje = r2.recv()
                    conexion.execute("""UPDATE jugadores SET puntaje = {} WHERE alias = '{}' """.format(puntaje, alias))
                    conexion.commit()
                    ranking = conexion.execute("SELECT puntaje, alias FROM jugadores ORDER by puntaje DESC").fetchall()
                    w1.send(ranking)
                    conexion.close()
                    break
                    
        
            else:               #? HIJO

                if preguntas:
                    print(colored("\nProceso HIJO: {} {} Hilo: {} está interactuando con '{}'".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))
                    pregunta = r1.recv()
                    respuesta1 = r1.recv()
                    respuesta2 = r1.recv()
                    pregunta_completa = "- {}) {} \n     a) {} \n     b) {}".format(contador, pregunta["pregunta"], respuesta1["respuesta"], respuesta2["respuesta"])

                    dato = pickle.dumps(pregunta_completa)
                    self.request.sendall(dato) 

                    respuesta = self.request.recv(1024)
                    respuesta = pickle.loads(respuesta)

                    if respuesta == "exit":                     
                        mensaje = pickle.dumps("- SERVER: Chau chau")
                        self.request.sendall(mensaje) 
                        print("\n-----------  '{}' {}:{} ABANDONO DE LA SALA -----------".format(alias,self.client_address[0], self.client_address[1]))
                        
                        os.kill(pid1, signal.SIGTERM)      #? No hace falta ya que NIETO se muere cuando HIJO muere 
                        time.sleep(2)
                        nieto = psutil.Process(pid1)
                        print(colored("\nProceso NIETO: {} {} Hilo: {} ha muerto. Su estado es {}".format(os.getppid(), os.getpid(), threading.current_thread().name, nieto.status()), "magenta"))
                        print(colored("\nProceso HIJO: {} {} Hilo: {} está muriendo ... ".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))
                        break 

                    if respuesta == "a":
                        elegida = respuesta1
                    else:
                        elegida = respuesta2

                    if elegida["correcta"] == 1:

                        puntaje = puntaje + 20

                    w2.send("\nNECESITO OTRA PREGUNTA!")


                else:
                    print(colored("\nProceso HIJO: {} {} Hilo: {} está mostrando puntaje a '{}'".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))
                    mensaje = pickle.dumps("- SERVER: Obtuviste {} puntos".format(puntaje))
                    self.request.sendall(mensaje) 
                    w2.send(puntaje)

                    ranking = r1.recv()

                    os.kill(pid1, signal.SIGTERM)      #? No hace falta ya que NIETO se muere cuando HIJO muere 
                    time.sleep(2)
                    nieto = psutil.Process(pid1)
                    print(colored("\nProceso NIETO: {} {} Hilo: {} ha muerto. Su estado es {}".format(os.getppid(), os.getpid(), threading.current_thread().name, nieto.status()), "magenta"))
               
                    
                    print(colored("\nProceso HIJO: {} {} Hilo: {} está mostrando ranking a '{}'".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))

                    msg = "- SERVER: Mira como quedó el Ranking\n"
                    contador = 1
                    for jugador in ranking:
                        msg = msg + "\n  {}º {} {} pts".format(contador, jugador[1], jugador[0])
                        contador = contador +1

                    mensaje = pickle.dumps(msg)
                    self.request.sendall(mensaje)                 

                    print("\n-----------  '{}' {}:{} SALIÓ DE LA SALA -----------".format(alias,self.client_address[0], self.client_address[1]))
                    
                    print(colored("\nProceso HIJO: {} {} Hilo: {} está muriendo ... ".format(os.getppid(), os.getpid(), threading.current_thread().name, alias), "cyan"))
                    break 


            contador = contador + 1


            if contador == 6:
                preguntas = False



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
    parser.add_argument("-p", default=1234, type=int, help= "puerto donde va atender el servidor")
    args = parser.parse_args()

    puerto = args.p

    direcciones = []
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET, 1)[0])
    direcciones.append(socket.getaddrinfo("localhost", puerto, socket.AF_INET6, 1)[0])

    for direccion in direcciones:
        print(colored("\nProceso MAIN: {} Hilo: {} levantó server en {}: {}" .format(os.getpid(), threading.current_thread().name,direccion[4][0], direccion[4][1]),"green"))
        threading.Thread(target=abrir_socket_procesos, args=(direccion,)).start()   #? Lanzo un hilo para sokcet IPv4 y otro para IPv6



#? Correr con python3 server.py -p 1234
#? Ver procesos que estan utilizando el puerto 1234: sudo lsof -i:1234
#? Ver procesos htop o ps






