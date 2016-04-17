CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I ~/Apps/ztoolkit/
all:simple_server
simple_server:zsimple_server.c
	$(CC) -o simple_server zsimple_server.c ;
touch:
	touch *.c;
clean:
	rm -f *.o;
run:all
	./simple_server
