import os
import json
import random

class json:
    def __init__(self):
        pass
    def load(self,file):
        with open(file) as a:
            _json=json.load(a)
            return _json
        
class log:
    def __init__(self):
        if not os.path.exists('log'): 
            print("[*] Creating a log directory")
            os.mkdir('log') 
        self.log_id = str(random.getrandbits(16))
        self.log_name = os.path.join("log", f"log{self.log_id}.txt")
        print(self.log_name)
        print(os.listdir('log'))
        with open(self.log_name, "w") as f:
            f.write(f"---Log created---\n---Id: {self.log_id}---\n")
            if __name__ == '__main__':
                f.write(f"[*] Arquivo rodado sozinho, favor utilizar ele como biblioteca\n :)")
        
        def write(self,data):
            with open(self.log_name, 'w') as f:
                f.write(f'[*] {data}')        

l=log()
