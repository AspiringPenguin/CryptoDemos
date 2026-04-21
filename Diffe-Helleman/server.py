from random import randint
import socket
from socketWrapper import SocketWrapper

prime = 2134879 #For the modulus
g = 6 #The base, a primitive root in Z{prime}
msgLEN = 16384

class Server:
    port : int
    a : int
    keyTable = list[int]()
    idNum = -1 #Is incremented before use

    def __init__(self, port : int):
        self.port = port
        self.a = randint(2, prime - 2)
    
    def connectNew(self):
        self.idNum += 1
        return f"""id {self.idNum}
p {prime}
g {g}
c {(g ** self.a) % prime}"""

    def handleSocket(self, clientSocket : socket.socket):
        sock = SocketWrapper(msgLEN, sock = clientSocket)

        msg = sock.receive()

        #Handle new unencrypted connections
        if msg == "new":
            sock.send(self.connectNew())

            print(f"Got a new client. ID {self.idNum}")

            dContainer = sock.receive()

            sock.close()

            d = int(dContainer.split(" ")[-1])

            self.keyTable.append(pow(d, self.a, prime))

            print("Finished handshake.")

            return

        #Grab the id and encrypted message, pass them on
        if msg.startswith("id"):
            sock.close()
            lines = msg.split("\n")
            self.handleEncrypted(int(lines[0][2:].strip()), "\n".join(lines[1:]))

    def handleEncrypted(self, _id:int, message : str):
        print(f"New message from id {_id}.")

        decrypted = ""
        n = 10
        
        for char in message:
            num = ord(char) - ((pow(n, self.keyTable[_id], prime))) % 256
            if (num < 0): num += 256
            decrypted += chr(num)
            n += 1

        print(decrypted)

    def mainloop(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Bind socket
        serversocket.bind(("localhost", self.port))
        
        # become a server socket
        serversocket.listen(1)

        while True:
            (clientSocket, _) = serversocket.accept()

            self.handleSocket(clientSocket)