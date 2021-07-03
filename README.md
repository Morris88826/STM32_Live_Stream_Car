# STM32 Live Stream Car
Author: Mu-Ruei Tseng, Yih Cheng 

![](https://i.imgur.com/oDeRqRS.jpg)

## Overview
We want to build a three-wheels remote control car that can return live streams of the current room. We use ultrasound sensors to detect walls or obstacles to automatically stop the car when almost bumping into the walls. We use bluetooth  to communicate between tthe microcontroller and the computer, where the computer will send instructions to control the car, and also, the camera will send the live stream back to the computer for users to see. In addition, we implement the PID controller that uses motor's encoder value to adjust the motor rpm to the target speed.

![](https://i.imgur.com/YnOrA8H.png)

## List of functions
* Computer UI shows all controls of the car and live stream video.
* Xbox controller controls the movements of the car.
* The mecanum wheels allows this car to rotate in cycles, unlike most common cars.
* Camera provides live stream image updates to computer.
* Ultrasonic sensor forces the car to stop when encountering obstacles.
* PID controller uses Hall encoders to control the PWM of the car.
* Bluetooth connects the computer and the car.

## Pin Layout for STM32
We use two boards for three main reasons:
1. Not enough available pins
2. Doesn’t have enough transmitting power when sending both the real-time image and also control data
3. The workload for sending encoder values, image pixels, and receiving PWM signals all in real time is too large for only one board.

To overcome these difficulites, we decided to utilize two boards and use UART to communicate between them. 

Here are the pin layout for the two boards (master/slave).![](https://i.imgur.com/PVsCWOq.png)

### Master Board
* Set motors’ pwm and control the motors based on values calculated from the PC (GUI).
* Obtain distance from the ultrasonic sensor and stop the car when the car is reaching the wall.
* Send motor speed information to the slave board to display on the LCD

### Slave Board 
* Get camera image and encoder values
* Display necessary information on the LCD


## General User Interface (GUI)
We use python and tkinter to build the user interface to control the robot remotely. Our user interface supports:

* Get the signal from Xbox controller, use it to set the movement of the car.
* Pop-up window showing the enocder value of the three motors.
* Calculate PID based on the encoder values to maintain the motor speed at a desire speed. 
* Display images captured by the camera
* Buttons to connect/reconnect bluetooth

### PID Control
We want to better adjust the motor pwm signal to reach the desire rpm we set. We use encoders’ values to compare with the target value we set to determine the error that can be used as the input for the controller to adjust the output speed.

> PID control: 
> P: Proportional (Kp) 
> Output is proportion to the error multiply a constant Kp. 
> 
> I: Intergral (Ki)
> Integral path will continue sum up the errors as the time move on and multiply with a constant Ki. It can be used to remove constant error since no matter how small the constant error is, the summation of the error can be significant enough to adjust the controller output.
> 
> D: Derivative (Kd)
> Detect the rate of changes in the error. The faster the error changes, the larger the D value will output. 

## Other hardware components

### Camera 
* Location: Slave Board
* Image size: 60x80 (height x width)
* Frame rate: 1~2 frames per sec
* Image type: Grayscale
* Function: Observe the environment. The captured image is sent from from the slave board to the GUI on PC
<img width="250" alt="Screen Shot 2021-07-04 at 3 04 34 AM" src="https://user-images.githubusercontent.com/32810188/124364507-96d83180-dc74-11eb-8683-caa0caed90a2.png">
#### Implementation
1. Camera Sensors capture image Pixels.
2. Camera then writes the pixels into FIFO buffer
3. Different Clock signals of OV7725 in order to control writing buffer and reading buffer time.
4. STM32 reads the FIFO for camera data.
5. STM32 sends these camera data to computer through Bluetooth (HC-05).

### Ultrasonic Sensor
* Location: Master Board 
* Detect distance between the car and and walls/obstacles
* Function: Stop the car when the distance is within 15 cm
<img width="500" alt="Screen Shot 2021-07-04 at 3 02 21 AM" src="https://user-images.githubusercontent.com/32810188/124364466-5973a400-dc74-11eb-94df-a1694868bb39.png">
#### Implementation
1. TRIG pin High for 10us.
2. HC-SR04 send out 8 cycles of 40kHz ultrasound
3. Signal returns, and will output High pulse.
4. Distance = Output High level time * speed (340m/s)/2

## More Information
[Presentation](https://www.youtube.com/watch?v=Tc_mnBWXl4c&ab_channel=YihCHENG)
