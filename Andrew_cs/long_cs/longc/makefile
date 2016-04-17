CC=gcc
CFLAGS=-g -DZ_DEBUG_PRTVAR -I /media/D/Nutstore/Softwares/ztoolkit
OBJS=zlongc.o
all:longc
longc:$(OBJS)
	$(CC) $(CFLAGS) -o $@ $^
*.o:*.c
	$(CC) $(CFLAGS) -c $< ;
touch:
	touch *.c;
clean:
	rm -f *.o;
	rm longc;
run:all
	./longc
