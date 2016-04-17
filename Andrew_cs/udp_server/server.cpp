#include <cstdlib>
#include <unistd.h>
#include <stdint.h>
#include <cassert>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/select.h>
#include <ctime>
#include <cstring>
#include <pthread.h>
#include <netinet/in.h>


#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>
#include "udp-config.h"
#include "mzcxx-utils.h"

using namespace std;

class TimeSus
{
    friend class WallTimer;
    public:
    uint32_t tv_sec;
    uint32_t tv_usec;
    TimeSus(uint32_t sec, uint32_t usec):tv_sec(sec), tv_usec(usec) {}
};

class WallTimer
{
    public:
	static bool testTimeDiffSec(const TimeSus &first, const TimeSus &second, uint32_t secs)
	{
	    uint64_t usec1 = first.tv_sec * 1000000 + first.tv_usec; 
	    uint64_t usec2 = second.tv_sec * 1000000 + second.tv_usec; 
	    if (usec1 == usec2) return false;
	    uint64_t usecs_diff = (usec2 > usec1) ? (usec2 - usec1) : (usec1 - usec2);
	    return (usecs_diff >= (secs * 1000000));
	}

	static uint64_t getTimeDiffUsec(const TimeSus &first, const TimeSus &second)
	{
	    uint64_t usec1 = first.tv_sec * 1000000 + first.tv_usec; 
	    uint64_t usec2 = second.tv_sec * 1000000 + second.tv_usec; 
	    if (usec1 == usec2) return 0;
	    uint64_t usecs_diff = (usec2 > usec1) ? (usec2 - usec1) : (usec1 - usec2);
	    return usecs_diff;
	}

	static uint32_t getTimeDiffSec(const TimeSus &first, const TimeSus &second)
	{
	   return getTimeDiffUsec(first, second)/1000000; 
	}

	static TimeSus getTimeSus()
	{
	    struct timeval tv;
	    gettimeofday(&tv, NULL);
	    return TimeSus(tv.tv_sec, tv.tv_usec);
	}

	static uint64_t get_usec()
	{
	    struct timeval tv;
	    gettimeofday(&tv, NULL);
	    return tv.tv_sec * 1000000 + tv.tv_usec; 
	}

	static uint64_t getSec()
	{
	    struct timeval tv;
	    gettimeofday(&tv, NULL);
	    return tv.tv_sec; 
	}

	static uint64_t getMsec()
	{
	    struct timeval tv;
	    gettimeofday(&tv, NULL);
	    return tv.tv_sec * 1000; 
	}

	static std::string makeTimeIntvStr(uint64_t usec1, uint64_t usec2)
	{
	    if (usec1 == usec2) return std::string("(Zero time)");
	    uint64_t usecs = (usec2 > usec1) ? (usec2 - usec1) : (usec1 - usec2);
	    std::ostringstream oss;
	    oss << " ";
	    if (usecs < 1000)
	    {
		oss << usecs << "us" << std::endl;
	    }
	    else 
	    {
		uint64_t msecs = usecs / 1000;
		if (msecs < 1000)
		{
		    usecs %= 1000;
		    oss << msecs << "ms " << usecs << "us" << std::endl;
		}
		else
		{
		    uint32_t secs = msecs / 1000;
		    msecs %= 1000;
		    oss << secs << "s " << msecs << "ms" << std::endl;
		}
	    }

	    return oss.str();
	}
};

class BandwidthTracker
{
    class DataDrop
    {
	class BandwidthTracker;
	friend class BandwidthTracker;
	uint32_t flow_id;
	uint64_t record_usec;
	uint32_t nbytes;
	public:
	void set_paras(uint32_t flow, uint64_t usec, uint32_t bytes)
	{
	    flow_id = flow;
	    record_usec = usec;
	    nbytes = bytes;
	}
    };

    std::vector<DataDrop> drops;
    std::vector<DataDrop>::iterator it;
    uint64_t fire_usec;
    uint64_t update_usec; //time of last record keeping event
    bool fired;
    uint64_t nbytes_total;
    std::vector<uint64_t>nbytes_flow;
    std::vector<uint64_t>nbytes_flow_new;
    uint32_t sample_diff_sec;
    uint32_t nrecs; //number of records currently kept
    uint32_t nrecs_max;
    uint32_t nflows;
    pthread_rwlock_t lock;

    double get_avg_mbps_all(uint64_t now) const
    {
	return ((nbytes_total * 8.0) / (now - fire_usec));
    }

    double get_avg_mbps_flow(uint32_t n, uint64_t now) const
    {
	return (((nbytes_flow[n] + nbytes_flow_new[n]) * 8.0) / (now - fire_usec));
    }

    void add_drop(uint32_t flow, uint64_t usec, uint32_t nbytes)
    {
	it->set_paras(flow, usec, nbytes);
	nrecs++;
	it++;
	if (it == drops.end()) it = drops.begin();
    }

