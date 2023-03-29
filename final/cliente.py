import socket, sys, argparse, pickle

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "dirección IP o nombre del servidor al que conectarse")
parser.add_argument("-p", default=1234, type=int, help= "puerto donde va atender el servidor")
parser.add_argument("-ip", required=True, help="IPv4 (4) o IPv6 (6)", choices=["4", "6"], type=str)
args = parser.parse_args()

host = args.d
puerto = args.p

if args.ip == "4":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

elif args.ip == "6":
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)


s.connect((host,puerto))

dato = s.recv(1024)
bienvenida = pickle.loads(dato)
print("\n{}".format(bienvenida))

alias = input("\n+ ")
dato = pickle.dumps(alias)
s.send(dato)

dato = s.recv(1024)
respuesta = pickle.loads(dato)
print("\n{}".format(respuesta))

password = input("\n+ ")
dato = pickle.dumps(password)
s.send(dato)

dato = s.recv(1024)
comienzo = pickle.loads(dato)
print("\n{}".format(comienzo))

while(True) :
    print("pepeeeee")
    msg = s.recv(1024)
    msg = pickle.loads(msg)
    print("\n{}".format(msg))

    if msg == "- Chau chau":
        break   

    respuesta = input("\n+ ")
    respuesta = pickle.dumps(respuesta)
    s.send(respuesta)
    
#? Correr con p cliente.py -d 127.0.0.1 -p 1234 -ip 4
#? Correr con p cliente.py -d ::1 -p 1234 -ip 6