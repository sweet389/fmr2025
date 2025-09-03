import network
import time

class wifi:
    def __init__(self):
        pass
        
    def wifi_ap(self,ssid="ESP32", passwd="123", hostname='23PSE'):
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(ssid=ssid, password=passwd)
        network.hostname(hostname)
        print(self.ap.ifconfig()[0])
        return self.ap.ifconfig()[0]

    def wifi_con(self,ssid,password):
        print(f"[*] Trying connection on {ssid} with pass {password}")
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.wifi.connect(ssid, password)
        while not self.wifi.isconnected():
            pass
        print(f"[*] Sucessful connection on {ssid} \n[*] Your IP is: {self.wifi.ifconfig()}")
        
    def scan(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print("[*] Scanning for Wi-Fi networks...")
        networks = wlan.scan()

        if networks:
            print("[*] Found networks:")
            for net in networks:
                ssid = net[0].decode('utf-8')
                rssi = net[3]
                channel = net[2]
                security = net[4] # 0: open, 1: WEP, 2: WPA-PSK, 3: WPA2-PSK, 4: WPA/WPA2-PSK
                print(f"[*] SSID: {ssid}, RSSI: {rssi} dBm, Channel: {channel}, Security: {security}")
        else:
            print("[*] No Wi-Fi networks found.")
        

