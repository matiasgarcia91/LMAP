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

    def carry(self,a,b,c):
        return (a & b) | ((a | b) & c)

    def get_bits(self, index, it):
        
        aux = self.seen[it]

        def get(name, round_dif=0, offset=0):
            return self.seen[it+round_dif][name][index + offset] 

        aux["n1"][index] = get("B") ^ get("IDS") ^ self.c["B"][it][index]
        aux["K1"][index] = get("A") ^ get("n1") ^ get("IDS")
        aux["K4"][index] = get("IDS", 1) ^ get("D") ^ get("n1") ^ self.c["IDS+1"][it][index]
        n22 = get("IDS",1) ^ get("C",1) ^ get("C") ^ get("D") ^ get("K1") ^ self.c["C/1"][it][index] ^ self.c["C/2"][it][index] ^ self.c["D"][it][index] ^ self.c["C+1/1"][it][index] ^ self.c["C+1/2"][it][index] ^ self.c["C+1/3"][it][index]
        aux["K2"][index] = get("IDS",2) ^ get("IDS",1) ^ n22 ^ get("K4") ^ get("n1") ^ self.c["K2aux"][it][index] ^ self.c["K2aux"][it][index]
        n12 = get("B",1) ^ (get("IDS",1) | (get("K2") ^ get("K4") ^ get("D") ^ get("n1") ^ get("IDS") ^ self.c["B+1/1"][it][index] ^ self.c["D"][it][index]) ^ self.c["B+1/2"][it][index])
        self.ID[index] = get("IDS", 1) ^ get("D", 1) ^ n12 ^ n22 ^ self.c["D+1"][it][index]
        aux["K3"][index] = get("C") ^ get("n2") ^ get("IDS") ^self.c["C/1"][it][index] ^self.c["C/2"][it][index]
        aux["n2"][index] = self.ID[index] ^ get("n1") ^ get("D") ^ get("IDS") ^ self.c["D"][it][index]

        self.set_carry(index, it, n12, n22)

    def set_carry(self, index, it, n12, n22):
        def get(name, round_dif=0, offset=0):
            return self.seen[it+round_dif][name][index + offset] 

        self.c["IDS+1"][it][index-1] = self.carry(get("IDS"), get("K4") ^ get("n2"), self.c["IDS+1"][it][index])
        self.c["B"][it][index-1] = self.carry(get("n1"), get("IDS") | get("K2"), self.c["B"][it][index])
        self.c["A+1"][it][index-1] = self.carry(get("K3"), self.ID[index], self.c["A+1"][it][index])
        self.c["B+1/1"][it][index-1] = self.carry(get("K4"), self.ID[index], self.c["B+1/1"][it][index])
        self.c["B+1/2"][it][index-1] = self.carry(n12, get("IDS", 1) | (get("K2") ^ get("n2") ^ get("K4") ^self.ID[index] ^self.c["B+1/1"][it][index]), self.c["B+1/2"][it][index])
        self.c["C+1/1"][it][index-1] = self.carry(get("K3") ^ get("n1"), get("K1") ^ self.ID[index], self.c["C+1/1"][it][index])
        self.c["C+1/2"][it][index-1] = self.carry(get("IDS", 1), get("K3") ^ get("n1") ^ get("K1") ^ self.ID[index] ^ self.c["C+1/1"][it][index], self.c["C+1/2"][it][index]) 
        self.c["C+1/3"][it][index-1] = self.carry(n22, get("IDS", 1) ^ get("K3") ^ get("n1") ^ get("K1") ^ self.ID[index] ^ self.c["C+1/1"][it][index] ^ self.c["C+1/2"][it][index], self.c["C+1/3"][it][index])
        self.c["D+1"][it][index-1] = self.carry(get("IDS", 1), self.ID[index], self.c["D+1"][it][index])
        self.c["C/1"][it][index-1] = self.carry(get("IDS"), get("K3"), self.c["C/1"][it][index])
        self.c["C/2"][it][index-1] = self.carry(get("n2"), get("IDS") ^ get("K3") ^ self.c["C/1"][it][index], self.c["C/2"][it][index])
        self.c["D"][it][index-1] = self.carry(get("IDS"), self.ID[index], self.c["D"][it][index])
        self.c["K2aux"][it][index-1] = self.carry(get("K4") ^ get("n1"), get("K2") ^ self.ID[index], self.c["K2aux"][it][index])
        self.c["K2/2"][it][index-1] = self.carry(get("IDS+1"), n22 ^ get("K4") ^ get("n1") ^ get("K2") ^ self.ID[index] ^ self.c["K2aux"][it][index], self.c["K2/2"][it][index])


    def reveal(self):
        for auxround in self.seen:
            auxround["K1"] = BitVector(size=96)
            auxround["K2"] = BitVector(size=96)
            auxround["K3"] = BitVector(size=96)
            auxround["K4"] = BitVector(size=96)
            auxround["n1"] = BitVector(size=96)
            auxround["n2"] = BitVector(size=96)

        print("Rounds needed: " + len(self.seen))

        return None

    def run(self):
        rounds_where_set = [None]*96
        seen = []

        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        count = 0

        current = 95
        while (current != 0):
            data = self.listen_round()
            ids = data["IDS"]
            while(ids[current] == 1):
                rounds_where_set[current] = count
                current -= 1
            count += 1
            seen.append(data)

        data = self.listen_round()
        seen.append(data)
        data = self.listen_round()
        seen.append(data)
        count+=2

        self.seen = seen
        self.where_set = rounds_where_set
        self.ID = BitVector(size=96)
        self.c = {}
        self.c["IDS+1"] = [BitVector(size=96, intVal=0)] * count
        self.c["B"] = [BitVector(size=96, intVal=0)] * count
        self.c["A+1"] = [BitVector(size=96, intVal=0)] * count
        self.c["B+1/1"] = [BitVector(size=96, intVal=0)] * count
        self.c["B+1/2"] = [BitVector(size=96, intVal=0)] * count
        self.c["C+1/1"] = [BitVector(size=96, intVal=0)] * count
        self.c["C+1/2"] = [BitVector(size=96, intVal=0)] * count
        self.c["C+1/3"] = [BitVector(size=96, intVal=0)] * count
        self.c["D+1"] = [BitVector(size=96, intVal=0)] * count
        self.c["C/1"] = [BitVector(size=96, intVal=0)] * count
        self.c["C/2"] = [BitVector(size=96, intVal=0)] * count
        self.c["D"] = [BitVector(size=96, intVal=0)] * count
        self.c["K2aux"] = [BitVector(size=96, intVal=0)] * count
        self.c["K2/2"] = [BitVector(size=96, intVal=0)] * count

        self.reveal()


    
attacker = LmapAttacker()
attacker.run()