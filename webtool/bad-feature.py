#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## query server for statistics and graph plotting, and generate a markdown report


import urllib.request
import re
import os
import sys

fea_end = 10000000000
fea_start = 1
badfea_fname = "badfeature.md"
feaweight_fname = "wei.fixfeature.curse"
train_fname = "reorder_label_train_merge_5feature.final.fad"

def file_append(fname, line):
    append_f = open(fname, 'a')
    append_f.write(line)
    append_f.close()

if __name__ == "__main__":
    badfea_list_f = open(badfea_fname, 'r')
    feaweight_f = open(feaweight_fname, 'r')
    badfea_list = {}
    for line in badfea_list_f:
        if not re.search('^#', line):
            feature_name = line.strip()
            badfea_list[feature_name] = True

    badfea_list_f.close()

    feature_count = 1
    bad_feature_count = 1
    report_fname = 'sta-'+str(fea_start) + '-'+str(fea_end) + '.md'
    if os.path.isfile(report_fname): os.remove(report_fname)
    for metadata_line in feaweight_f:
        if feature_count >= fea_start:
            words = metadata_line.split()
            feature_name = words[0]
            if feature_name in badfea_list:
                feature_weight = words[2]
                fea_title = '## '+ str(feature_count) + ' ' + feature_name + '(weight：' + feature_weight + ' %)  \n'
                file_append(report_fname, fea_title)
                os.system('./feature.py %s %s >> %s ' % (train_fname, feature_name, report_fname))
                bad_feature_count += 1
        feature_count += 1
        if feature_count > fea_end: break


    feaweight_f.close()
    sys.exit(0)
    
    


