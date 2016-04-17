#include <iostream>
#include <cassert>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <netinet/in.h>
#include <unistd.h>

#include "udp-config.h"
#include "mzcxx-utils.h"

using namespace std;

int main()
{
    sleep(2);

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    assert(sockfd > 0);
    struct sockaddr_in servaddr;
    struct sockaddr *addrp = (struct sockaddr*)&servaddr;
    
    memset(addrp, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(SERVER_IP);
    servaddr.sin_port = htons(SERVER_PORT_START + 3);

#define BUFLEN 1023
    char buf[BUFLEN + 1];
    strcpy(buf, "Hello\n");
    uint64_t i;
    while (true)
    {
	sendto(sockfd, buf, BUFLEN, 0, addrp, sizeof(servaddr));
    }

    //int res = bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    //assert(!res);

    return 0;
}


