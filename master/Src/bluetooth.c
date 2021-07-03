#include "bluetooth.h"



void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) 
{
	
	
		uint8_t header[2];
		header[0] = Rxstr[0];
		header[1] = Rxstr[1];
		
		uint8_t size = Rxstr[2];
		
		if (Rxstr[2+size+1] != 10)
			return;

		if ((header[0] == '0') && (header[1]=='0')){
			bt_data.b[3] = Rxstr[6];
			bt_data.b[2] = Rxstr[5];
			bt_data.b[1] = Rxstr[4];
			bt_data.b[0] = Rxstr[3];
			Joystick_SetValue(0, bt_data.f);
		}

		else if ((header[0] == '0') && (header[1]=='1')){
			bt_data.b[3] = Rxstr[6];
			bt_data.b[2] = Rxstr[5];
			bt_data.b[1] = Rxstr[4];
			bt_data.b[0] = Rxstr[3];
			Joystick_SetValue(1, bt_data.f);
		}
		
		else if ((header[0] == '0') && (header[1]=='2')){
			bt_data.b[3] = Rxstr[6];
			bt_data.b[2] = Rxstr[5];
			bt_data.b[1] = Rxstr[4];
			bt_data.b[0] = Rxstr[3];
			Motor_SetValue(0, bt_data.f);
		}
		
		else if ((header[0] == '0') && (header[1]=='3')){
			bt_data.b[3] = Rxstr[6];
			bt_data.b[2] = Rxstr[5];
			bt_data.b[1] = Rxstr[4];
			bt_data.b[0] = Rxstr[3];
			Motor_SetValue(1, bt_data.f);
		}
		
		else if ((header[0] == '0') && (header[1]=='4')){
			bt_data.b[3] = Rxstr[6];
			bt_data.b[2] = Rxstr[5];
			bt_data.b[1] = Rxstr[4];
			bt_data.b[0] = Rxstr[3];
			Motor_SetValue(2, bt_data.f);
		}
		
		bt_data.f = 0;

}

