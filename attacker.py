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

    def carry(a,b,c):
        return (a & b) | ((a | b) & c)

    def get_bits(self, index, it, carry):
        
        aux = seen[it]

        def get(name, round_dif=0, offset=0):
            return self.seen[it+round_dif][name][index + offset] 

        aux["n1"][index] = get("B") ^ get("IDS")
        aux["K1"][index] = get("A") ^ get("n1") ^ get("IDS")
        aux["K4"][index] = get("IDS", 1) ^ get("D") ^ get("n1") 
        n22 = get("IDS",1) ^ get("C",1) ^ get("C") ^ get("D") ^ get("K1") 
        aux["K2"][index] = get("IDS",2) ^ get("IDS",1) ^ n22 ^ get("K4") ^ get("n1")
        n12 = get("B") ^ (get("IDS",1) | (get("K2") ^ get("K4") ^ get("D") ^ get("n1")))
        ID[index] = get("IDS", 1) ^ get("IDS", 1) ^ n12 ^ n22
        aux["K3"][index] = get("C") ^ get("n2") ^ get("IDS")
        aux["n2"][index] = ID[index] ^ get("n1") ^ get("D") ^ get("IDS")



    def reveal(self, seen, where_set):
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

        self.seen = seen
        self.where_set = where_set
        self.ID = BitVector(size=96)


    
attacker = LmapAttacker()
attacker.run()