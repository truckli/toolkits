#!/usr/bin/env python
# -*- coding: utf-8 -*-

## covert values in a logarithm scale, f(x) = log_2(1+x), or x for x < 0


import scipy.stats
import matplotlib.pyplot as plt
import os
import re
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(filename)s[line %(lineno)d] %(levelname)s: %(message)s')
line_limit = 1e9 
fea_sta_min = 1e10
fea_sta_max = -1e10
fea_sta_bucket_avg_min = 1e10
fea_sta_bucket_avg_max = -1e10
eps_val = 1e-7
buckets = []


def is_integer(float_num):
    if abs(float_num - int(float_num)) <= eps_val: 
        return True
    return False

def draw_histo(downcut, upcut, value, maxpoints=60):
    npoints = 2 + int((value - downcut) * 1.0 * maxpoints/ (upcut - downcut))
    print ('`'),
    for i in range(npoints):
        print('*'),
    print("`  ")


def print_val(name, val):
    if is_integer(val):
        print("%s: %d  " % (name, val))
    else:
        print("%s: %f  " % (name, val))

class Bucket:
    def __init__(self, downcut_dist, upcut_dist, downcut, upcut, dist_type = "integer"):
        self.range_val = (downcut, upcut)
        self.range_dist = (downcut_dist, upcut_dist)
        self.samples = {}
        self.dist_type = dist_type
        self.count = 0
        self.label_sum = 0
        self.label_avg = 0 
    def is_in_bucket(self, value):
        if value >= self.range_val[0] and value < self.range_val[1]:
            return True
        return False

    def add_sample(self, key, info, limit=8):
        self.count += 1
        self.label_sum += float(key)
        self.label_avg = self.label_sum * 1.0 / self.count
        if not self.samples.has_key(key):
            self.samples[key] = []
        vlist = self.samples[key]
        if len(vlist) < limit:
            vlist.append(info)

    def display_sample(self):
        for key in self.samples:
            vlist = self.samples[key]
            for val in vlist:
                print'%s: <%s>  '%(key, val)

    def display(self):
        if self.range_dist[0] < 0:
            print("Bucket for 0 values."),
        else:
            if is_integer(self.range_val[0]) and is_integer(self.range_val[1]):
                print("%d %% - %d %%: [%d, %d]." % 
                        (self.range_dist[0]*100, 
                            self.range_dist[1]*100, 
                            self.range_val[0], 
                            self.range_val[1])),
            else:
                print("%d %% - %d %%: [%.5f, %.5f]." % 
                        (self.range_dist[0]*100, 
                            self.range_dist[1]*100, 
                            self.range_val[0], 
                            self.range_val[1]))

        print("bucket size: %d." % (self.count)),
        if self.count > 0:
            print("label average: %.2f .  " % (self.label_avg))

def find_bucket(val, buckets):
    for bucket in buckets:
        if bucket.is_in_bucket(val): return bucket

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s DATA-FILE FEATURE-NAME" %(sys.argv[0]))
   
    data_fname = sys.argv[1]

    feature = sys.argv[2]
    data_f = open(data_fname, 'r')

    title_line = data_f.readline()
    titles = title_line.split()
    index = 0
    for value in titles:
        if value == feature:
            logging.debug('index is %d' % (index))
            break
        index += 1

    line_num = 0
    fea_val_sum = 0.0
    values = []
    labels = []
    dist_type = "binary"
    zeros_count = 0
    ones_count = 0

    while True:
        if line_num > line_limit: break
        line = data_f.readline()
        if not line: break
        line_num += 1
        words = line.split()

        assert(len(words) > index or logging.debug('len %d, index %d' %(len(words), index)))
        value = float(words[index])
        label = int(words[0])
        if not is_integer(value):
            if value < 0:
                dist_type = "real"
            elif dist_type != "real":
                dist_type = "non-negative-real"
        else:
            value = int(value)
            if value == 0: 
                zeros_count += 1
            elif value == 1:
                ones_count += 1
            else:
                dist_type = "integer" 
        
        fea_sta_max = max(fea_sta_max, value)
        fea_sta_min = min(fea_sta_min, value)
        fea_val_sum += value
        values.append(value)
        labels.append(label)
        fea_sta_avg = fea_val_sum * 1.0 / line_num
        zero_ratio = zeros_count * 100.0/ line_num 
           
    print('### Basic Statistics  ')
    print(' Distribution type: %s.  \n  %f %% zeros  ' % (dist_type, zero_ratio))
    print_val("Average", fea_sta_avg)
    print_val("Minimum", fea_sta_min)
    print_val("Maximum", fea_sta_max)
    spearman = scipy.stats.spearmanr(values, labels)[0]
    pearson = scipy.stats.pearsonr(values, labels)[0]
    print_val("Spearman R", spearman)
    print_val("Pearson R", pearson)
    
    
    #make buckets
    if dist_type == "binary":
        buckets.append(Bucket(0, zero_ratio/100, 0, eps_val*0.1, dist_type))
        buckets.append(Bucket(zero_ratio/100, 1, 1, 1+eps_val*0.1, dist_type))
    else:
        #purge 0 value
        svalues = [v for v in values if v != 0]
        svalues.sort()
        item_count = len(svalues)

        downcut = svalues[0] 
        #downcut, upcut, samples for each bucket
        buckets.append(Bucket(-1, 0, 0, eps_val, dist_type))

        for i in range(9):
            ratio = (i + 1) * 0.1
            upid = int(item_count*ratio)
            if upid > 0: upid -= 1
            upcut = svalues[upid]
            buckets.append(Bucket(ratio - 0.1, ratio, downcut, upcut, dist_type))
            downcut = upcut
        for i in range(9):
            ratio = 0.9 + (i + 1) * 0.01
            upid = int(item_count*ratio)
            if upid > 0: upid -= 1
            upcut = svalues[upid]
            buckets.append(Bucket(ratio - 0.01, ratio, downcut, upcut, dist_type))
            downcut = upcut
       
        buckets.append(Bucket(0.99, 1, downcut, fea_sta_max + 1, dist_type))
    
    #sample data into buckets
    data_f.seek(0, 0)
    title_line = data_f.readline()
    line_num = 0
    while True:
        if line_num > line_limit: break
        line = data_f.readline()
        if not line: break
        line_num += 1
        words = line.split()
        value = float(words[index])
        label = words[0]
        url = words[1]
        bucket = find_bucket(value, buckets)
        bucket.add_sample(label, url, 8)
   

    for bucket in buckets:
        if bucket.count > 0:
            fea_sta_bucket_avg_max = max(fea_sta_bucket_avg_max, bucket.label_avg)
            fea_sta_bucket_avg_min = min(fea_sta_bucket_avg_min, bucket.label_avg)
    
    #plot
    print('### Feature-Label Histogram  ')
    for bucket in buckets:
        if bucket.count > 0:
            bucket.display()
            draw_histo(fea_sta_bucket_avg_min, fea_sta_bucket_avg_max, bucket.label_avg)

    if dist_type == "binary":
        print('### Zero Value Sampling  ')
        buckets[0].display_sample()
        print('### One Value Sampling  ')
        buckets[1].display_sample()
    else:
        print('### Large Value(99% -100%) Sampling  ')
        buckets[-1].display_sample()
    
    print('\n\n\n')
    data_f.close()
    sys.exit(0)



