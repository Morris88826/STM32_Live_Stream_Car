import serial
import struct
import sys
from camera import Camera
import numpy as np
from controller import PID_Controller
import random

class Bluetooth():
    def __init__(self, comport, baud_rate, id, timeout=0):
        self.comport = comport
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.id = id
        self.s = None
        self.package_type = {
            'joystick_x': 0,
            'joystick_y': 1,
            'motor_0': 2,
            'motor_1': 3,
            'motor_2': 4
        }

        self.package_size = {
            'joystick_x': 4, # float32
            'joystick_y': 4,
            'motor_0': 4,
            'motor_1': 4,
            'motor_2': 4
        }
        self.connected = False
        self.current_r_package = None

    def packaging(self, package_type, data, send=False):
        data = float(data)
        if type(data) == float:
            data = bytearray(struct.pack("f", data))

        size = bytearray(struct.pack("B", self.package_size[package_type]))
        package_type = '{:02d}'.format(self.package_type[package_type])

        package_type = package_type.encode()

        package = [package_type, size, data]

        if send == True:
            self.send_data(package)
        else:
            return package

    def send_data(self, package):

        if self.connected:
            self.s.write(package[0])
            self.s.write(package[1])
            self.s.write(package[2])
            self.s.write(b'\n')
        return
    
    def receive_cam_data(self, camera:Camera):
        width = camera.WIDTH
        height = camera.HEIGHT

        
        buffer = []
        for i in range(width*height):
            data = self.s.read()
            if len(data) == 0:
                return False
            if data == bytes([2]):
                camera.current_image = np.zeros((height, width))
                return False
            buffer.append(ord(data))

        camera.update_image(np.array(buffer).astype(int).reshape((height, width)))
        return True
    
    def receive_encoder_data(self, controller:PID_Controller):
        buffer = ""
        for i in range (8):
            data = self.s.read()
            if data == bytes([4]) or data == bytes([6]) or data == bytes([8]):
                return False
            buffer += data.decode("utf-8") 

        data = float(buffer)
        print(data)
        controller.measure_value = data

        return data


    def toggle_connect(self):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        
        self.s = serial.Serial(self.comport, baudrate=self.baud_rate, timeout=self.timeout)
        if self.id == 1:
            self.s.write('R'.encode())
        self.connected = True
        print('Connected')
    
    def disconnect(self):
        print('Disconnected')
        self.s.write('G'.encode())
        self.s.close()
        self.connected = False
