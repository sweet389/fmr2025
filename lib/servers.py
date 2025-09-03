import socket

class TCP:
    def __init__(self, ip='', port=23, bufsize=1023):
        self.ip=ip
        self.port=port
        self.bufsize=bufsize
        self.init()

    def init(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip,self.port))
        self.s.listen(1)
        print(f"[*] Listening on {self.ip}:{self.port}")
        self.conn, self.addr=self.s.accept()
        print(f"[*] Connected on: {self.addr}")        

    def recive(self):
        data=self.addr.recv(self.bufsize)
        print(f"[*] Data Recived {data.decode()}")
        data_deco=data.decode()
        return data_deco

    def send(self,data):
        self.addr.send(data.encode())
    
    def close(self):
        self.s.close()
        print("[*] Socket Closed")
    
    def sendall(self,data):
        self.addr.sendall(data.encode())
        
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
