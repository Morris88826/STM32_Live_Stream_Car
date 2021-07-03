#include "usart2.h"


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) 
{
				
    uint8_t header;
    header = Rxstr[0];
		uint8_t i;
    
    //if (Rxstr[2+size+1] != 10)
    //    return;

    if (header == 'A'){
			for (i=0; i<9; i++) {
				ABS_X[i] = Rxstr[i+1];
			}
    }

    else if (header == 'B'){
			for (i=0; i<9; i++) {
				ABS_Y[i] = Rxstr[i+1];
			}
    }
    
    else if (header == 'C'){
			for (i=0; i<9; i++) {
				Motor_0[i] = Rxstr[i+1];
			}
			
    }
    
    else if (header == 'D'){
			for (i=0; i<9; i++) {
				Motor_1[i] = Rxstr[i+1];
			}
    }
    
    else if (header == 'E'){			
			for (i=0; i<9; i++) {
				Motor_2[i] = Rxstr[i+1];
			}
    }
		

}