import socket
import sys
from operator import xor
from bitarray import bitarray

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 10010)
sock.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % sock.getsockname()
sock.listen(1)

TAG_IDS = bitarray(96)
TAG_IDS.setall(1);
k1 = bitarray(96);
k2 = bitarray(96);
k3 = bitarray(96);
k4 = bitarray(96);
db = { TAG_IDS.to01(): { "k1": k1, "k2": k2, "k3": k3, "k4": k4 } }

def calculateABC(IDS):
    IDSArray = bitarray(IDS)
    keys = db[IDS]
    k1 = keys["k1"]
    k2 = keys["k2"]
    k3 = keys["k3"]
    n1 = bitarray(96);
    n2 = bitarray(96);
    A = IDSArray ^ k1 ^ n1
    B = (IDSArray | k2) + n1
    C = IDSArray + k3 + n2
    return [ A, B, C, n1, n2 ]


while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            # Expect IDS
            # Calculate A, B, C and send
            # Expect D, extract ID
            # Update IDS and Ks
            data = connection.recv(96)
            todo = calculateABC(data)
            print >>sys.stderr, 'received "%s"' % todo[0]
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()

# A = IDS XOR K1 XOR n1 now the tag knows n1
# B = (IDS OR K2) + n1 reader authentication
# C = IDS + K3 + n2 the tag knows n2
