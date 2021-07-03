#ifndef __BLUETOOTH_H
#define	__BLUETOOTH_H
#include "stm32f1xx_hal.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

union Data {
  float f;
  char b[4];
};


extern uint8_t* bt_buffer;
extern uint8_t Rxstr[10];
extern uint8_t v[4];
extern union Data bt_data;
extern uint8_t ABS_X[9];
extern uint8_t ABS_Y[9];
extern uint8_t Motor_0[9];
extern uint8_t Motor_1[9];
extern uint8_t Motor_2[9];


#endif