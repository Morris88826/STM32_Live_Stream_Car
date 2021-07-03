import tkinter as tk
import time
from inputs import get_gamepad
from joystick import Joystick
import glob
from PIL import Image, ImageTk
import numpy as np
from movement import MovementHandler
from bluetooth import Bluetooth
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from camera import Camera
import random

using_PID = False

# Main Tkinter application
class Application(tk.Frame):
    # Init the variables & start measurements
    def __init__(self, root=None):
        tk.Frame.__init__(self, root)

        self.root = root

        self.bt = Bluetooth('COM7', 115200, 0, timeout=None)
        self.bt2 = Bluetooth('COM9', 115200, 1, timeout=0.1)
        self.camera = Camera(WIDTH=40, HEIGHT=30)
        

        self.previous = 0

        self.label = tk.Label(text="Real-time Image")
        self.label.grid(row=0, column=0)

        self.images_root = './test_frames'
        self.num_frames = len(glob.glob(self.images_root+'/*'))
        self.current_frame = 0
        self.scaler = 8
        self.update_image()
        self.panel = tk.Label(image=self.image)
        self.panel.grid(row=1, column=0)
        self.show_frame()

        self.label1 = tk.Label(text="Controller Status")
        self.label1.grid(row=0, column=1)

        self.mh = MovementHandler()
        
        self.info = tk.Frame()
        self.info.grid(row=1, column=1, padx=(10,10))
        self.label2 = tk.Label(self.info, text="Left_x: ")
        self.label2.grid(row=2, column=0, padx=(10,10))
        self.label3 = tk.Label(self.info, text="Left_y: ")
        self.label3.grid(row=3, column=0, padx=(10,10))
        self.label4 = tk.Label(self.info, text="Movement: ")
        self.label4.grid(row=4, column=0, padx=(10,10))
        self.label5 = tk.Label(self.info, text="Speed: Set/Target ")
        self.label5.grid(row=5, column=0, padx=(10,10))
        self.label6 = tk.Label(self.info, text="Left_Motor: ")
        self.label6.grid(row=6, column=0, padx=(10,10))
        self.label7 = tk.Label(self.info, text="Right_Motor: ")
        self.label7.grid(row=7, column=0, padx=(10,10))
        self.label8 = tk.Label(self.info, text="Back_Motor: ")
        self.label8.grid(row=8, column=0, padx=(10,10))

        self.button = tk.Button(self.info, text='PID Tuning', command=self.create_pid_window)
        self.button.grid(row=9, column=0, pady=(10,10))
        self.label9 = tk.Label(self.info, text="Using PID: {}".format("True" if using_PID else "False"))
        self.label9.grid(row=10, column=0, padx=(10,10))
        self.button1 = tk.Button(self.info, text='Connect Bluetooth 1', command=self.bt.toggle_connect)
        self.button1.grid(row=11, column=0, padx=(10,10))
        self.button2 = tk.Button(self.info, text='Connect Bluetooth 2', command=self.bt2.toggle_connect)
        self.button2.grid(row=12, column=0, padx=(10,10))

        self.joystick = Joystick()
        self.joystick_event()
        self.receive_bt_event()
        self.send_info_to_pid_window_event()
        

    def create_pid_window(self):
        global using_PID
        using_PID = True
        self.new = tk.Toplevel(self.root)
        self.pid_window = PID_window(self.new)
        
    
    def send_info_to_pid_window_event(self):
        try:
            # # Debug
            # self.pid_window.motor0_mv = random.randint(-100,100)
            # self.pid_window.motor0_tv = random.randint(50,60)
            # self.pid_window.motor1_mv  = random.randint(-100,100)
            # self.pid_window.motor1_tv = random.randint(50,60)
            # self.pid_window.motor2_mv = random.randint(-100,100)
            # self.pid_window.motor2_tv = random.randint(50,60)
            self.pid_window.motor0_mv = self.mh.controller0.measure_value
            self.pid_window.motor0_tv = self.mh.controller0.target_value
            self.pid_window.motor1_mv = self.mh.controller1.measure_value
            self.pid_window.motor1_tv = self.mh.controller1.target_value
            self.pid_window.motor2_mv = self.mh.controller2.measure_value
            self.pid_window.motor2_tv = self.mh.controller2.target_value
        
        except:
            pass

        self.after(50, self.send_info_to_pid_window_event)


	# Measure data from the sensor
    def joystick_event(self):

		# Request data and read the answer
        events = get_gamepad(blocking=False)
        if events == None:
            time.sleep(0.0001)
        else:
            for event in events:
                self.joystick.update(event)

        info = self.joystick.get_info(log=False)

        self.update_info(info)

        self.mh.control(self.joystick.ABS_X, self.joystick.ABS_Y, using_PID)
        
        if (self.counter % 50==0):
            self.send_bt()
            self.counter = 0
        self.counter += 1
        self.after(1, self.joystick_event)

    def send_bt(self):
        self.bt.packaging('joystick_x', self.joystick.ABS_X, send=True)
        self.bt.packaging('joystick_y', self.joystick.ABS_Y, send=True)
        self.bt.packaging('motor_0', self.mh.motor0.get_speed(), send=True)
        self.bt.packaging('motor_1', self.mh.motor1.get_speed(), send=True)
        self.bt.packaging('motor_2', self.mh.motor2.get_speed(), send=True)
    
    def receive_bt_event(self):
        if self.bt2.connected:
            if self.bt2.current_r_package is None:
                header = self.bt2.s.read()

                if (header == bytes([1])):
                    self.bt2.current_r_package = 'camera'

                if (header == bytes([3])):
                    self.bt2.current_r_package = 'encoder0'

                if (header == bytes([5])):
                    self.bt2.current_r_package = 'encoder1'

                if (header == bytes([7])):
                    self.bt2.current_r_package = 'encoder2'

            
            if self.bt2.current_r_package == 'camera':
                success = self.bt2.receive_cam_data(self.camera)
                self.bt2.current_r_package = None

            elif self.bt2.current_r_package == 'encoder0':               
                self.bt2.current_r_package = None
                self.bt2.receive_encoder_data(self.mh.controller0)


            elif self.bt2.current_r_package == 'encoder1': 
                self.bt2.current_r_package = None
                self.bt2.receive_encoder_data(self.mh.controller1)


            elif self.bt2.current_r_package == 'encoder2': 
                self.bt2.current_r_package = None
                self.bt2.receive_encoder_data(self.mh.controller2)


        self.after(200, self.receive_bt_event)



    def update_info(self, info):
        self.label2.configure(text="Left_x: {}".format(self.joystick.ABS_X))
        self.label3.configure(text="Left_y: {}".format(self.joystick.ABS_Y))
        self.label4.configure(text="Movement: {}".format(self.mh.get_movement()))
        self.label6.configure(text="Left_Motor: {:.1f}%/{:.1f}%".format(self.mh.motor0.get_speed(), self.mh.motor0.get_target_speed()))
        self.label7.configure(text="Right_Motor: {:.1f}%/{:.1f}%".format(self.mh.motor1.get_speed(), self.mh.motor1.get_target_speed()))
        self.label8.configure(text="Back_Motor: {:.1f}%/{:.1f}%".format(self.mh.motor2.get_speed(), self.mh.motor2.get_target_speed()))
        self.label9.configure(text="Using PID: {}".format("True" if using_PID else "False"))
    
    def update_image(self):
        self.image = ImageTk.PhotoImage(Image.fromarray(self.camera.get_image()).resize((self.camera.WIDTH*self.scaler, self.camera.HEIGHT*self.scaler)))

    def show_frame(self):
        self.current_frame += 1
        self.counter = 0

        if self.current_frame >= self.num_frames:
            self.current_frame = 0
        
        self.update_image()
        self.panel.configure(image=self.image)
        self.after(100, self.show_frame)

