import machine
import time

class motor:
    def __init__(self,pin1,pin2,pwm=None):
        self.pin=machine.Pin(pin1, machine.Pin.OUT)
        self.pin2=machine.Pin(pin2, machine.Pin.OUT)
        if pwm:
            self.pwm=machine.PWM(pwm)
            self.pwm.freq(1000)
    def front(self):
        self.pin.on()
        self.pin2.off()
    def back(self):
        self.pin.off()
        self.pin2.on()
    def speed(self,value):
        self.pwm.duty(value - 0 * (100 - 0) / (1023 - 0) + 0)
        
