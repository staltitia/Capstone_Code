/*
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

#include <fcntl.h>

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
	FILE* fp = 0;
	int flags = fcntl(fp, F_GETFL, 0);
	fcntl(fp, F_SETFL, flags | O_NONBLOCK); // makes read non-blocking
	char* presets = char* ( malloc(10 * sizeof(char) ) );
	char in_char = '\0';
	int changedFlag = '0';
	while(fp==0)
		fp = fopen ("/dev/uart", "r+");
	if (fp)
	{
		while (1)
		{
			update(fp, presets, &changedFlag);
			if (changedFlag)
			{
				for ( i = 0; i < 5; i++)
				{
					alt_avalon_spi_command(S_DAC1_BASE,i+2,
									   0x07, presets[i+2],
									   0, spi_command_string_rx,
									   0x01);
				}
				alt_avalon_spi_command(S_DAC1_BASE,7,
								   0x07, presets[7],
								   0, spi_command_string_rx,
								   0x0);
			}
		}
	}
	fclose (fp);
	return 0;
}

int update(FILE* serial, char* presets, int* flag) //serial is our serial connection
{
	char in_char;
	if not (in_char = fgetc(serial))	// Get a character from the UART. Returns -1 if no character to read 
		return 0;
	/* types of packets */
	/*
	To DE2: status packet
	1 byte: 
	[ 11110000 ]

	From DE2: hardcoded version number and ready signal
	19 bytes: (in ascii)
	VERSION 0.1, READY\n
	*/
	// 0b11110000 = 240
	if ( 240 == unsigned(in_char) )
	{
		//send back ready signal
		1+1;
	}
	/*
	To DE2: confirm packet
	1 byte:
	[ 11110001 ]
	From DE2: n/a
	*/
	// 0b11110001 = 241
	else if ( 241 == unsigned(in_char) )
	{
		//confirm previous changes
		1+1;
	}
	/*
	To DE2: cancel packet
	1 byte:
	[ 11110010 ]
	From DE2: n/a
	*/
	// 0b11110010 = 242
	else if ( 242 == unsigned(in_char) )
	{
		//discard previous changes
		1+1;
	}
	/*
	To DE2: presets packet
	(2n + 2) bytes, where n is number of variables:
	[ 11110100 (var_1) (var_val) (var_2) (var_val) ... (var_n) (var_val) ascii(\n) ]

	mode: 00000001
	[ photo, slow1, slow2, fast, TV ] = [ 00000001, 00000010, 00000100, 00001000, 00010000 ]
	inType: 00000010
	[ secondaryElectrons, X-Ray, auxiliary ] = [ 00000001, 00000010, 00000100 ]

	[ xShift, yShift, xStig, yStig, condLens, objLens, filaCurr, magni ] = [ 00000011, 00000100, 00000101, 00000110, 00000111, 00001000, 00001001, 00001010 ]
	
	From DE2: checksum
	1 byte:
	[ (checksum) ]
	*/
	// 0b11110100 = 244
	else if ( 244 == unsigned(in_char) )
	{
		*flag = 1;
		while(1)
		{
			if not (in_char = fgetc(serial))	// Get a character from the UART. Returns -1 if no character to read 
				return 0;
			if ( '\n' == in_char ) //then we're done
				break;
			index = unsigned(in_char) - 1;
			if ( 0 <= index && 9 >= index )
			{
				if not (in_char = fgetc(serial))	// Get a character from the UART. Returns -1 if no character to read 
					return 0;
				presets[index] = in_char;
			}
		}
	}

	/*
	To DE2: screenshot request packet

	1 byte:
	[ 11111000 ]
	
	From DE2: image data
	n + 4 bytes, wher n is the number of pixels:
	[ 00001111 (num rows) (num columns) (pixel_1) (pixel_2) ... (pixel_n) ascii(\n) ]
	*/
	// 0b11111000 = 248
	else if ( 248 == unsigned(in_char) )
	{
		1+1;
		// request image data
	}
	else
		return 0;
}