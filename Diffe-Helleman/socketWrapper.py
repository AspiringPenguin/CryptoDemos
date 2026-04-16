import socket

#From https://docs.python.org/3/howto/sockets.html, with some tweaks
class SocketWrapper:
    def __init__(self, msgLEN : int, sock : socket.socket | None = None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.msgLEN = msgLEN

    def connect(self, host : str, port : int):
        self.sock.connect((host, port))

    def send(self, _msg : str):
        msg = _msg.encode().rjust(self.msgLEN, b"\0")
        totalsent = 0
        while totalsent < self.msgLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self) -> str:
        chunks = list[bytes]()
        bytes_recd = 0
        while bytes_recd < self.msgLEN:
            chunk = self.sock.recv(min(self.msgLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks).decode().replace("\0", "")

    def close(self):
        self.sock.close()