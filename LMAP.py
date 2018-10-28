import socket
import sys
from operator import xor
import random
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10010)
sock.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % sock.getsockname()
sock.listen(1)

initialized = False

# Initial Ks and IDS should be shared between tag and reader
IDS = random.randint(0, 2**96 - 1)
k1 = random.randint(0, 2**96 - 1)
k2 = random.randint(0, 2**96 - 1)
k3 = random.randint(0, 2**96 - 1)
k4 = random.randint(0, 2**96 - 1)
db = { "k1": k1, "k2": k2, "k3": k3, "k4": k4 }

def calculateABC(IDS):
    k1 = db["k1"]
    k2 = db["k2"]
    k3 = db["k3"]
    n1 = random.randint(0, 2**96 - 1)
    n2 = random.randint(0, 2**96 - 1)
    A = IDS ^ k1 ^ n1
    B = (IDS | k2) + n1
    C = IDS + k3 + n2
    return [ A, B, C, n1, n2 ]


while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            initialized = False
            if not initialized:
                init = json.dumps({ 'IDS': IDS, 'k1': k1, 'k2': k2, 'k3': k3 })
                connection.sendall(init)
                ack = connection.recv(10000)
                if ack == 'ACK': initialized = True
                print 'initialized'
            # Expect IDS
            data = connection.recv(10000)
            ids_recieved = json.loads(data)
            print { 'IDS': ids_recieved }

            # Calculate A, B, C and send
            todo = calculateABC(int(ids_recieved['IDS']))
            print >> sys.stderr, 'calculated "%s"' % bin(todo[0])
            abc = { 'A': todo[0], 'B': todo[1], 'C': todo[2], 'n1': todo[3] }
            print abc
            abcSerial = json.dumps(abc)

            # Expect D, extract ID
            # Update IDS and Ks
            if data:
                connection.sendall(abcSerial)
            else:
                break
    except Exception as e:
        print(e)
        connection.close()
    finally:
        connection.close()

# A = IDS XOR K1 XOR n1 now the tag knows n1
# B = (IDS OR K2) + n1 reader authentication
# C = IDS + K3 + n2 the tag knows n2
