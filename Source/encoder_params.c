#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

void error(const char *msg)
{
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[])
{
    int sockfd, portno, n, reactive=0;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[256];
    if (argc < 5) {
       fprintf(stderr,"usage %s hostname port action(2,3) cmdString reactive(0,1)\n", argv[0]);
       exit(0);
    }

    portno = atoi(argv[2]);
    if (argc == 6)
    	reactive = atoi(argv[5]);
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0) 
        error("ERROR opening socket");
    server = gethostbyname(argv[1]);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(portno);
    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) 
        error("ERROR connecting");

    bzero(buffer,256);
    //fgets(buffer,255,stdin);
    //char *cmd = "enc0.vid_bitrate\nenc0.vid_input\nenc0.aud_bitrate\nenc0.vid_in\n";
    char action = atoi(argv[3]);
    char *cmd = argv[4];
    char cmdLen = strlen(cmd);
    int i;
    for(i = 0; i < cmdLen; i++) {
    	if(cmd[i] == '|') cmd[i] = '\n';
    }

    buffer[1] = action;
    buffer[3] = cmdLen;
    memcpy(buffer + 4,cmd,cmdLen); 
    n = write(sockfd,buffer,cmdLen+4);
    if (n < 0) 
         error("ERROR writing to socket");
    bzero(buffer,256);
    n = read(sockfd,buffer,255);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("%s",buffer+6);
    if (action == 3) {
    	bzero(buffer,256);
		buffer[1] = 4;
		buffer[3] = 2;
		buffer[5] = 4;
		n = write(sockfd,buffer,6);
		if(reactive == 1) {
			buffer[5] = 7;
			n = write(sockfd,buffer,6);
		}
    }
    close(sockfd);

    return 0;
}
