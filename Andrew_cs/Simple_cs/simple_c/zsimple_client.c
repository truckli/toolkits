#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define IP_ADDR_DEEPIN ((192<<24)|(168<<16)|(130<<8)|224)
#define TCP_PORT_DEEPIN_SERVER 5896

int Recv(int sockfd, void *buf, size_t len, int flags)
{
    while (1)
    {
	errno = 0;
	int res = recv(sockfd, buf, len, flags);
	if (res > 0) return res;
	
	if (res < 0 && errno == EAGAIN)
	    continue;

	return res;
    }
}

int main()
{
    int sockfd;
    struct sockaddr_in address;
    int result;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(IP_ADDR_DEEPIN);
    /*address.sin_addr.s_addr = htonl(0xc0a882e1);*/
    address.sin_port = htons(TCP_PORT_DEEPIN_SERVER);

    if (-1 == connect(sockfd, (struct sockaddr *)&address, sizeof(address)))
    {
	printf("Simple client :Connection refused\n");	
        exit(1);
    }

    const char* req_msg1 = "The first msg";

#define BUF_LEN 255
    char buf[BUF_LEN + 1];
    int len;
    int revflag = 0;
    

    send(sockfd, req_msg1, strlen(req_msg1), 0);

    len = Recv(sockfd, buf, BUF_LEN, revflag);
    if (len <= 0)
    {
	close(sockfd);
	exit(1);
    }

    buf[len] = '\0';
    printf("Server msg:%s\n", buf);

    close(sockfd);
    exit(0);
}
