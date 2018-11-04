 #!/usr/bin/env python
import socket, json, BitVector

class LmapAttacker:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 3002))
        self.seen = []
        self.bitsSet = [False]*96

    def run(self):
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))

        while True:
            data, _ = self.socket.recvfrom(10000)
            print(data.decode())
    
attacker = LmapAttacker()
attacker.run()