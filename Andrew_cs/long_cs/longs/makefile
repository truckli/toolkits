CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I /media/D/Nutstore/Softwares/ztoolkit
OBJS=zlongs.o
all:longs
longs:$(OBJS)
	$(CC) $(CFLAGS) -o $@ $^
*.o:*.c
	$(CC) $(CFLAGS) -c $< ;
touch:
	touch *.c;
clean:
	rm -f *.o;
	rm longs;
run:all
	./longs
