#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdlib.h>

#define MAXLINE 80
int port = 8812;

int main(void)
{
	struct sockaddr_in pin;
	struct sockaddr_in rin;
	int sock_fd;
	char buf[MAXLINE];
	char str[6] = "*find*";
	char sip[INET_ADDRSTRLEN];
	char *b_addr = "255.255.255.255";
	int n;
	int address_size;

	bzero(&pin, sizeof(pin));
	pin.sin_family = AF_INET;
	inet_pton(AF_INET, b_addr, &pin.sin_addr);
	pin.sin_port = htons(port);

	sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
	if (-1 == sock_fd)
	{
		perror("call to socket");
		exit(1);
	}

	const int on = 1;
	if (setsockopt(sock_fd,SOL_SOCKET,SO_BROADCAST,&on,sizeof(on)) == -1) {
		perror("setopt");
		exit(1);
	}

	//while(NULL != fgets(str,MAXLINE, stdin)) 
	//{
		sendto(sock_fd, str, 6 , 0, (struct sockaddr *)&pin, sizeof(pin));
		if (-1 == n)
		{
			perror("call to sendto.\n");
			exit(1);
		}

		address_size = sizeof(rin);
		n = recvfrom(sock_fd, buf, MAXLINE, 0, (struct sockaddr *)&rin, &address_size);
		if (-1 == n)
		{
			perror("call to recvfrom.\n");
			exit(1);
		}
		else
		{
			printf("Response from %s port %d:%s\n",
			inet_ntop(AF_INET, &rin.sin_addr, sip, sizeof(sip)),
			ntohs(rin.sin_port),buf);
		}
	//}	
	close(sock_fd);
	if (-1 == n)
	{
		perror("call to close.\n");
		exit(1);
	}
	return 0;
}
