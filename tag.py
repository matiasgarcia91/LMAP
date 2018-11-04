 #!/usr/bin/env python
import socket, sys, random, json

'''
TCP_IP = '0.0.0.0'
TCP_PORT = 3001
BUFFER_SIZE = 10000
MESSAGE = "Hello, World!"
ID = random.randint(0, 2**96 - 1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
initialized = False
'''

BUFFER_SIZE = 10000

class LmapTag:

    def __init__(self):
        json_data = open("initial_keys.json").read()
        self.db = json.loads(json_data)
        self.db['IDS'] = random.randint(0, 2**96 - 1)
        self.ID = random.randint(0, 2**96-1)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(5)
        self.s.bind(("127.0.0.1", 3001))
        self.listeners = []
        print(self.ID)

    def receive(self):
        msg, addr = self.s.recvfrom(BUFFER_SIZE)
        if(msg.decode() == "listener"):
            self.listeners.append(addr)
            return self.receive()
        msg = msg.decode()
        return msg
        
    def sendMsg(self, msg):
        for addr in self.listeners:
            self.s.sendto(msg.encode(), addr)

    def verifyABC(self, abc):
        A = abc['A']
        C = abc['C']
        IDS = self.db['IDS']
        k1 = self.db['k1']
        k2 = self.db['k2']
        k3 = self.db['k3']
        n1 = A ^ k1 ^ IDS
        B2 = ((IDS | k2) + n1 ) % 2**96
        if B2 == abc['B']:
            print('Reader authenticated')
        else:
            print('auth failed')
        n2 = (((C - IDS) % 2**96) - k3) % 2**96
        self.db['n1'] = n1
        self.db['n2'] = n2
        D = ((IDS + self.ID) % 2**96) ^ n1 ^ n2
        print('verifyready')
        print(self.db)
        return D

    def update_values(self):
        IDS = self.db['IDS']
        print('updatedstarted')
        k1 = self.db['k1']
        k2 = self.db['k2']
        k3 = self.db['k3']
        k4 = self.db['k4']
        n1 = self.db['n1']
        n2 = self.db['n2']
        print('updatedadasd')
        newIDS = ((IDS + (n2 ^ k4)) % 2**96) ^ self.ID
        newk1 = k1 ^ n2 ^ ((k3 + self.ID) % 2**96)
        newk2 = k2 ^ n2 ^ ((k4 + self.ID) % 2**96)
        newk3 = ((k3 ^ n1) + (k1 ^ self.ID)) % 2**96
        newk4 = ((k4 ^ n1) + (k2 ^ self.ID)) % 2**96
        self.db = { 'k1': newk1, 'k2': newk2, 'k3': newk3, 'k4': newk4, 'IDS': newIDS }

    def run(self):
            while True:
                try:
                    msg = self.receive()
                    if(msg == "hello"):
                        # Send IDS
                        IDS = json.dumps({ 'IDS': self.db['IDS'] })
                        print(bin(self.db["IDS"]))
                        self.sendMsg(IDS)

                        # Expect A, B, C
                        data = self.receive()
                        abc = json.loads(data)
                        
                        # Calculate B' and check it B == B'
                        # Calculate and send D
                        D = self.verifyABC(abc)
                        if not D:
                            print('ABC invalid')
                            continue
                        dsend = json.dumps({ 'D': D })
                        self.sendMsg(dsend)

                        # Calculate new IDS, Ks 1-4,
                        self.update_values()
                except Exception as e:
                    print(e)
                    continue
                    


    # A = IDS XOR K1 XOR n1 now the tag knows n1
    # B = (IDS OR K2) + n1 reader authentication
    # C = IDS + K3 + n2 the tag knows n2

tag = LmapTag()
tag.run()