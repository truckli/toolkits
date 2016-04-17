CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I ~/Apps/ztoolkit/
all:simple_bif
simple_bif:zsimple_bif.c
	$(CC) -o simple_bif zsimple_bif.c ;
touch:
	touch *.c;
clean:
	rm -f *.o;
run:all
	./simple_bif
