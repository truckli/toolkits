CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I ~/Apps/ztoolkit/
all:crazy_server
crazy_server:zcrazy_server.c
	$(CC) -o crazy_server zcrazy_server.c ;
touch:
	touch *.c;
clean:
	rm -f *.o;
run:all
	./crazy_server
