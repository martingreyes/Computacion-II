import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                           
host = ""
port = 1234

serversocket.bind((host, port))                                  

serversocket.listen(1)

clientsocket, addr = serversocket.accept()

while True:
    data = clientsocket.recv(1024)
    print("Address: %s " % str(addr))
    print( "Recibido: "+ data.decode("ascii"))
    msg = data.decode().upper()
    clientsocket.send(msg.encode('ascii'))

# Tengo que ejecutar primero este archivo
# Para conectarme a este server tengo que hacer: telnet 127.0.0.1 1234 o telnet 127.0.0.1 1234 o 192.168.1.38