from random import randint
from socketWrapper import SocketWrapper

msgLEN = 16384

class Client:
    port : int
    prime: int
    root : int
    b: int
    secureKey : int
    _id : int

    def __init__(self, port : int):
        self.port = port

    def getSecureCode(self):
        s = SocketWrapper(msgLEN)

        s.connect("localhost", self.port)

        s.send("new")

        print("Sent connection message to server.")

        msg = s.receive()
        lines = msg.split("\n")

        self._id = int(lines[0].split(" ")[-1])
        self.prime = int(lines[1].split(" ")[-1])
        self.root = int(lines[2].split(" ")[-1])

        #Generate a b
        self.b = randint(2, self.prime - 2)

        c = int(lines[3].split(" ")[-1])
        self.secureKey = (c ** self.b) % self.prime

        print("Received server response")

        #Send back d
        s.send(f"d {(self.root ** self.b) % self.prime}")

        s.close()

        print("Finished handshake")

    def mainloop(self):
        inp = input("> ")

        print(inp)