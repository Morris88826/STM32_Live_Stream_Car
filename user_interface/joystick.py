import numpy as np
import math

class Joystick():
    
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.BTN_EAST = 0 # X
        self.BTN_NORTH = 0 # N
        self.BTN_SOUTH = 0 # S
        self.BTN_WEST = 0 # W
        self.ABS_X = 0 
        self.ABS_Y = 0
        self.ABS_RY = 0
        self.ABS_RX = 0
        self.ABS_Z = 0 # LT
        self.ABS_RZ = 0 # RT

    def get_info(self, log=True):
        
        if log:
            print(self.BTN_EAST, self.BTN_NORTH, self.BTN_SOUTH, self.BTN_WEST, self.ABS_X, self.ABS_Y, self.ABS_RX, self.ABS_RY)

        return (self.BTN_EAST, self.BTN_NORTH, self.BTN_SOUTH, self.BTN_WEST, self.ABS_X, self.ABS_Y, self.ABS_RX, self.ABS_RY)
    def update(self, event):
        
        if event.code == 'SYN_REPORT':
            return 

        if event.code in ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY']:
            setattr(self, event.code, round(event.state/Joystick().MAX_JOY_VAL, 3))
        elif event.code in ['ABS_Z', 'ABS_RZ']:
            setattr(self, event.code, round(event.state/Joystick().MAX_TRIG_VAL, 3))
        else:
            setattr(self, event.code, event.state)


        
