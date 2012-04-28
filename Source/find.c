 #include <sys/types.h>
 #include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdlib.h>
//#include <signal.h>


#define MAXLINE 80
int port = 8712;

int main(void)
{
	struct sockaddr_in sin;
	struct sockaddr_in rin;
	int sock_fd;
	socklen_t address_size;
	char buf[MAXLINE];
	char str[INET_ADDRSTRLEN];
	int i;
	int len;
	int n;

	bzero(&sin, sizeof(sin));
	sin.sin_family = AF_INET;
	sin.sin_addr.s_addr = INADDR_ANY;
	sin.sin_port = htons(port);
	sock_fd = socket(AF_INET, SOCK_DGRAM, 0);
	if (-1 == sock_fd)
	{
		perror("call to socket");
		exit(1);
	}
	n = bind(sock_fd, (struct sockaddr *)&sin, sizeof(sin));
	if (-1 == n)
	{
		perror("call to bind");
		exit(1);
	}

	/*
	bzero(&mreq, sizeof(struct ip_mreq));
	if ((group = gethostbyname(b_addr)) == (struct hostent *) 0) {
		perror("gethostbyname");
		exit(errno);
	}
	bcopy((void *) group->h_addr, (void *) &ia, group->h_length);
	bcopy(&ia, &mreq.imr_multiaddr.s_addr, sizeof(struct in_addr));
	mreq.imr_interface.s_addr = htonl(INADDR_ANY);

	if (setsockopt(sock_fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq,sizeof(struct ip_mreq)) == -1) {
		perror("setsockopt");
		exit(-1);
	}
	*/
	const int on = 1;
	if (setsockopt(sock_fd,SOL_SOCKET,SO_BROADCAST,&on,sizeof(on)) == -1) {
		perror("setsockopt");
		exit(-1);
	}

	while(1)
	{
		address_size = sizeof(rin);
		n = recvfrom(sock_fd, buf, MAXLINE, 0, (struct sockaddr *)&rin, &address_size);
		if (-1 == n)
		{
			perror("call to recvfrom.\n");
			//exit(1);
		}
		printf("you ip is %s at port %d:%s\n",inet_ntop(AF_INET, &rin.sin_addr,str,sizeof(str)),ntohs(rin.sin_port),buf);
	}
}
