import socket, pickle, argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True, help="direccion")
    parser.add_argument("-p", type=int, required=True, help="puerto")
    args = parser.parse_args()
    direccion = args.d
    puerto = args.p

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((direccion, puerto))    
    print("\nConnected to " + direccion + ":" + str(puerto))


    while True:
        msg1 = input("\nIntroduzca comando: ")
        msg1 = pickle.dumps(msg1)       #De normal a bits
        s.send(msg1)

        msg2 = s.recv(10000)
        msg2 = pickle.loads(msg2)       #De bits a normal

        if msg2 == "Chau chau":
            s.close()
            exit()

        print("\n+ {}".format(msg2))


if __name__ == '__main__':
    main()


#? Correr con: p cliente.py -d 127.0.0.1 -p 8888