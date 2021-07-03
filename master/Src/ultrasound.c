#include "ultrasound.h"


void delay (uint16_t time)
{
	__HAL_TIM_SET_COUNTER(&htim1, 0);
	while (__HAL_TIM_GET_COUNTER(&htim1) < time);
}

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
	if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1)  // if the interrupt source is channel1
	{
		if (Is_First_Captured_0==0) // if the first value is not captured
		{
			IC_Val1_0 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1); // read the first value
			Is_First_Captured_0 = 1;  // set the first captured as true
			// Now change the polarity to falling edge
			__HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_FALLING);
		}

		else if (Is_First_Captured_0==1)   // if the first is already captured
		{
			IC_Val2_0 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);  // read second value
			__HAL_TIM_SET_COUNTER(htim, 0);  // reset the counter

			if (IC_Val2_0 > IC_Val1_0)
			{
				Difference_0 = IC_Val2_0-IC_Val1_0;
			}

			else if (IC_Val1_0 > IC_Val2_0)
			{
				Difference_0 = (0xffff - IC_Val1_0) + IC_Val2_0;
			}

			Distance_0 = Difference_0 * .034/2;
			Is_First_Captured_0 = 0; // set it back to false

			// set polarity to rising edge
			__HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_RISING);
			__HAL_TIM_DISABLE_IT(&htim1, TIM_IT_CC1);
		}
	}
	if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_4)  // if the interrupt source is channel4
	{
		if (Is_First_Captured_1==0) // if the first value is not captured
		{
			IC_Val1_1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_4); // read the first value
			Is_First_Captured_1 = 1;  // set the first captured as true
			// Now change the polarity to falling edge
			__HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_4, TIM_INPUTCHANNELPOLARITY_FALLING);
		}

		else if (Is_First_Captured_1==1)   // if the first is already captured
		{
			IC_Val2_1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_4);  // read second value
			__HAL_TIM_SET_COUNTER(htim, 0);  // reset the counter

			if (IC_Val2_1 > IC_Val1_1)
			{
				Difference_1 = IC_Val2_1-IC_Val1_1;
			}

			else if (IC_Val1_1 > IC_Val2_1)
			{
				Difference_1 = (0xffff - IC_Val1_1) + IC_Val2_1;
			}

			Distance_1 = Difference_1 * .034/2;
			Is_First_Captured_1 = 0; // set it back to false

			// set polarity to rising edge
			__HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_4, TIM_INPUTCHANNELPOLARITY_RISING);
			__HAL_TIM_DISABLE_IT(&htim1, TIM_IT_CC4);
		}
	}
}

void HCSR04_Read (void)
{
	HAL_GPIO_WritePin(TRIG_PORT_0, TRIG_PIN_0, GPIO_PIN_SET);  // pull the TRIG pin HIGH
	HAL_GPIO_WritePin(TRIG_PORT_1, TRIG_PIN_1, GPIO_PIN_SET);  // pull the TRIG pin HIGH
	delay(10);  // wait for 10 us
	HAL_GPIO_WritePin(TRIG_PORT_0, TRIG_PIN_0, GPIO_PIN_RESET);  // pull the TRIG pin low
	HAL_GPIO_WritePin(TRIG_PORT_1, TRIG_PIN_1, GPIO_PIN_RESET);  // pull the TRIG pin low

	__HAL_TIM_ENABLE_IT(&htim1, TIM_IT_CC1);
	__HAL_TIM_ENABLE_IT(&htim1, TIM_IT_CC4);
}