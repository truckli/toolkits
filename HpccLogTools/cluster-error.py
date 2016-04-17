#!/usr/bin/env python


####################################################
####################################################
#NEED CUSTOMIZATION:

#extract error info from a log line
#if log format changes, please modify this function accordingly
def extract_err(line):
    import re
    m = re.match(".*\[lua\](.*) client:.*", line)
    if m: return m.group(1)

####################################################
####################################################


import sys, os

#count error line occurences
err_count = {}
request_count = 0

#extract error info from a log line
def parse_line(line):
    def add_count(table, key):
        if table.has_key(key):
            table[key] += 1
        else:
            table[key] = 0
    
    global request_count
    global err_count
    request_count += 1
    info = extract_err(line)
    if info: add_count(err_count, info)

#decide if two strings are similar. used for fuzzy matching
#TODO: more advanced fuzzy matching algorithms
def similar_string(str1, str2):
    if str1[1:30] == str2[1:30]:
        return True
    return False

def report_fuzzy():
    fuzzy = err_count.items()
    fuzzy = sorted(fuzzy, key=lambda d:d[0], reverse = True)
    #merge similar error strings 
    ind = 1
    uind = 0
    while ind < len(fuzzy):
        if similar_string(fuzzy[ind][0], fuzzy[uind][0]):
            fuzzy[uind] = (fuzzy[uind][0], fuzzy[uind][1] + fuzzy[ind][1])
            fuzzy[ind] = (fuzzy[ind][0], 0)
        else:
            uind = ind
        ind += 1

    #sort by occurrence 
    fuzzy = sorted(fuzzy, key=lambda d:d[1], reverse = True)
    print('fuzzy result: *******************************')
    for item in fuzzy:
        if item[1] > 0:
            print(str(item[1])+' occurences(fuzzy): '+ item[0])


def report_exact():
    exact = err_count.items()
    #sort by occurrence 
    topcount = 50
    print('top '+ str(topcount) + ' error lines: *************************')
    exact = sorted(exact, key=lambda d:d[1], reverse = True)
    for ind in range(topcount):
        if ind < len(exact):
            item = exact[ind]
            print(str(item[1])+' occurences(exact): '+ item[0])



if __name__ == '__main__':
    fhandle = None
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == 'help' or sys.argv[1] == '--help':
            print('This script processes cache.log for HPCC nginx servers')
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

    report_fuzzy()
    report_exact()





