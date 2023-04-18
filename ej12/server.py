import socket, sys, threading, os

def hilo(cliente):
    while True:
        data = cliente.recv(1024).decode("ascii")
        if data.lower() == "exit":
            print(addr, " saliendo")
            break
            sock.close()
        print("{} from {} hilo: {} {}".format(data, str(addr), threading.get_native_id()))
        msg = data.upper().encode("ascii")
        cliente.send(msg)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                           
host = ""
port = 1234

serversocket.bind((host, port))                                  

serversocket.listen(5)

print("Server {} {} ID: {} \n".format(host, port, threading.get_native_id()))


while True:
    clientesocket, addr = serversocket.accept()
    print("\n", str(addr), " connected")
    threading.Thread(target=hilo, args=(clientesocket,)).start()
    


