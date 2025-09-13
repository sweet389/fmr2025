import machine
import time

class motor:
    def __init__(self, in1, in2, freq=1000):
        self.pwm = machine.PWM(machine.Pin(in1), freq=freq, duty=0)
        self.dir = machine.Pin(in2, machine.Pin.OUT)

    def forward(self, speed):
        self.dir.value(0)
        self.pwm.duty(speed) 
    def backward(self, speed):
        self.dir.value(1)
        self.pwm.duty(1023 - speed)

class omnidirecional:
    def __init__(self, left_front,right_front,left_back,right_back):
        self.lf_ft=left_front
        self.lf_bk=left_back
        self.rt_ft=right_front
        self.rt_bk=right_back
    def _process_values(self,axial,lateral,yaw):
        right_front=axial-lateral-yaw
        left_front=axial+lateral+yaw
        right_back=axial+lateral-yaw
        left_back=axial-lateral+yaw
        return right_front,left_front,right_back,left_back
    def move(self,axial,lateral,yaw):
        right_front,left_front,right_back,left_back=self._process_values(axial,lateral,yaw)
        if right_front<0:
            self.rt_ft.backward(right_front*-1)
        else:
            self.rt_ft.forward(right_front)

        if right_back<0:
            self.rt_bk.backward(right_back*-1)
        else:
            self.rt_bk.forward(right_back)

        if left_front<0:
            self.lf_ft.backward(left_front*-1)
        else:
            self.lf_ft.forward(left_front)

        if left_back<0:
            self.lf_bk.backward(left_back*-1)
        else:
            self.lf_bk.forward(left_back)
            