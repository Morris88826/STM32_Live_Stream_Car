#include "joystick.h"
#include <math.h>

void Joystick_Init(void){
	my_joystick.BTN_EAST = 0; // X
	my_joystick.BTN_NORTH = 0; // N
  my_joystick.BTN_SOUTH = 0; // S
  my_joystick.BTN_WEST = 0; // W
  my_joystick.ABS_X=0.0;
  my_joystick.ABS_Y=0.0;
  my_joystick.ABS_RY=0.0;
  my_joystick.ABS_RX=0.0;
  my_joystick.ABS_Z=0.0; // LT
  my_joystick.ABS_RZ=0.0; // RT
}

void Joystick_SetValue(int id, float value){
	if(id==0)
		my_joystick.ABS_X = value;
	else if(id==1)
		my_joystick.ABS_Y = value;
	else if(id==2)
		my_joystick.ABS_RX = value;
	else if(id==3)
		my_joystick.ABS_RY = value;
	else if(id==4)
		my_joystick.ABS_Z = value;
	else if(id==5)
		my_joystick.ABS_RZ = value;
}