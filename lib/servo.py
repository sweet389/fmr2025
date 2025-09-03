import machine

class Servo:
    def __init__(self,pin,frequencia=50):
        self.servo_pin=machine.Pin(pin)
        self.servo_pwm=machine.PWM(self.servo_pin, freq=frequencia)
    def set_angle(self,angle):
        duty = int(3277 + (angle / 180) * (6554 - 3277))
        self.servo_pwm.duty(duty)