    void start_timing()
    {
	fired = true;
	fire_usec = WallTimer::get_usec();
	update_usec = fire_usec;
    }

    void lockread()
    {
	pthread_rwlock_rdlock(&lock);
    }

    void lockwrite()
    {
	pthread_rwlock_wrlock(&lock);
    }

    void unlock()
    {
	pthread_rwlock_unlock(&lock);
    }

    public:
    BandwidthTracker(size_t nrecs_max = 100, uint32_t sample_diff_sec = 1, size_t nflow = SERVER_PORT_COUNT): 
	sample_diff_sec(sample_diff_sec), fired(false), 
	nbytes_total(0), nrecs(0), nrecs_max(nrecs_max), fire_usec(0), nflows(nflow)
    {
	drops.resize(nrecs_max);
	it = drops.begin();
	nbytes_flow.resize(nflow);
	nbytes_flow_new.resize(nflow);
	fill(nbytes_flow.begin(), nbytes_flow.end(), 0);
	fill(nbytes_flow_new.begin(), nbytes_flow_new.end(), 0);
	pthread_rwlock_init(&lock, NULL);
    }

    virtual ~BandwidthTracker() {}

    void report_info()
    {
	lockread();
	uint64_t now = WallTimer::get_usec();
	if (fired)
	{
	    cout << "Average rate for all " << nflows << " flows:"; 
	    cout << "\t" << get_avg_mbps_all(now) << " Mbps" << endl;

	    for (uint32_t i = 0; i < nflows; i++)
	    {
		cout << "\tFlow " << i << " : " << get_avg_mbps_flow(i, now) << " Mbps" << endl;
	    }
	}

	unlock();
    }
    
    void addBytes(uint32_t flow, uint32_t nbytes)
    {
	if (!nbytes) return;

	lockwrite();

	if (!fired)
	{
	    start_timing();
	}

	nbytes_flow_new[flow] += nbytes;
	nbytes_total += nbytes;
	unlock();
    }

    void book_keeping()
    {
	lockread();
	if (!fired) { unlock();return; }
	unlock();

	uint64_t now_time = WallTimer::get_usec();

	lockwrite();
	update_usec = now_time;

	for (uint32_t i = 0; i < nflows; i++)
	{
	    if (nbytes_flow_new[i])
	    {
		nbytes_flow[i] += nbytes_flow_new[i];
		add_drop(i, now_time, nbytes_flow_new[i]);
		nbytes_flow_new[i] = 0;
	    }
	}

	unlock();
    }

};

BandwidthTracker bwtracker;
pthread_t trafThread;
pthread_t shapeThread;
ostream_iterator<int> iprt(cout, " \n");

void *shape_data(void *arg)
{
    while (true)
    {
	sleep(1);
	bwtracker.book_keeping();
    }

    return (void*)0;
}

class SocketUtils
{
    public:
	static void bindUdp(int *it, uint32_t ip, uint16_t port)
	{
	    *it = socket(AF_INET, SOCK_DGRAM, 0);
	    if (*it <= 0) ABORT;
	    struct sockaddr_in addr;
	    memset(&addr, 0, sizeof(addr));
	    addr.sin_family = AF_INET;
	    addr.sin_addr.s_addr = htonl(ip);
	    addr.sin_port = htons(port);
	    int res = bind(*it, (struct sockaddr*)&addr, sizeof(addr));
	    if (res) ABORT;
	}
};

void *monitorTraf(void *arg)
{
    vector<int> sockfds(SERVER_PORT_COUNT);
    for (uint32_t i = 0; i < SERVER_PORT_COUNT; i++)
    {
	SocketUtils::bindUdp(&sockfds[i], INADDR_ANY, SERVER_PORT_START + i);
    }

#define BUFLEN 10230
    char buf[BUFLEN + 1];

    fd_set set;
    int max_fd = *max_element(sockfds.begin(), sockfds.end());

    while (true)
    {
	FD_ZERO(&set);

	for (uint32_t i = 0; i < SERVER_PORT_COUNT; i++)
	    FD_SET(sockfds[i], &set);

	select(max_fd + 1, &set, NULL, NULL, NULL);

	for (uint32_t i = 0; i < SERVER_PORT_COUNT; i++)
	{
	    if (FD_ISSET(sockfds[i], &set))
	    {
		int nrecv = recvfrom(sockfds[i], buf, BUFLEN, 0, NULL, NULL);
		if (nrecv > 0)
		{
		    bwtracker.addBytes(i, nrecv);
		}
	    }
	}
    }

    return (void*)0;
}

int main(int argc, char* argv[])
{
    int ret;
    ret = pthread_create(&trafThread, NULL, monitorTraf, NULL);
    assert(!ret);
    ret = pthread_create(&shapeThread, NULL, shape_data, NULL);
    assert(!ret);

    while (true)
    {
	sleep(1);
	bwtracker.report_info();
    }

    return 0;
}


