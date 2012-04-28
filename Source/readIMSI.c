#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
static int fd;
long BAUD = B9600;
long DATABITS = CS8;
long STOPBITS = 0;
long PARITYNO = 0;
long PARITY = 0;

int main ( int argc , char** argv )
{
  struct termios oldtio,newtio;
  int i ,cmd,bytes,count=0;
  char devname[32];
  char message[1024];
  for ( i = 1 ; i < argc ; i++ )
	{
	  if ( strcmp("-p",argv[i])==0 )
		{
		  i++;
		  strcpy(devname,argv[i]);
		}
	  else
		{
		  fprintf(stderr,"-p serial device name\n");
		}
	}
  fd = open ( devname , O_RDWR | O_NOCTTY | O_NONBLOCK);
  if ( fd < 0 )
	{
	  perror("serial open");
	  exit(-1);
	}
  tcgetattr(fd,&oldtio);
  memset((char *) &newtio,0, sizeof(newtio));	
  //bzero(&newtio,sizeof(newtio));
  newtio.c_cflag = BAUD |CRTSCTS|CLOCAL | CREAD;
  newtio.c_iflag = IGNPAR|ICRNL;
  newtio.c_oflag = 0;
  newtio.c_lflag = ICANON;
  newtio.c_cc[VMIN] = 1;
  newtio.c_cc[VTIME] = 0;
  newtio.c_cc[VEOF]  = 4;
  tcflush(fd,TCIFLUSH);
  tcsetattr(fd,TCIFLUSH,&newtio);

  /*
	 write cmd
   */
/*
  switch (cmd)
	{
	case 1:
	  strcpy(message,"AT+CSQ");
	  break;
	default:
	  break;
	}
*/	
  strcpy(message,"AT+CIMI\r\n");
  bytes = write(fd,message,strlen(message));
  /**************************************
   * read same
   */

  do
	{
	  //if ( wait_fd_read == 1 )
		{
		  int bytes = read(fd,message,12);
		  if ( bytes > 0 )
			{
			  if ( message[0]=='4' && message[1]=='6')
				{
				  printf("%s",message);
				  break;
				}
			}
		  else
			sleep(1);
		  count++;
		}
	  //else
		//sleep(1);

	}while(count < 10 );

  tcsetattr(fd,TCSANOW,&oldtio);
  close(fd);
}
