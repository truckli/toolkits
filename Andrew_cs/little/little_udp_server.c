#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <strings.h>
#include <stdio.h>
#include <assert.h>
#include <sys/socket.h>
#include <sys/times.h>
#include <time.h>
#include <netinet/in.h>

int main(int argc, char* argv[])
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    assert(sockfd > 0);
    struct sockaddr_in servaddr, cliaddr;
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(8866);

    int res = bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    assert(!res);
#define BUFLEN 1023
    char buf[BUFLEN + 1];

    time_t last_sec = time(NULL); 

    uint64_t recv_total = 0;
    while (1)
    {
	socklen_t socklen = sizeof(cliaddr);
	int nrecv = recvfrom(sockfd, buf, BUFLEN, 0, (struct sockaddr*)&cliaddr, &socklen);
	if (nrecv > 0) 
	{
	    recv_total += (uint64_t)nrecv;
	}
	else exit(1);

	time_t now_sec = time(NULL);
	if (now_sec - last_sec > 2)
	{
	    printf("Current recv : %llu bytes\n", (unsigned long long)recv_total);
	    last_sec = now_sec;
	}

    }

    close(sockfd);

    return 0;
}
