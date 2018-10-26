 #!/usr/bin/env python
import socket, pickle
import random
import json

TCP_IP = '0.0.0.0'
TCP_PORT = 10010
BUFFER_SIZE = 10000
MESSAGE = "Hello, World!"
IDS = random.randint(0, 2**96 - 1)
ID = "secreto"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

try:
    while True:
        ready = raw_input("Type 'y' to begin")
        if ready == 'y':
            # Send IDS
            # Expect A, B, C
            # Calculate B' and check it B == B'
            # Calculate and send D
            # Calculate new IDS, Ks 1-4 ,
            print str(IDS)
            s.send(str(IDS))
            data = s.recv(BUFFER_SIZE)
            a = json.loads(data)
            print "received data:", a
except:
    s.close()
finally:
    s.close()
