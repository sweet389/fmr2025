from lib.servers import TCP
from lib.wifi import wifi
import os
import json

default_html="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Esp32</title>
</head>
<body>
    <h1 style="text-align: center;">Http Server on Esp32</h1>
    <br>
    <h2>To create your pages just create a folder like this:</h2>
    <div style="font-size: 160%; line-height: 30px; font-weight: 600;">
        <ul style="list-style-type: none;">
            <li>html/</li>
            <ul style="list-style-type: none;">
                <li>css/ <ul style="list-style-type: none;"><li>style.css</li></ul></li>
                <li>html/ <ul style="list-style-type: none;"><li>index.html</li></ul></li>
                <li>js/ <ul style="list-style-type: none;"><li>script.js</li></ul></li>
            </ul>
        </ul>
    </div>
    :)
</body>
</html>"""

class server:
    def __init__(self,ssid,passwd,create_wifi=True):
        self.sensor_dict={}
        self.default_page=True
        for x in os.listdir():
            print(x)
            if x=='html':
                self.default_page=False
                print(self.default_page)
        self.wifi=wifi()
        if create_wifi==False:
            self.ip=self.wifi.wifi_con(ssid=ssid,password=passwd)
        else:
            self.ip=self.wifi.wifi_ap(ssid=ssid,passwd=passwd)
        print(f"[*] HTTP IP: {self.ip[0]}")
        
    def load_file(self,filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except:
            return "<h1>Arquivo nao encontrado</h1>"

    def init(self):
        self.socket=TCP(ip=self.ip[0],port=80)
        self.conn, self.addr=self.socket.init()
        
    def request_recv(self):
        self.conn, self.addr=self.socket.accept()
        self.request = self.conn.recv(1024).decode()
        if self.request:  
            print(self.request)
            self.load_file(req=self.request.split(" ")[1])
            return self.request.split(" ")
        
    def open_file(self,filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except:
            return "<h1>Arquivo não encontrado</h1>"    
        
    def load_file(self,req):    
        print(f"request:{req}")
        if req=="/":
            if self.default_page==True:
                response = default_html
                content_type = "text/html"
            elif self.default_page==False:
                path = "/html/html/index.html"
                response = self.open_file(path[1:])
                content_type = "text/html"
        elif req=='/sensor':
            values=self.sensor_dict
            response=json.dumps(values)
            content_type='application/json'
        else:
            path = '/html/'
            file_solicited=req.split('/')
            print(file_solicited)
            if file_solicited[1]=='css':
                content_type = "text/css"
                path=f"/html/css/{file_solicited[2]}"
            elif file_solicited[1]=='js':
                content_type = "application/javascript"
                path=f"/html/js/{file_solicited[2]}"
            else:
                content_type = "text/html"
            print(path)
            response = self.open_file(path[1:])
        self.send_to_client(response=response,content_type=content_type)
        
    def send_to_client(self,response,content_type):
        self.conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n")
        self.conn.sendall(response)
        print(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n")
        print(response)
        self.conn.close()    

    def sensors(self,name,values: list):
        self.sensor_dict[name]=values