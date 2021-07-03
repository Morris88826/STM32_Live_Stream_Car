#ifndef __BLUETOOTH_H
#define	__BLUETOOTH_H
#include "stm32f1xx_hal.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "cvector.h"
#include "joystick.h"
#include "motor.h"

union Data {
  float f;
  char b[4];
};


extern uint8_t* bt_buffer;
extern uint8_t Rxstr[8];
extern uint8_t v[4];
extern union Data bt_data;
extern UART_HandleTypeDef huart3;


#endif
