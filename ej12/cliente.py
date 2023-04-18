import socket, sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = str(sys.argv[1])
port = 1234

s.connect((host,port))

while True :
    msg = input('Enter message to send : ')
    if msg.lower() == "exit":
        s.send(msg.encode('ascii'))
        s.close()
        exit()
    s.send(msg.encode('ascii'))
    data = s.recv(1024)
    print('Server reply : ' + data.decode("ascii"))
    
