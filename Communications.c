/*/*
 * SPI Test code.
 * License. Do whatever you want with the code. Just remember my name :)
 * Author : Zubair Lutfullah Kakakhel. But most of this comes from scattered forum posts..
 * Email : EL12ZLK@LEEDS.AC.UK
 */
#include "alt_types.h"
#include "sys/alt_stdio.h"
#include "io.h"
#include "system.h"
#include "sys/alt_cache.h"
#include <stdio.h>
#include "altera_avalon_spi.h"
#include "altera_avalon_spi_regs.h"
#include "sys/alt_irq.h"
//This is the ISR that runs when the SPI Slave receives data
//static void spi_rx_isr(void* isr_context){
// alt_printf("ISR :) %x \n" ,  IORD_ALTERA_AVALON_SPI_RXDATA(SPI_SLAVE_BASE));
        //This resets the IRQ flag. Otherwise the IRQ will continuously run.
// IOWR_ALTERA_AVALON_SPI_STATUS(SPI_SLAVE_BASE, 0x0);
//
//}
#define SPI_MASTER_BASE (char *) 0x00109040
#define switches (volatile char *) 0x0109060
#define DAC_BASE (char *) 0x109020
#define SDRAM_BASE2 (char *) 0x08000000
#define leds (char *) 0x00109030
int main()
{
  //printf("Hello from Nios II!\n");
  FILE* fp;
  int trig;
  char in_char = 0;
//int pointer = 0;
  //char weight[1000];
  char *tx_addr;
  char spi_command_string_rx[8] = "cbcdefxy";
  fp=0;
  while(fp==0) {
  fp = fopen ("/dev/uart", "r+");
//  //Open file for reading and writing
 // if (fp ==0){
//   //printf("error");
 // }
  }
  trig = 0;
  if (fp){
   //printf("opened");
  // *leds = *switches;
   while (1){
    in_char = fgetc(fp); // Get a character from the UART.
    //printf("in char is: %c\n",in_char);
    if (in_char == 'a'){
     //printf("received 'a'");
    if (trig == 0) {
     *DAC_BASE = 0x01;
    } else {
     *DAC_BASE = 0x00;
    }
    }
    else if (in_char == 'b') {
    // printf("received 'b'");
     in_char = fgetc(fp);
    // printf("in char is: %c\n",in_char);
     *SDRAM_BASE2 = in_char;
     tx_addr = SDRAM_BASE2;
     tx_addr++;
     in_char = fgetc(fp);
     *tx_addr = in_char;

     alt_avalon_spi_command(S_DAC1_BASE,0,
                                   0x07, *SDRAM_BASE2,
                                   0, spi_command_string_rx,
                                   0x01);
     alt_avalon_spi_command(S_DAC1_BASE,0,
                                   0x07, *tx_addr,
                                   0, spi_command_string_rx,
                                   0x0);
    }
    else if (in_char == 'c') {
    // printf("received 'c'");
      in_char = fgetc(fp);
       // printf("in char is: %c\n",in_char);
        *SDRAM_BASE2 = in_char;
        tx_addr = SDRAM_BASE2;
        tx_addr++;
        in_char = fgetc(fp);
        *tx_addr = in_char;
         alt_avalon_spi_command(S_DAC1_BASE,1,
                                       0x07, *SDRAM_BASE2,
                                       0, spi_command_string_rx,
                                       0x01);
         alt_avalon_spi_command(S_DAC1_BASE,1,
                                       0x07, *tx_addr,
                                       0, spi_command_string_rx,
                                       0x0);
    }
    else if (in_char == 'd') {
     in_char = fgetc(fp);
           // printf("in char is: %c\n",in_char);
            *SDRAM_BASE2 = in_char;
            tx_addr = SDRAM_BASE2;
            tx_addr++;
            in_char = fgetc(fp);
            *tx_addr = in_char;
             alt_avalon_spi_command(S_DAC1_BASE,2,
                                           0x07, *SDRAM_BASE2,
                                           0, spi_command_string_rx,
                                           0x01);
             alt_avalon_spi_command(S_DAC1_BASE,2,
                                           0x07, *tx_addr,
                                           0, spi_command_string_rx,
                                           0x0);
    } else if (in_char == 'e') {
     in_char = fgetc(fp);
           // printf("in char is: %c\n",in_char);
            *SDRAM_BASE2 = 0x96;
            tx_addr = SDRAM_BASE2;
            tx_addr++;
            //in_char = fgetc(fp);
            *tx_addr = 0xDC;
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x07, *SDRAM_BASE2,
                                           0, spi_command_string_rx,
                                           0x01);
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x07, *tx_addr,
                                           0, spi_command_string_rx,
                                           0x0);
    } else if (in_char == 'f') {
     in_char = fgetc(fp);
           // printf("in char is: %c\n",in_char);
            *SDRAM_BASE2 = in_char;
            tx_addr = SDRAM_BASE2;
            tx_addr++;
            in_char = fgetc(fp);
            *tx_addr = in_char;
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x08, *SDRAM_BASE2,
                                           0, spi_command_string_rx,
                                           0x01);
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x08, *tx_addr,
                                           0, spi_command_string_rx,
                                           0x0);
    } else if (in_char == 'g') {
     in_char = fgetc(fp);
           // printf("in char is: %c\n",in_char);
            *SDRAM_BASE2 = in_char;
            tx_addr = SDRAM_BASE2;
            tx_addr++;
            in_char = fgetc(fp);
            *tx_addr = in_char;
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x07, 0x96,
                                           0, spi_command_string_rx,
                                           0x01);
             alt_avalon_spi_command(S_DAC1_BASE,0,
                                           0x07, 0xDC,
                                           0, spi_command_string_rx,
                                           0x0);
    }else if (in_char == 'h') {
     *leds=*switches;
    }else if (in_char == 'j') {
     while(1){
     *SDRAM_BASE2 = 0x96;
        tx_addr = SDRAM_BASE2;
        tx_addr++;
        //in_char = fgetc(fp);
        *tx_addr = 0xDC;

        alt_avalon_spi_command(S_DAC1_BASE,0,
                                      0x07, *SDRAM_BASE2,
                                      0, spi_command_string_rx,
                                      0x01);
        alt_avalon_spi_command(S_DAC1_BASE,0,
                                      0x07, *tx_addr,
                                      0, spi_command_string_rx,
                                      0x0);
     }
    }

   }
   }
 //  printf("closed");
   fclose (fp);
   return 0;
  }     //   return 0;