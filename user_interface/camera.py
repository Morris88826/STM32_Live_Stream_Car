import serial
import numpy as np

class Camera():
    def __init__(self, WIDTH=80, HEIGHT=60):
        self.WIDTH = WIDTH
        self.HEIGHT= HEIGHT

        self.current_image = np.zeros((self.HEIGHT, self.WIDTH))

        self.buffer = []
    
    def update_image(self, image):
        self.current_image = image

    def get_image(self, shifted=True):
        if shifted:
            if np.amax(self.current_image) != 0:
                self.current_image = self.current_image * (255/np.amax(self.current_image))
        return self.current_image 
    