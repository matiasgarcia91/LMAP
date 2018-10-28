 #!/usr/bin/env python
import socket, sys, random, json

TCP_IP = '0.0.0.0'
TCP_PORT = 3001
BUFFER_SIZE = 10000
MESSAGE = "Hello, World!"
ID = random.randint(0, 2**96 - 1)
db = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
initialized = False


def verifyABC(abc):
    global db
    A = abc['A']
    C = abc['C']
    IDS = db['IDS']
    k1 = db['k1']
    k2 = db['k2']
    k3 = db['k3']
    n1 = A ^ k1 ^ IDS
    B2 = (IDS | k2) + n1
    if B2 == abc['B']:
        print 'Reader authenticated'
    else:
        print 'auth failed'
    n2 = C - IDS - k3
    db['n1'] = n1
    db['n2'] = n2
    D = (IDS + ID) ^ n1 ^ n2
    print 'verifyready'
    print db
    return D

def update_values():
    global db
    IDS = db['IDS']
    print 'updatedstarted'
    k1 = db['k1']
    k2 = db['k2']
    k3 = db['k3']
    k4 = db['k4']
    n1 = db['n1']
    n2 = db['n2']
    print 'updatedadasd'
    newIDS = (IDS + (n2 ^ k4)) ^ ID
    newk1 = k1 ^ n2 ^ (k3 + ID)
    newk2 = k2 ^ n2 ^ (k4 + ID)
    newk3 = (k3 ^ n1) + (k1 ^ ID)
    newk4 = (k4 ^ n1) + (k2 ^ ID)
    db = { 'k1': newk1, 'k2': newk2, 'k3': newk3, 'k4': newk4, 'IDS': newIDS }

try:
    while True:
        if not initialized:
            initData = s.recv(BUFFER_SIZE)
            db = json.loads(initData)
            s.send('ACK')
            initialized = True
        ready = raw_input("Type 'y' to begin")
        if ready == 'y':
            # Send IDS
            IDS = json.dumps({ 'IDS': db['IDS'] })
            s.sendall(IDS)

            # Expect A, B, C
            data = s.recv(BUFFER_SIZE)
            abc = json.loads(data)
            
            # Calculate B' and check it B == B'
            # Calculate and send D
            D = verifyABC(abc)
            if not D:
                print 'ABC invalid'
                break
            dsend = json.dumps({ 'D': D })
            s.sendall(dsend)

            # Calculate new IDS, Ks 1-4,
            update_values()
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
