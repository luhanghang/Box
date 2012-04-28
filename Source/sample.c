#include     <stdio.h>
#include     <string.h>
#include     <stdlib.h>
#include     <unistd.h>
#include     <sys/types.h>
#include     <sys/stat.h>
#include     <fcntl.h>
#include     <termios.h>
#include     <errno.h>

#define DEV_NAME "/dev/ttyUSB0"
#define OUTPUT_LCD 1
char buff[256];

#define SEARCH_NETWORK_CMD_1 "AT^SYSINFO\r\n"
#define SEARCH_NETWORK_CMD_2 "AT+COPS?\r\n"
#define SEARCH_NETWORK_ERR_1 1001
#define SEARCH_NETWORK_ERR_2 1002

#define CONNECT_NETWORK_CMD_1 "AT+CGDCONT=1,\"IP\",,,\r\n"
#define CONNECT_NETWORK_CMD_2 "AT+CGACT=1,1\r\n"
#define CONNECT_NETWORK_ERR_1 2001
#define CONNECT_NETWORK_ERR_2 2002

#define DISCON_NETWORK_CMD "AT+CGACT=0,1\n"
#define DISCON_NETWORK_ERR 3001

#define TRY_SN_TIMES    10
#define TRY_CONT_TIMES  10

/* Since our UART is USB-simulated-UART, so speed and parity are
not so important, just HARD-CODED to 115200,8,N,1
Speed is 115200,
No parity
8 data bit
1 stop bit
*/
#define BAND_RATE B115200
static int init_uart(int fd)
{
	int status;
	struct termios options;
	
	tcflush(fd, TCIOFLUSH);

	if (0 != tcgetattr(fd,&options)) {
  		printf("%s report: setup serial failed!", __FILE__);
  		return -1;
	}

	/*Don't need terminal functions*/
	options.c_lflag  &= ~(ICANON | ECHO | ISIG);  /*Input*/
	options.c_oflag  &= ~OPOST;   /*Output*/

	/*Set band-rate 115200 8N1 */
	cfsetispeed(&options, BAND_RATE);
	cfsetospeed(&options, BAND_RATE);
	options.c_cflag |= CS8;	/*8-bit data*/
	options.c_cflag &= ~PARENB;	/* Clear parity enable */
	options.c_iflag &= ~INPCK;	/* Enable parity checking */
	options.c_cflag &= ~CSTOPB;	/* one stop bit */

	if (0 != tcsetattr(fd, TCSANOW, &options)) {
		printf("%s report: set speed error!", __FILE__);
		return -1;
	}

	printf("== Set USB-UART ok ==\n");
	return 0;
}

/* Search network procedure:
1. AT^SYSINFO

If things goes well, LTE modem should return:
^SYSINFO:2,2,0,17,1,,25
	
or you have to resend the commands, untill get the right answer.
*/
static int search_network(int fd)
{
	unsigned long len;
	int try = 0;

	for (try = 0; try < TRY_SN_TIMES; try++) {
		printf("Search net work now, try <%d>: \n", try + 1);
		len = write(fd, SEARCH_NETWORK_CMD_1, strlen(SEARCH_NETWORK_CMD_1));
		printf("Command:  %sWrite   %lu chars\n", SEARCH_NETWORK_CMD_1, len);
		sleep(3);

		memset(buff, 0, sizeof(buff));
		read(fd, buff, 256);
		printf(" response: %s\n", buff);
		printf("-----------------\n");

		if (strstr(buff, "OK") != NULL) {
			printf("Check the sys info\n");
			if (strstr(buff, "^SYSINFO:2,2") != NULL) {
				break;
			}
			if (strstr(buff, "^SYSINFO:16,2") != NULL) {
				break;
			}
		}
	}
	
	if (try >= TRY_SN_TIMES) {
		printf("Search_network failed in step-1\n");
		return SEARCH_NETWORK_ERR_1;
	}

	printf("Search network OK!\n");

	return 0;
}
/* Procedure of connect to network
1. AT+CGDCONT=1,"IP",,,
2. AT+CGACT=1,1
After step-2, LTE modem will connect to network automatically,
if it successfully connets to network, it return "OK",
User should send the command repeatly until LTE returns "OK"
*/

static int connect_network(int fd)
{
	unsigned long len;
        int try;

	len = write(fd, CONNECT_NETWORK_CMD_1, strlen(CONNECT_NETWORK_CMD_1));
	printf("Command\n[\n");
	printf("%s] write %lu chars\n", CONNECT_NETWORK_CMD_1, len);

	sleep(1);
	memset(buff, 0, sizeof(buff));
	read(fd, buff, 256);
	printf("Response: %s\n", buff);
	printf("-----------------\n");

	if (NULL == strstr(buff, "OK")) {
		printf("Connect network failed in step-1\n");
		return CONNECT_NETWORK_ERR_1;
	}
	
	for(try = 0; try < TRY_CONT_TIMES; try++) {
		printf("Connet Net Try < %d > times\n", try + 1); 
		len = write(fd, CONNECT_NETWORK_CMD_2, strlen(CONNECT_NETWORK_CMD_2));

		printf("Command\n[\n");
		printf("%s] write %lu chars\n", CONNECT_NETWORK_CMD_2, len);
	
		sleep(3);
		memset(buff, 0, sizeof(buff));
		read(fd, buff, 256);
		printf("Response: %s\n", buff);
		printf("-------------------\n");
		if (strstr(buff, "OK") != NULL) {
			break;
		}
	}
	
	if(try >= TRY_CONT_TIMES) {
		printf("Connect network failed in step-2\n");
		return CONNECT_NETWORK_ERR_2;
	} else {
		printf("Connect network OK\n");
	}

	return 0;	
}

static int turn_on_echo(int fd)
{
	write(fd, "ATE1\r\n", strlen("ATE1\r\n"));
	return 0;
}

static int turn_off_echo(int fd)
{
	write(fd, "ATE0\r\n",strlen("ATE0\r\n"));
}

int main(int argc, char **argv)
{
	int fd;
	int nread;

	printf("========= start test =========\n");
	fd = open(DEV_NAME, O_RDWR);
	if (fd > 0) {
		init_uart(fd);
	} else {
		printf("%s: Can't Open Serial Port!\n", __FILE__);
		exit(1);
	}

	turn_off_echo(fd);

	if (0 != search_network(fd)) {
		close(fd);	
		return 1;
	}
	
	if (0 != connect_network(fd)) {
		close(fd);
		return 1;
	}


	printf("============== start pppoe ===============\n");
	system("ifconfig usb0 up");
	sleep(1);
	system("pppd pty 'pppoe -I usb0' local noauth nodetach noaccomp nodeflate nopcomp  \
		novj novjccomp usepeerdns defaultroute logfile /tmp/pppd.log &");

	close(fd);
	return 0;
}
