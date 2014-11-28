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
  
#define SDRAM_BASE (char *) 0x008f0000
#define IMG_PTR (char *) 0x00000000
  
int main() 
{ 
    FILE* fp = 0; 
    unsigned int* values = (int*) SDRAM_BASE; 
    unsigned int* compare = (int*) SDRAM_BASE + sizeof(unsigned int) * 10;
    unsigned char* txPtr = (unsigned char*) SDRAM_BASE + sizeof(unsigned int) * 20;
    char spi_command_string_rx[8] = "Rubbish";
    int width = 640; 
    int height = 480; 
    int i; 
      
    while(fp==0)  
        fp = fopen ("/dev/uart", "r+"); 
      
    if (fp) 
    { 
        while (1) 
        { 
            update(fp, values, width, height, IMG_PTR) 
            for (i=0; i<10; ++i) 
            { 
                if (values[i] != compare[i]) 
                {
                    switch(i)
                    {
                        case 2:
							unsigned base = 0x9000;
							toWrite = (values[i]%256)<<4;
							base += toWrite;
							txPtr[0] = (unsigned char) base / 256;
							txPtr[1] = (unsigned char) base % 256;
							alt_avalon_spi_command( SPI_MASTER_BASE, 0, 0x02, txPtr, 0, spi_command_string_rx, 0x00);
                            break;
                        case 3:
							base = 0xA000;
							toWrite = (values[i]%256)<<4;
							base += toWrite;
							txPtr[0] = (unsigned char) base / 256;
							txPtr[1] = (unsigned char) base % 256;
							alt_avalon_spi_command( SPI_MASTER_BASE, 0, 0x02, txPtr, 0, spi_command_string_rx, 0x00);
                            break;
                        case 4:
							base = 0x9000;
							toWrite = (values[i]%256)<<4;
							base += toWrite;
							txPtr[0] = (unsigned char) base / 256;
							txPtr[1] = (unsigned char) base % 256;
							alt_avalon_spi_command( SPI_MASTER_BASE, 1, 0x02, txPtr, 0, spi_command_string_rx, 0x00);
                            break;
                        case 5:
			    base = 0xA000;
							toWrite = (values[i]%256)<<4;
							base += toWrite;
							txPtr[0] = (unsigned char) base / 256;
							txPtr[1] = (unsigned char) base % 256;
							alt_avalon_spi_command( SPI_MASTER_BASE, 1, 0x02, txPtr, 0, spi_command_string_rx, 0x00);
                            break;

                    }
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
    if ( 240 == (unsigned int) in_char)         //0b11110000 status 
        1+1; 
    else if ( 241 == (unsigned int) in_char)    //0b11110001 confirm 
        1+1; 
    else if ( 242 == (unsigned int) in_char)    //0b11110010 cancel 
        1+1; 
    else if ( 244 == (unsigned int) in_char)    //0b11110100 presets packet 
    { 
        while(1) 
        {             
	    in_char = fgetc(fp); 
            if (in_char == '\n') 
                break; 
            int index = (unsigned int) in_char - 1; 
            in_char = fgetc(fp); 
            if (in_char == '\n') 
                break; 
            int value = (unsigned int) in_char; 
            values[index] = value; 
        } 
    } 
    else if ( 248 == (unsigned int) in_char)    //0b11111000 image request 
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
