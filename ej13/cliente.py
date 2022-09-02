import socket, sys, argparse, pickle

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "dirección IP o nombre del servidor al que conectarse")
parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
args = parser.parse_args()

host = args.d
puerto = args.p

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,puerto))

while(True) :
    command = input('+ Enter a command to send : ')
    command = pickle.dumps(command)
    s.send(command)
    
    # receive data from client (data, addr)
    msg = s.recv(1024)
    msg = pickle.loads(msg)
    print("- {}".format(msg))

    if msg == "Chau chau":
        break

#? Correr con p cliente.py -d 127.0.0.1 -p 1234