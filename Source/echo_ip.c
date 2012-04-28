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
int port = 8812;
int send_port = 8712;

int main(void)
{
	struct sockaddr_in sin;
	struct sockaddr_in rin;
	//struct in_addr ia;
	//struct hostent *group;
	//struct ip_mreq mreq;
	int sock_fd;
	socklen_t address_size;
	char buf[MAXLINE];
	char str[INET_ADDRSTRLEN];
    char *b_addr = "255.255.255.255";	
	//char *bs_addr = "255.255.255.255";
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
		len = strlen(buf);
		if(  6 <= len && buf[0] == '*' && buf[1] == 'f' && buf[2] == 'i' && buf[3] == 'n' && buf[4] == 'd' && buf[5] == '*'  )
		{
			inet_pton(AF_INET, b_addr, &rin.sin_addr);
			rin.sin_port = htons(send_port);
		//for (i = 0; i < len; i++)
		//{
		//	buf[i] = toupper(buf[i]);
		//}
			n = sendto(sock_fd,buf,1,0, (struct sockaddr *)&rin, address_size);
			if (-1 == n)
			{
				perror("call to sendto\n");
		//	exit(1);
			}
		}
	}
}
