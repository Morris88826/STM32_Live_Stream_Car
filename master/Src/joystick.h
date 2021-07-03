#ifndef __JOYSTICK_H
#define	__JOYSTICK_H
#include "stm32f1xx_hal.h"
#include <string.h>


struct Joystick{
	uint8_t BTN_EAST; // X
	uint8_t BTN_NORTH; // N
  uint8_t BTN_SOUTH; // S
  uint8_t BTN_WEST; // W
  float ABS_X;
  float ABS_Y;
  float ABS_RY;
  float ABS_RX;
  float ABS_Z; // LT
  float ABS_RZ; // RT
}extern my_joystick;

void Joystick_Init(void);

void Joystick_SetValue(int, float);
#endif
