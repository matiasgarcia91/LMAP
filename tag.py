 #!/usr/bin/env python
import socket
from bitarray import bitarray

TCP_IP = '0.0.0.0'
TCP_PORT = 10010
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
IDS = bitarray(96)
IDS.setall(1);
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
        s.send(IDS.to01())
        data = s.recv(BUFFER_SIZE)
        print "received data:", data


s.close()
