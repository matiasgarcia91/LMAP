 #!/usr/bin/env python
import socket, json
from BitVector import BitVector

class LmapAttacker:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 3002))
        self.socket.settimeout(5)
        self.seen = []
        self.bitsSet = BitVector(size = 96)
        self.rounds = 0

    def receive(self):
        data, _ = self.socket.recvfrom(10000)
        return data.decode()

    def attack(self, ids):
        db_tmp = {}
        db_tmp["IDS"] = ids["IDS"]
        ids = BitVector(size=96, intVal=ids["IDS"])
        for i in range(0,96):
            if(ids[i] == 1):
                self.bitsSet[i] = 1
        aux = self.receive()
        db_tmp.update(json.loads(aux))
        aux = self.receive()
        db_tmp.update(json.loads(aux))

        db = {}
        for message, value in db_tmp.items():
            db[message] = BitVector(size=96, intVal=value)
        self.seen.append(db)

        while(self.bitsSet.int_val() != 2**96-1):
            self.rounds = self.rounds + 1
            aux = self.receive()
            aux = self.receive()
            db = {}
            db["IDS"] = json.loads(aux)["IDS"]
            aux = self.receive()
            db.update(json.loads(aux))
            aux = self.receive()
            db.update(json.loads(aux))
            for message, value in db.items():
                db[message] = BitVector(size=96, intVal=db[message])
            self.seen.append(db)
            for i in range(0,96):
                if(db["IDS"][i] == 1):
                    self.bitsSet[i] = 1
            print(db)
        
        self.reveal()


    def reveal(self):
        print("Rounds needed: " + self.rounds)
        return None

    def run(self):
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        count = 0
        while True:
            #try:
                data = self.receive()
                if(data == "hello"):
                    ids= self.receive()
                    ids_json = json.loads(ids)
                    if(ids_json["IDS"] % 2 == 1):
                        print("attack")
                        self.attack(ids_json)
                        break

                '''except Exception as e:
                    print("shit")
                    continue
                '''

    
attacker = LmapAttacker()
attacker.run()