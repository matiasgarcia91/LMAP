 #!/usr/bin/env python
import socket, json, sys
from BitVector import BitVector
from approximations import calculate_approximations

class tangoAttacker:

    def __init__(self, IDtodecode):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 3002))
        self.socket.settimeout(5)
        self.round_aproximations = []
        self.rounds = 0
        self.ID = BitVector(size = 96, intVal=int(IDtodecode))

    def receive(self):
        data, _ = self.socket.recvfrom(10000)
        return data.decode()

    def attack(self, ids):
        db_tmp = {}
        db_tmp["IDS"] = ids["IDS"]
        ids = BitVector(size=96, intVal=ids["IDS"])
        aux = self.receive()
        db_tmp.update(json.loads(aux))
        aux = self.receive()
        db_tmp.update(json.loads(aux))

        db = {}
        for message, value in db_tmp.items():
            db[message] = BitVector(size=96, intVal=value)
        current_approx = calculate_approximations(db, self.ID)
        self.round_aproximations.append(current_approx)



    def run(self):
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3000))
        self.socket.sendto("listener".encode(), ("127.0.0.1", 3001))
        count = 0
        while True:
            #try:
                self.rounds += 1
                data = self.receive()
                if(data == "hello"):
                    ids= self.receive()
                    ids_json = json.loads(ids)
                    print("attack")
                    self.attack(ids_json)

                '''except Exception as e:
                    print("shit")
                    continue
                '''


IDtodecode = sys.argv[1]
attacker = tangoAttacker(IDtodecode)
attacker.run()
