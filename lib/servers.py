import socket

class TCP:
    def __init__(self, ip='', port=23, bufsize=1024):
        self.ip = ip
        self.port = port
        self.bufsize = bufsize
        self.s = None
        self.conn = None
        self.addr = None

    def init(self):
        # fecha socket antigo se existir
        if self.s:
            self.s.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # evita EADDRINUSE
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        print(f"[*] Listening on {self.ip}:{self.port}")
        self.conn, self.addr = self.s.accept()
        print(f"[*] Connected on: {self.addr}")
        return self.conn, self.addr

    def accept(self):
        conn, addr = self.s.accept()
        return conn, addr

    def receive(self):
        if not self.conn:
            return None
        data = self.conn.recv(self.bufsize)
        print(f"[*] Data Received: {data.decode()}")
        return data.decode()

    def send(self, data):
        if self.conn:
            self.conn.send(data.encode())

    def sendall(self, data):
        if self.conn:
            self.conn.sendall(data.encode())

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        if self.s:
            self.s.close()
            self.s = None
        print("[*] Socket Closed")   
class UDP:
    def __init__(self, ip='', port=23, bufsize=1023):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((ip,port))
        self.bufsize=bufsize
        print(f"[*] UDP SERVER ON {ip}:{port}")
        
    def recive(self):
        msg,addr=self.s.recvfrom(self.bufsize)
        print(f'[*] Recived {msg.decode()} from {addr}')
        data_deco=msg.decode()
        return data_deco, addr
        
    def send(self,data,addr):
        status=self.s.sendto(data.encode(), addr)
        print(f'[*] Status {status}')
