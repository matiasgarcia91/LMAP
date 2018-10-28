 #!/usr/bin/env python
import socket, sys
import random
import json

TCP_IP = '0.0.0.0'
TCP_PORT = 10010
BUFFER_SIZE = 10000
MESSAGE = "Hello, World!"
ID = "secreto"
init = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
initialized = False

try:
    while True:
        if not initialized:
            initData = s.recv(BUFFER_SIZE)
            init = json.loads(initData)
            s.send('ACK')
            initialized = True
        ready = raw_input("Type 'y' to begin")
        if ready == 'y':
            # Send IDS
            IDS = json.dumps({ 'IDS': init['IDS'] })
            s.sendall(IDS)

            # Expect A, B, C
            data = s.recv(BUFFER_SIZE)
            a = json.loads(data)
            print "received data:", a

            # Calculate B' and check it B == B'
            # Calculate and send D
            # Calculate new IDS, Ks 1-4,
except Exception as e:
    print(e)
    s.close()
    initialized = False
finally:
    s.close()
    initialized = False
