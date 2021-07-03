#include "motor.h"
#include <math.h>

void Motor_Init(void){
	my_motor.motor_0_speed = 0.0; 
	my_motor.motor_1_speed = 0.0; 
  my_motor.motor_2_speed = 0.0; 
}

void Motor_SetValue(int id, float value){
	if(id==0)
		my_motor.motor_0_speed = value;
	else if(id==1)
		my_motor.motor_1_speed = value;
	else if(id==2)
		my_motor.motor_2_speed = value;
}
