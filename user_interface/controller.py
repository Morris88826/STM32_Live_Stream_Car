import numpy as np
import time


class PID_Controller():

    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.previous_t = None
        self.previous_e = 0
        self.target_value = -1
        self.measure_value = 0

        self.P = 0
        self.I = 0
        self.D = 0

    def set_PID(self, Kp=None, Ki=None, Kd=None):
        if Kp is not None:
            self.Kp = Kp
        if Ki is not None:
            self.Ki = Ki
        if Kd is not None:
            self.Kd = Kd
    
    def set_target_value(self, target_value):
        if self.target_value != target_value:
            self.target_value = target_value
            self.previous_e = 0
            self.previous_t = None
        # self.target_value = target_value

    def run(self, scaler=1):
        current_t = time.time()
        error = self.target_value - self.measure_value


        self.P = self.Kp * error

        if self.previous_t is not None:
            self.I = self.I + self.Ki*error*(current_t - self.previous_t)
            self.D = self.Kd*(error - self.previous_e)/(current_t - self.previous_t)
            # print(self.P, self.I, self.D)
            new_measure_value = self.P + self.I + self.D
        else:
            new_measure_value = self.P


        self.previous_e = error
        self.previous_t = current_t

        if new_measure_value > 0:
            new_measure_value = min(new_measure_value, 100*scaler)
        else:
            new_measure_value = max(new_measure_value, -100*scaler)
        
        return new_measure_value
        
        # return self.target_value


    
