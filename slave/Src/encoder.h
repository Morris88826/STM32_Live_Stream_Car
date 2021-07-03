#ifndef __ENCODER_H
#define	__ENCODER_H
#include "stm32f1xx_hal.h"
#include <stdio.h>
#include <time.h>

struct Encoder{
	uint8_t id;
	int pos;
	float rpm;
	float time_period;
	clock_t previous_t;
}extern encoder0, encoder1, encoder2;

void Encoder_Init(struct Encoder*, uint8_t);

void read_encoder(struct Encoder*);

void get_rpm(struct Encoder*);

#endif
