#!/usr/bin/env python
# -*- coding: utf-8 -*-

## covert values in a logarithm scale, f(x) = log_2(1+x), or x for x < 0


import re
import sys

def do_logarithm(value):
    if value == '0': return 0
    float_number = float(value)
    if float_number < 0: return float_number
    import math
    try:
        loga_number = math.log(1+float_number, 2)
        loga_number = round(loga_number, 2)
        if loga_number - int(loga_number) < 1e-6: 
            loga_number = int(loga_number)
    except Exception as e:
        print 'Error doing logarithm calcs:', value 
    return loga_number 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: %s datafile" %(sys.argv[0]))

    data_fname = sys.argv[1]
    output_fname = 'loga-' + data_fname
    data_f = open(data_fname, 'r')
    output_f = open(output_fname, 'w')

    title_line = data_f.readline()
    output_f.write(title_line)

    line_num = 1
    while True:
        if line_num > 1000000:break
        line = data_f.readline()
        if not line: break
        values = line.split()
        output_line = values[0] + '\t' + values[1] + '\t' + values[2] + '\t'
        for i in range(3, len(values), 1):
            output_line += str(do_logarithm(values[i])) + '\t'
        output_f.write(output_line + '\n')
            
        line_num += 1

    data_f.close()
    output_f.close()






