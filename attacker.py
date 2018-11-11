 #!/usr/bin/env python
import socket, json
from BitVector import BitVector

class LmapAttacker:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 3002))
        self.socket.settimeout(5)        
        self.rounds = 0

    def receive(self):
        data, _ = self.socket.recvfrom(10000)
        return data.decode()


    def listen_round(self):
        temp_dict = {}
        db = {}
        while True:
            aux = self.receive()
            if(aux == "hello"):
                msg = self.receive()
                temp_dict = json.loads(msg)
                msg = self.receive()
                temp_dict.update(json.loads(msg))
                msg = self.receive()
                temp_dict.update(json.loads(msg))

                for message, value in temp_dict:
                    db[message] = BitVector(size=96, intVal=value)
                return db

    def get_bits(self, seen, index, it, carry, ID):
        aux = seen[it]
        aux["n1"][index] = aux["B"][index] ^ 1
        aux["K1"][index] = aux["A"][index] ^ aux["n1"][index] ^ 1
        aux["K4"][index] = seen[it+1]["IDS"][index] ^ aux["D"][index] ^ aux["n1"][index] 
        n22 = seen[it+1]["IDS"][index] ^ seen[it+1]["C"][index] ^ aux["C"][index] ^ aux["D"][index] ^ aux["K1"][index] 
        aux["K2"][index] = seen[it+2]["IDS"][index] ^ seen[it+1]["IDS"][index] ^ n22 ^ aux["K4"][index] ^ aux["n1"][index]
        n12 = aux["B"][index] ^ (seen[it+1]["IDS"][index] | (aux["K2"][index] ^ aux["K4"][index] ^ aux["D"][index] ^ aux["n1"][index]))
        ID[index] = seen[it+1]["IDS"][index] ^ seen[it+1]["D"][index] ^ n12 ^ n22
        aux["K3"][index] = aux["C"][index] ^ aux["n2"][index] ^ 1
        aux["n2"][index] = ID[index] ^ aux["n1"][index] ^ aux["D"][index] ^ 1




    def reveal(self, seen, where_set):
        ID = BitVector(size=96)
        for auxround in seen:
            auxround["K1"] = BitVector(size=96)
            auxround["K2"] = BitVector(size=96)
            auxround["K3"] = BitVector(size=96)
            auxround["K4"] = BitVector(size=96)
            auxround["n1"] = BitVector(size=96)
            auxround["n2"] = BitVector(size=96)

        print("Rounds needed: " + len(seen))



        return None

    def run(self):
        bitsSet = BitVector(size = 96)
        rounds_where_set = [None]*96
        seen = []

        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        count = 0

        while (bitsSet.int_val() != 2**96-1):
            #try:
                data = self.listen_round()
                for i in range(0,96):
                    if(data["IDS"][i] == 1):
                        bitsSet[i] = 1
                        rounds_where_set[i] = count
                seen.append(data)
                count+=1

        data = self.listen_round()
        seen.append(data)
        data = self.listen_round()
        seen.append(data)
        count+=2


    
attacker = LmapAttacker()
attacker.run()