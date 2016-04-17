/*  Make the necessary includes and set up the variables.  */

#include <sys/types.h>
#include <sys/socket.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <ctype.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>


#define TCP_PORT_SERVER 5896

int main()
{
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;

/*  Remove any old socket and create an unnamed socket for the server.  */

    server_sockfd = socket(AF_INET, SOCK_STREAM, 0);

/*  Name the socket.  */

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(TCP_PORT_SERVER);
    server_len = sizeof(server_address);
    bind(server_sockfd, (struct sockaddr *)&server_address, server_len);

/*  Create a connection queue and wait for clients.  */

    listen(server_sockfd, 5);
    while(1) 
    {

        printf("**********************************************\n");

/*  Accept a connection.  */

	client_len = sizeof(client_address);
	client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_address, &client_len);

	/*  We can now read/write to client on client_sockfd.  */
	char buf[256];	
	int nrecv;

	errno = 0;
	nrecv = recv(client_sockfd, buf, 255, 0);

	if (nrecv == 0)
	{
	    printf("End of client data. Shutting down ....\n");
	    close(client_sockfd);
	    break;
	}

	if (nrecv < 0)
	{
	    perror("Server receive error");
	    if (errno != EAGAIN)
	    {
		close(client_sockfd);
		break;
	    }
	    else
		continue;
	}

	printf("client msg:%s\n", buf);
	char sendmsg[1024];

	uint64_t i;
	for (i=0; i<10; i++)
	{
	    printf("Send msg to client ");
	    send(client_sockfd, sendmsg, 1024, 0);
	}

	close(client_sockfd);

    }
}

