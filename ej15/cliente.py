import socket, sys, argparse, pickle

parser = argparse.ArgumentParser()
parser.add_argument("-d", help= "dirección IP o nombre del servidor al que conectarse")
parser.add_argument("-p", type=int, help= "puerto donde va atender el servidor")
parser.add_argument("-ip", required=True, help="IPv4 (4) o IPv6 (6)", choices=["4", "6"], type=str)
args = parser.parse_args()

host = args.d
puerto = args.p

if args.ip == "4":
    print("\nIPv4\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

elif args.ip == "6":
    print("\nIPv6\n")
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)


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

#? Correr con p cliente.py -d 127.0.0.1 -p 1234 -ip 4
#? Correr con p cliente.py -d 127.0.0.1 -p 1234 -ip 6
