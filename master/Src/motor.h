#ifndef __MOTOR_H
#define	__MOTOR_H
#include "stm32f1xx_hal.h"
#include <string.h>

struct Motor{
  float motor_0_speed;
  float motor_1_speed;
  float motor_2_speed;
}extern my_motor;

void Motor_Init(void);

void Motor_SetValue(int, float);
#endif