class PID_window(tk.Frame):
    def __init__(self, master):
        super(PID_window, self).__init__()
        self.master = master
        self.master.geometry('600x800')
        self.master.wm_title("PID Tuning")

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, figsize=(6,8))
        self.ax1.set(title='Motor0', xlabel='Time', ylabel='Measure', ylim=(-100,100), xlim=(0,100))
        self.ax2.set(title='Motor1', xlabel='Time', ylabel='Measure', ylim=(-100,100), xlim=(0,100))
        self.ax3.set(title='Motor2', xlabel='Time', ylabel='Measure', ylim=(-100,100), xlim=(0,100))

        self.current_line1 = self.ax1.plot([],[])[0]
        self.target_line1 = self.ax1.plot([],[])[0]

        self.current_line2 = self.ax2.plot([],[])[0]
        self.target_line2 = self.ax2.plot([],[])[0]

        self.current_line3 = self.ax3.plot([],[])[0]
        self.target_line3 = self.ax3.plot([],[])[0]

        self.buffer1 = np.array([])
        self.target_buffer1 = np.array([])

        self.buffer2 = np.array([])
        self.target_buffer2 = np.array([])

        self.buffer3 = np.array([])
        self.target_buffer3 = np.array([])

        self.ax1.legend([self.current_line1, self.target_line1], ['Observed Value', 'Target Value'])
        self.ax2.legend([self.current_line2, self.target_line2], ['Observed Value', 'Target Value'])
        self.ax3.legend([self.current_line3, self.target_line3], ['Observed Value', 'Target Value'])
        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()

        self.motor0_mv = 0
        self.motor0_tv = 0
        self.motor1_mv = 0
        self.motor1_tv = 0
        self.motor2_mv = 0
        self.motor2_tv = 0

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.plot_data()

    def on_closing(self):
        global using_PID
        using_PID = False
        self.master.destroy()

    def plot_data(self):

        # Update Motor 0
        if self.buffer1.shape[0] < 100:
            self.buffer1 = np.append(self.buffer1, self.motor0_mv)
            self.target_buffer1 = np.append(self.target_buffer1, self.motor0_tv)
        else:
            self.buffer1[0:99] = self.buffer1[1:100]
            self.buffer1[99] = self.motor0_mv
            self.target_buffer1[0:99] = self.target_buffer1[1:100]
            self.target_buffer1[99] = self.motor0_tv

        self.current_line1.set_xdata(np.arange(0, self.buffer1.shape[0]))
        self.current_line1.set_ydata(self.buffer1)
        self.target_line1.set_xdata(np.arange(0, self.target_buffer1.shape[0]))
        self.target_line1.set_ydata(self.target_buffer1)
        
        # Update Motor 1
        if self.buffer2.shape[0] < 100:
            self.buffer2 = np.append(self.buffer2, self.motor1_mv)
            self.target_buffer2 = np.append(self.target_buffer2, self.motor1_tv)
        else:
            self.buffer2[0:99] = self.buffer2[1:100]
            self.buffer2[99] = self.motor1_mv
            self.target_buffer2[0:99] = self.target_buffer2[1:100]
            self.target_buffer2[99] = self.motor1_tv
        
        self.current_line2.set_xdata(np.arange(0, self.buffer2.shape[0]))
        self.current_line2.set_ydata(self.buffer2)
        self.target_line2.set_xdata(np.arange(0, self.target_buffer2.shape[0]))
        self.target_line2.set_ydata(self.target_buffer2)

        # Update Motor 2
        if self.buffer3.shape[0] < 100:
            self.buffer3 = np.append(self.buffer3, self.motor2_mv)
            self.target_buffer3 = np.append(self.target_buffer3, self.motor2_tv)
        else:
            self.buffer3[0:99] = self.buffer3[1:100]
            self.buffer3[99] = self.motor2_mv
            self.target_buffer3[0:99] = self.target_buffer3[1:100]
            self.target_buffer3[99] = self.motor2_tv
        
        self.current_line3.set_xdata(np.arange(0, self.buffer3.shape[0]))
        self.current_line3.set_ydata(self.buffer3)
        self.target_line3.set_xdata(np.arange(0, self.target_buffer3.shape[0]))
        self.target_line3.set_ydata(self.target_buffer3)

        self.canvas.draw()
        self.after(100, self.plot_data)        


# Create and run the GUI
root = tk.Tk()
root.resizable(0,0)
root.geometry('500x300')
frame = Application(root) 
frame.mainloop()