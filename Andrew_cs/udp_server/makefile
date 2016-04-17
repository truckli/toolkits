CC=g++
TOOLKIT:=~/Coding/Toolkit
CFLAGS=-g -DZ_DEBUG_PRTVAR -I $(TOOLKIT)/mzcxx/include
LDFLAGS=-L $(TOOLKIT)/mzcxx/lib -pthread

APPS=client server

all:$(APPS) 

client:client.o
server:server.o

%:%.o
	$(CC) $(LDFLAGS) -o $@ $^ -lmzcxx 

%.o:%.cpp
	$(CC) $(CFLAGS) -c $< 

.PHONY: run
run: $(APPS)
	./server &
	./client
	killall server

touch:
	touch *.cpp

upload:
	sshpass -p lmz scp server limz@192.168.130.194:~

.PHONY: kill 
kill:
	killall $(APPS)

.PHONY: clean 
clean:
	-rm -f $(APPS) *.o


