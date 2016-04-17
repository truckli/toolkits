#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define IP_ADDR_DEEPIN ((192<<24)|(168<<16)|(130<<8)|130)
#define TCP_PORT_DEEPIN_SERVER 9999

int main()
{
    int sockfd;
    int len;
    struct sockaddr_in address;
    int result;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(IP_ADDR_DEEPIN);
    /*address.sin_addr.s_addr = htonl(0xc0a882e1);*/
    address.sin_port = htons(TCP_PORT_DEEPIN_SERVER);
    len = sizeof(address);

    if (-1 == connect(sockfd, (struct sockaddr *)&address, len))
    {
	printf("Andrew client:Connection refused\n");	
        exit(1);
    }

    char* req_msg = "Hi! This is a linux host";
    char buf[1024];
    send(sockfd, req_msg, strlen(req_msg), 0);
    len = read(sockfd, buf, 1024);
    buf[len] = '\0';

    printf("Receive server:\n %s\n", buf);
    write(sockfd, req_msg, strlen(req_msg));
    close(sockfd);
    exit(0);
}
