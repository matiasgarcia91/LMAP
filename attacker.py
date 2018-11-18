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

                for message, value in temp_dict.items():
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

        self.seen[it+1]["n1"][index] = n12
        self.seen[it+1]["n2"][index] = n22

        self.set_carry(index, it)

    def set_carry(self, index, it):
        def get(name, round_dif=0, offset=0):
            return self.seen[it+round_dif][name][index + offset] 

        self.c["IDS+1"][it][index-1] = self.carry(get("IDS"), get("K4") ^ get("n2"), self.c["IDS+1"][it][index])
        self.c["B"][it][index-1] = self.carry(get("n1"), get("IDS") | get("K2"), self.c["B"][it][index])
        self.c["A+1"][it][index-1] = self.carry(get("K3"), self.ID[index], self.c["A+1"][it][index])
        self.c["B+1/1"][it][index-1] = self.carry(get("K4"), self.ID[index], self.c["B+1/1"][it][index])
        self.c["B+1/2"][it][index-1] = self.carry(get("n1",1), get("IDS", 1) | (get("K2") ^ get("n2") ^ get("K4") ^self.ID[index] ^self.c["B+1/1"][it][index]), self.c["B+1/2"][it][index])
        self.c["C+1/1"][it][index-1] = self.carry(get("K3") ^ get("n1"), get("K1") ^ self.ID[index], self.c["C+1/1"][it][index])
        self.c["C+1/2"][it][index-1] = self.carry(get("IDS", 1), get("K3") ^ get("n1") ^ get("K1") ^ self.ID[index] ^ self.c["C+1/1"][it][index], self.c["C+1/2"][it][index]) 
        self.c["C+1/3"][it][index-1] = self.carry(get("n2",1), get("IDS", 1) ^ get("K3") ^ get("n1") ^ get("K1") ^ self.ID[index] ^ self.c["C+1/1"][it][index] ^ self.c["C+1/2"][it][index], self.c["C+1/3"][it][index])
        self.c["D+1"][it][index-1] = self.carry(get("IDS", 1), self.ID[index], self.c["D+1"][it][index])
        self.c["C/1"][it][index-1] = self.carry(get("IDS"), get("K3"), self.c["C/1"][it][index])
        self.c["C/2"][it][index-1] = self.carry(get("n2"), get("IDS") ^ get("K3") ^ self.c["C/1"][it][index], self.c["C/2"][it][index])
        self.c["D"][it][index-1] = self.carry(get("IDS"), self.ID[index], self.c["D"][it][index])
        self.c["K2aux"][it][index-1] = self.carry(get("K4") ^ get("n1"), get("K2") ^ self.ID[index], self.c["K2aux"][it][index])
        self.c["K2/2"][it][index-1] = self.carry(get("IDS",1), get("n2", 1) ^ get("K4") ^ get("n1") ^ get("K2") ^ self.ID[index] ^ self.c["K2aux"][it][index], self.c["K2/2"][it][index])

    
    def carry_of_round(self, limit, it):
        index = 0
        while (index<limit):
            self.set_carry(index, it)
            index+=1

    
    def update_bits(self, index, it):

        k1 = self.seen[it]["K1"].int_val() ^ self.seen[it]["n2"].int_val() ^ (self.seen[it]["K3"].int_val() + self.ID.int_val())
        k2 = self.seen[it]["K2"].int_val() ^ self.seen[it]["n2"].int_val() ^ (self.seen[it]["K4"].int_val() + self.ID.int_val())
        k3 = self.seen[it]["K3"].int_val() ^ self.seen[it]["n1"].int_val() ^ (self.seen[it]["K1"].int_val() + self.ID.int_val())
        k4 = self.seen[it]["K4"].int_val() ^ self.seen[it]["n1"].int_val() ^ (self.seen[it]["K2"].int_val() + self.ID.int_val())

        auxVal = 2**(95-index)
        self.seen[it+1]["K1"] = BitVector(size=96, intVal = k1 % auxVal)
        self.seen[it+1]["K2"] = BitVector(size=96, intVal = k2 % auxVal)
        self.seen[it+1]["K3"] = BitVector(size=96, intVal = k3 % auxVal)
        self.seen[it+1]["K4"] = BitVector(size=96, intVal = k4 % auxVal) 

        n12 = self.seen[it+1]["IDS"].int_val() ^ self.seen[it+1]["A"].int_val() ^ self.seen[it+1]["K1"].int_val()
        self.seen[it+1]["n1"] = BitVector(size=96, intVal = n12 % auxVal) 

        aux = (self.seen[it+1]["IDS"].int_val() + self.ID.int_val()) ^ n12 ^ self.seen[it+1]["D"].int_val()
        self.seen[it+1]["n2"] = BitVector(size=96, intVal=aux%auxVal)


    def reveal(self):
        for auxround in self.seen:
            auxround["K1"] = BitVector(size=96)
            auxround["K2"] = BitVector(size=96)
            auxround["K3"] = BitVector(size=96)
            auxround["K4"] = BitVector(size=96)
            auxround["n1"] = BitVector(size=96)
            auxround["n2"] = BitVector(size=96)

        current = 95
        while(current >= 0):
            
            it = self.where_set[current]
            print(str(current) + "," + str(it))
            if(current < 95):
                self.carry_of_round(current, it)
            self.get_bits(current, it)
            current = current - 1
            while(self.where_set[current] == it):
                self.get_bits(current, it)
                current = current - 1
            it2 = it
            while(it2 <= len(self.seen)):
                self.update_bits(current+1, it)
                it2 += 1
        


        print("Rounds needed: " , len(self.seen))
        print(self.ID)

        return None

    def run(self):
        rounds_where_set = [None]*96
        seen = []

        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        count = 0

        current = 95
        while (current >= 0):
            data = self.listen_round()
            ids = data["IDS"]
            while(ids[current] == 1 and current>=0):
                rounds_where_set[current] = count
                current -= 1
                print(current)
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


print("A")
attacker = LmapAttacker()
attacker.run()