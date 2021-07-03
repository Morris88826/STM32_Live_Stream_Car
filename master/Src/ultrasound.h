#ifndef __ULTRASOUND_H
#define __ULTRASOUND_H

#include "stm32f1xx_hal.h"

#define TRIG_PIN_0 GPIO_PIN_4
#define TRIG_PORT_0 GPIOA

#define TRIG_PIN_1 GPIO_PIN_5        ////
#define TRIG_PORT_1 GPIOA            ////

extern uint32_t IC_Val1_0;
extern uint32_t IC_Val2_0;
extern uint32_t IC_Val1_1;
extern uint32_t IC_Val2_1;
extern uint32_t Difference_0;
extern uint32_t Difference_1;
extern uint8_t Is_First_Captured_0;
extern uint8_t Is_First_Captured_1;
extern uint8_t Distance_0;
extern uint8_t Distance_1;


extern TIM_HandleTypeDef htim1;

void delay (uint16_t time);
void HCSR04_Read (void);

#endif 