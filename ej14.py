import argparse, pickle, subprocess, os, threading, socket, concurrent.futures

def handle(clientsocket):

    while True:

        sock , addr = clientsocket

        command = sock.recv(1024)
        command = pickle.loads(command)

        if args.c == "p":
            print("- {} {} : {} ({})".format(addr[0], addr[1], command, os.getpid()))
        if args.c == "t":
            print("- {} {} : {} ({}: {})".format(addr[0], addr[1], command,threading.current_thread().name, threading.get_native_id()))

        if command == "exit":
            dato = pickle.dumps("Chau chau")
            sock.sendall(dato) 
            break    
                
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  universal_newlines=True, bufsize=10000)
        salida, error = p.communicate()
            
        if salida == "":
            dato =  {"ERROR" :error} 
            dato = pickle.dumps(dato)
            sock.sendall(dato)
            
        if error == "":
            dato =  {"OK" :salida} 
            dato = pickle.dumps(dato)
            sock.sendall(dato)
        

parser = argparse.ArgumentParser()
parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
parser.add_argument("-c",type=str, help= "modo de concurrencia")
args = parser.parse_args()

puerto = args.p
concurrencia = args.c
address = ("localhost", puerto)

    
if concurrencia.lower() == "p":
    print("\nProceso padre ", os.getpid(), "\n")
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    
if concurrencia.lower() == "t":
    print("\n", threading.current_thread().name, threading.get_native_id(), "\n")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM,) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(5)
    while True:
        clientsocket = server.accept()
        executor.submit(handle,clientsocket)
          
   

#? Correr con p ej14.py -p 1234 -c t

#! NO ANDA CON p ej14.py -p 1234 -c p


