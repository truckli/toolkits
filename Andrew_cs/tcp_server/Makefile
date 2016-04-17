CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I ~/Apps/ztoolkit/
all:simple_server
simple_server:zsimple_server.o
	$(CC) -o $@ $^ 
	sshpass -p lmz scp $@ limz@192.168.130.130:~

%.o : %.c
	$(CC) -c $< 

touch:
	touch *.c;
clean:
	rm -f *.o;
run:all
	./simple_server
