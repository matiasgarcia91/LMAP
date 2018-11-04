import socket, sys, random, json, time


BUFFER_SIZE = 10000
'''
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('', 3001)
sock.bind(server_address)
print >>sys.stderr, 'starting up on %s port %s' % sock.getsockname()
sock.listen(1)

initialized = False

# Initial Ks and IDS should be shared between tag and reader
IDS_init = random.randint(0, 2**96 - 1)
k1 = random.randint(0, 2**96 - 1)
k2 = random.randint(0, 2**96 - 1)
k3 = random.randint(0, 2**96 - 1)
k4 = random.randint(0, 2**96 - 1)
db = { "k1": k1, "k2": k2, "k3": k3, "k4": k4 }
'''

class LmapReader:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 3000))
        json_data = open("initial_keys.json").read()
        self.db = json.loads(json_data)
        self.listeners = [("127.0.0.1", 3001),]


    def sendMsg(self, msg):
        for addr in self.listeners:
            self.socket.sendto(msg.encode(), addr)

    def receive(self):
        msg, addr = self.socket.recvfrom(BUFFER_SIZE)
        if(msg.decode() == "listener"):
            self.listeners.append(addr)
            return self.receive()
        msg = msg.decode()
        return msg

    def calculateABC(self, IDS):
        k1 = self.db["k1"]
        k2 = self.db["k2"]
        k3 = self.db["k3"]
        n1 = random.randint(0, 2**96 - 1)
        n2 = random.randint(0, 2**96 - 1)
        self.db['IDS'] = IDS
        self.db['n1'] = n1
        self.db['n2'] = n2
        print(self.db)
        A = IDS ^ k1 ^ n1
        B = ((IDS | k2) + n1) % 2**96 
        C = ((IDS + k3) % 2**96) + n2
        C = C % 2**96
        return [ A, B, C, n1, n2 ]

    def decodeD(self, D):
        n1 = self.db['n1']
        n2 = self.db['n2']
        IDS = self.db['IDS']
        ID = ((D ^ n1 ^ n2) - IDS) % 2**96
        return ID

    def update_values(self, ID):
        IDS = self.db['IDS']
        k1 = self.db['k1']
        k2 = self.db['k2']
        k3 = self.db['k3']
        k4 = self.db['k4']
        n1 = self.db['n1']
        n2 = self.db['n2']
        newIDS = (IDS + ((n2 ^ k4) % 2**96)) ^ ID
        newk1 = k1 ^ n2 ^ ((k3 + ID) % 2**96)
        newk2 = k2 ^ n2 ^ ((k4 + ID) % 2**96)
        newk3 = ((k3 ^ n1) + (k1 ^ ID)) % 2**96
        newk4 = ((k4 ^ n1) + (k2 ^ ID)) % 2**96
        self.db = { 'k1': newk1, 'k2': newk2, 'k3': newk3, 'k4': newk4, 'IDS': newIDS }
        print(ID)

    def run(self):
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        while True:
            '''
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = sock.accept()
            '''
            try:
                self.sendMsg("hello")
                '''
                print >>sys.stderr, 'client connected:', client_address
                initialized = False
                '''
                # Send initial IDS and Ks to tag - not part of the protocol but needed to share the
                # same initial values between entities
                '''
                if not initialized:
                    init = json.dumps({ 'IDS': IDS_init, 'k1': k1, 'k2': k2, 'k3': k3, 'k4': k4 })
                    connection.sendall(init)
                    ack = connection.recv(10000)
                    if ack == 'ACK': initialized = True
                    print('initialized')
                '''
                # Expect IDS
                data = self.receive()
                print(data)
                ids_recieved = json.loads(data)

                # Calculate A, B, C and send
                todo = self.calculateABC(int(ids_recieved['IDS']))
                abc = { 'A': todo[0], 'B': todo[1], 'C': todo[2] }
                abcSerial = json.dumps(abc)
                self.sendMsg(abcSerial)

                # Expect D, extract ID
                authreplyraw = self.receive()
                authreply = json.loads(authreplyraw)
                ID = self.decodeD(authreply['D'])
                # Update IDS and Ks 1-4
                self.update_values(ID)
                
                time.sleep(1.5)
            except Exception as e:
                print(e)
                continue

    # A = IDS XOR K1 XOR n1 now the tag knows n1
    # B = (IDS OR K2) + n1 reader authentication
    # C = IDS + K3 + n2 the tag knows n2

reader = LmapReader()
reader.run()