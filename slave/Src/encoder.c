#include "encoder.h"
#include <math.h>

void Encoder_Init(struct Encoder* encoder, uint8_t id){
	encoder->id = id;
	encoder->pos = 0;
	encoder->time_period = 200;
	encoder->rpm = 0.0;
	encoder->previous_t = HAL_GetTick();
}

void read_encoder(struct Encoder* encoder){
	if (encoder->id == 0){
		int b = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_7);
		if (b>0)
			encoder->pos += 1;
		else
			encoder->pos -= 1;
	}
	else if (encoder->id == 1){
		int b = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_6);
		if (b>0)
			encoder->pos += 1;
		else
			encoder->pos -= 1;
	}
	else if (encoder->id == 2){
		int b = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_7);
		if (b>0)
			encoder->pos += 1;
		else
			encoder->pos -= 1;
	}
}


void get_rpm(struct Encoder* encoder){
	clock_t current_t = HAL_GetTick();
	if (current_t > (encoder->previous_t+ encoder->time_period)){
		//encoder->rpm = (encoder->pos*60);//*(100/(current_t-encoder->previous_t));
		encoder->rpm = (encoder->pos*60.0)/(current_t-encoder->previous_t);
		encoder->pos = 0;
		encoder->previous_t = current_t;
	}
	
}
