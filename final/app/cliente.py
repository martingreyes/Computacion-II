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

alias = input("\n+ CLIENTE: ")
dato = pickle.dumps(alias)
s.send(dato)

dato = s.recv(1024)
respuesta = pickle.loads(dato)
print("\n{}".format(respuesta))

password = input("\n+ {}: ".format(alias))
dato = pickle.dumps(password)
s.send(dato)

dato = s.recv(1024)
comienzo = pickle.loads(dato)
print("\n{}".format(comienzo))

if comienzo == "- SERVER: Chau chau":
        sys.exit()   

while(True) :
    dato = s.recv(1024)
    pregunta = pickle.loads(dato)
    print("\n{}".format(pregunta))

    if pregunta == "- SERVER: Chau chau":
        sys.exit()
    
    if "Obtuviste" in pregunta:
        break   

    respuesta = input("\n+ {}: ".format(alias))
    while respuesta.lower() != "a" and respuesta.lower() != "b" and respuesta != "exit":
        respuesta = input("\n- Ingresa 'a' ó 'b': ")
    respuesta = pickle.dumps(respuesta.lower())
    s.send(respuesta)

dato = s.recv(1024)
ranking = pickle.loads(dato)
print("\n{}\n".format(ranking))

    
#? Correr con python3 cliente.py -d 127.0.0.1 -p 1234 -ip 4
#? Correr con python3 cliente.py -d ::1 -p 1234 -ip 6

