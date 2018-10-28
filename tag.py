 #!/usr/bin/env python
import socket, sys
import random
import json

TCP_IP = '0.0.0.0'
TCP_PORT = 10010
BUFFER_SIZE = 10000
MESSAGE = "Hello, World!"
ID = random.randint(0, 2**96 - 1)
init = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
initialized = False


def verifyABC(abc):
    A = abc['A']
    C = abc['C']
    IDS = init['IDS']
    k1 = init['k1']
    k2 = init['k2']
    k3 = init['k3']
    n1 = A ^ k1 ^ IDS
    B2 = (IDS | k2) + n1
    if B2 == abc['B']:
        print 'Reader authenticated'
    else:
        print 'auth failed'
    n2 = C - IDS - k3
    init['n1'] = n1
    init['n2'] = n2
    D = (IDS + ID) ^ n1 ^ n2
    return D



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
            abc = json.loads(data)
            print "received data:", abc
            # Calculate B' and check it B == B'
            # Calculate and send D
            D = verifyABC(abc)
            if not D:
                print 'ABC invalid'
                break
            dsend = json.dumps({ 'D': D })
            s.sendall(dsend)
            print { 'ID': ID }

            # Calculate new IDS, Ks 1-4,
except Exception as e:
    print(e)
    s.close()
    initialized = False
finally:
    s.close()
    initialized = False


# A = IDS XOR K1 XOR n1 now the tag knows n1
# B = (IDS OR K2) + n1 reader authentication
# C = IDS + K3 + n2 the tag knows n2
