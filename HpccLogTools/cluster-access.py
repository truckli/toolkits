#!/usr/bin/env python


####################################################
####################################################
#NEED CUSTOMIZATION:

## extract http status info from a log line
#if log format changes, please modify this function accordingly
def extract_http_status(line):
    words = line.split()
    if len(words) >= 4:
        info2 = words[3].split('/')
        if len(info2) == 2:
            return info2[1]

## extract cache status info from a log line
#if log format changes, please modify these functions accordingly
def is_hit(line):
    if line.find('HIT') >= 0: return True
    return False

def is_miss(line):
    if line.find('MISS') >= 0: return True
    return False

def is_expire(line):
    if line.find('EXPIRES') >= 0: return True
    return False

####################################################
####################################################

import sys, os, re

#count error line occurences
http_status_count = {}
request_count = 0
hit_count = miss_count = expire_count = 0

#extract error info from a log line
def parse_line(line):
    def add_count(table, key):
        if table.has_key(key):
            table[key] += 1
        else:
            table[key] = 0

    global http_status_count, request_count
    global hit_count, miss_count, expire_count
    request_count += 1
    if is_hit(line): hit_count += 1
    elif is_miss(line): miss_count += 1
    elif is_expire(line): expire_count += 1

    http_status = extract_http_status(line)
    if http_status: add_count(http_status_count, http_status)


def report_cache():
    global http_status_count, request_count
    global hit_count, miss_count, expire_count
    hit_rate = hit_count * 100.0 / request_count  
    miss_rate = miss_count * 100.0/ request_count 
    expire_rate = expire_count * 100.0/ request_count 
    print("%d requests, %.2f %% hit,  %.2f %% miss, %.2f %% expire, %.2f %% info missing" 
            % (request_count, hit_rate, miss_rate, expire_rate, 100 - hit_rate - miss_rate - expire_rate))
    

def report_http():
    global http_status_count, request_count
    items = http_status_count.items()
    items = sorted(items, key=lambda d:d[1], reverse = True)
    for item in items:
        print(" Status %s: %d occurences(%.2f %%)" % (item[0], item[1], item[1]*100.0/request_count))




if __name__ == '__main__':
    fhandle = None
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == 'help' or sys.argv[1] == '--help':
            print('This script processes access.log for HPCC nginx servers')
            print('Usage:')
            print('\t' + sys.argv[0] + ' FILENAME')
            print('\tcat FILENAME | ' + sys.argv[0])
            sys.exit(0)
        if os.path.isfile(sys.argv[1]):
            filename = sys.argv[1]
            try:
                fhandle = open(filename, 'r')
            except:
                pass

    fhandle = fhandle or sys.stdin

    for line in fhandle:
        parse_line(line)

    if fhandle != sys.stdin:
        fhandle.close()
    
    report_cache()
    report_http()




