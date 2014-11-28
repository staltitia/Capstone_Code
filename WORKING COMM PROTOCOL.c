#include "alt_types.h"
#include "sys/alt_stdio.h"
#include "io.h"
#include "system.h"
#include "sys/alt_cache.h"
#include <stdio.h>
#include "altera_avalon_spi.h"
#include "altera_avalon_spi_regs.h"

#include "sys/alt_irq.h"

#define SPI_MASTER_BASE (char *) 0x00109040
#define switches (volatile char *) 0x0109060
#define DAC_BASE (char *) 0x109020

#define SRAM_BASE2 (char *) 0x00080000
#define SDRAM_BASE (char *) 0x00800000

int main()
{
	FILE* fp = 0;
	int* values = (int*) SDRAM_BASE;
	int* compare = (int*) SDRAM_BASE + sizeof(int) * 10;
	int width = 640;
	int height = 480;
	int i;
	
	while(fp==0) 
		fp = fopen ("/dev/uart", "r+");
	
	if (fp)
	{
		while (1)
		{
			update(fp, values, width, height, imagePtr)
			for (i=0; i<10; ++i)
			{
				if (values[i] != compare[i])
				{
					printf("Value %i is %i", i, values[i]);
					compare[i] = values[i];
				}
			}
		}
	}
	
	fclose (fp);
	return 0;
}     //   return 0;

void update( FILE* fp, int* values, int width, int height, char* imagePtr )
{
	unsigned char in_char = fgetc(fp)
	if ( 240 == (unsigned int) in_char)			//0b11110000 status
		1+1;
	else if	( 241 == (unsigned int) in_char)	//0b11110001 confirm
		1+1;
	else if	( 242 == (unsigned int) in_char)	//0b11110010 cancel
		1+1;
	else if	( 244 == (unsigned int) in_char)	//0b11110100 presets packet
	{
		while(1)
		{
			in_char = fgetc(fp);
			if (in_char = '\n')
				break;
			index = (unsigned int) in_char - 1;
			in_char = fgetc(fp);
			value = (unsigned int) in_char;
			values[index] = value;
		}
	}
	else if	( 248 == (unsigned int) in_char)	//0b11111000 image request
	{
		// identifier is 0b00001111 = 15
		fputc( 15, fp );
		
		// width is the next two bytes
		fputc( width / 256, fp );
		fputc( width % 256, fp );
		
		// height is the next two bytes
		fputc( height / 256, fp );
		fputc( height % 256, fp );
		
		int i;
		for ( i = 0; i < height*width; ++i )
			fputc( imagePtr[i], fp );
	}
	else
		return;
}