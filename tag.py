 #!/usr/bin/env python
import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 10010
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
ID = "secreto"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    ready = raw_input("Type 'y' to begin")
    if ready == 'y':
        # Send IDS
        # Expect A, B, C
        # Calculate B' and check it B == B'
        # Calculate and send D
        # Calculate new IDS, Ks 1-4 ,
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        print "received data:", data


s.close()
