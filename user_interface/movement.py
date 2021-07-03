from controller import PID_Controller
import numpy as np
class Motor():
    def __init__(self, id):
        self.id = id
        self.duty_cycle = 0
        self.target_duty_cycle = 0
        self.dir = 1 # forward
        self.rpm = 0
        self.target_rpm = 0

    def set_pwm(self, rpm):
        duty_cycle = rpm/100.0
        if rpm > 0:
            self.duty_cycle = abs(duty_cycle)
            self.dir = 1
        else:
            self.duty_cycle = abs(duty_cycle)
            self.dir = -1
    
    def set_target_speed(self, duty_cycle, dir):
        self.target_duty_cycle = duty_cycle
        self.dir = dir
    
    def get_target_speed(self):
        return self.target_duty_cycle*100*self.dir
    
    def get_speed(self):
        return self.duty_cycle*100*self.dir

class MovementHandler():
    def __init__(self):
        self.motor0 = Motor(id=0) # Left
        self.motor1 = Motor(id=1) # Right
        self.motor2 = Motor(id=2) # Back

        self.scaler = 0.8

        self.movement_type = {
            -1: 'IDLE',
            0: 'Forward',
            1: 'Backward',
            2: 'Rotate_CW',
            3: 'Rotate_CCW'
        }

        self.controller0 = PID_Controller(Kp=0.6, Ki=0.1, Kd=0)
        self.controller1 = PID_Controller(Kp=0.6, Ki=0.1, Kd=0)
        self.controller2 = PID_Controller(Kp=0.6, Ki=0.1, Kd=0)

        self.movement = -1

        
    def control(self, left_x, left_y, using_PID=False):

        left_x = left_x*self.scaler
        left_y = left_y*self.scaler

        if left_y >= abs(left_x) and left_y>0.3:
            self.movement = 0
            self.controller0.set_target_value(min(abs(left_y)*100, 100))
            self.controller1.set_target_value(max(abs(left_y)*-100, -100))
            self.controller2.set_target_value(0)
            self.motor0.set_target_speed(abs(left_y), -1)
            self.motor1.set_target_speed(abs(left_y), 1)
            self.motor2.set_target_speed(0, 1)


        elif abs(left_y) >= abs(left_x) and left_y<-0.3:
            self.movement = 1
            self.controller0.set_target_value(max(abs(left_y)*-100, -100))
            self.controller1.set_target_value(min(abs(left_y)*100, 100))
            self.controller2.set_target_value(0)
            self.motor0.set_target_speed(abs(left_y), 1)
            self.motor1.set_target_speed(abs(left_y), -1)
            self.motor2.set_target_speed(0, 1)

        elif left_x > abs(left_y) and left_x>0.3:
            self.controller0.set_target_value(60)
            self.controller1.set_target_value(60)
            self.controller2.set_target_value(60)
            self.motor0.set_target_speed(0.6, 1)
            self.motor1.set_target_speed(0.6, 1)
            self.motor2.set_target_speed(0.6, 1)
            self.movement = 2
        elif abs(left_x) > abs(left_y) and left_x<-0.3:
            self.controller0.set_target_value(-60)
            self.controller1.set_target_value(-60)
            self.controller2.set_target_value(-60)
            self.motor0.set_target_speed(0.6, -1)
            self.motor1.set_target_speed(0.6, -1)
            self.motor2.set_target_speed(0.6, -1)
            self.movement = 3
        else:
            self.controller0.set_target_value(0)
            self.controller1.set_target_value(0)
            self.controller2.set_target_value(0)
            self.motor0.set_target_speed(0, 1)
            self.motor1.set_target_speed(0, 1)
            self.motor2.set_target_speed(0, 1)
            self.movement = -1



        if using_PID:
            measure_value_0 = self.controller0.run(scaler=self.scaler)
            measure_value_1 = self.controller1.run(scaler=self.scaler)
            measure_value_2 = self.controller2.run(scaler=self.scaler)
            self.motor0.set_pwm(measure_value_0)
            self.motor1.set_pwm(measure_value_1)
            self.motor2.set_pwm(measure_value_2)
        else:
            self.motor0.set_pwm(self.controller0.target_value)
            self.motor1.set_pwm(self.controller1.target_value)
            self.motor2.set_pwm(self.controller2.target_value)
        

    def send_info(self):
        pass

    def get_movement(self):
        return self.movement_type[self.movement]
