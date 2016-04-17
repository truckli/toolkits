#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## query server for statistics and graph plotting, and generate a markdown report


import urllib.request
import re
import os
import sys

handler = urllib.request.HTTPHandler()
opener = urllib.request.build_opener(handler)
metadata_f = open('wei.fixfeature.curse', 'r')
range_fname = 'fea-range.dat'
range_f = open(range_fname, 'r')
fea_start = 1
fea_end = 10
sta_file_name = 'feature-sta-'+str(fea_start) + '-'+str(fea_end) + '.md'
f = open(sta_file_name, 'w')
feature_range = {}


# determine a range that covers most values of the feature
def probe_range(feature):
    def get_coverage(feature, cut_from, cut_to):
        url = 'http://42.120.173.6/draw/html/show.php?datatag=reorder_label_train_merge_5feature.final.fad&break_key=-&break_value=-&fea=%s&prec=1&cut_from=%d&cut_to=%d&label=m%%3ALabel&recom=0&plottype=0&speartype=0' % (feature, cut_from, cut_to)
        req = urllib.request.Request(url=url, data=b"", headers={}, method='GET') 
        rsp_data = opener.open(req).read().decode('utf8')
        coverage = re.search(u"样本的(.*?)\%", rsp_data).group(1)
        pearson = re.search('pearson.*?(\d.\d*)', rsp_data, re.DOTALL).group(1)
        spearman = re.search('spearman.*?(\d.\d*)', rsp_data, re.DOTALL).group(1)
        return float(coverage)
    
    if feature in feature_range:
        cut_range = feature_range[feature]
        cut_from = cut_range[0]
        cut_to = cut_range[1]
        return cut_from, cut_to

    cut_from = 0
    cut_to = 64
    print('caculating coverage for %s, [%d - %d]' %(feature, cut_from, cut_to))
    coverage = get_coverage(feature, cut_from, cut_to)

    probe_limit = 10
    while probe_limit > 0 and coverage > 99:
        print('shrinking range for %s, [%d - %d]:%f coverage' %(feature, cut_from, cut_to, coverage))
        cut_to_try = int(cut_to / 2)
        if cut_to_try == 0: break
        coverage_try = get_coverage(feature, cut_from, cut_to_try)
        if coverage_try < 85: break
        coverage = coverage_try
        cut_to = cut_to_try
        probe_limit -= 1
    
    probe_limit = 10
    while probe_limit > 0 and coverage < 85:
        print('expanding range for %s, [%d - %d]:%f coverage' %(feature, cut_from, cut_to, coverage))
        cut_to *= 2
        coverage = get_coverage(feature, cut_from, cut_to)
        probe_limit -= 1

    if coverage != get_coverage(feature, -cut_to, cut_to):
        cut_from = -cut_to
        coverage = get_coverage(feature, cut_from, cut_to)
    
    return cut_from, cut_to



def crawl_query(feature):
    cut_from, cut_to = probe_range(feature)
    presison = ((cut_to) - (cut_from)) / 20.0
    url = 'http://42.120.173.6/draw/html/show.php?datatag=reorder_label_train_merge_5feature.final.fad&break_key=-&break_value=-&fea=%s&prec=%d&cut_from=%d&cut_to=%d&label=m%%3ALabel&recom=0&plottype=0&speartype=0' % (feature, presison, cut_from, cut_to)
    req = urllib.request.Request(url=url, data=b"", headers={}, method='GET') 
    print('querying info for feature ' + feature + ' ....')
    rsp_data = opener.open(req).read().decode('utf8')
    coverage = re.search(u"样本的(.*?)\%", rsp_data).group(1)
    feature_range[feature] = (int(cut_from), int(cut_to), float(coverage))
    pearson = re.search('pearson.*?(\d.\d*)', rsp_data, re.DOTALL).group(1)
    spearman = re.search('spearman.*?(\d.\d*)', rsp_data, re.DOTALL).group(1)
    image = re.search('img src="(.*?)"', rsp_data, re.DOTALL).group(1)
    f.write('range [%d - %d], coverage %s  \n' % (cut_from, cut_to, coverage))
    f.write('pearson %s, spearman %s  \n' % (pearson, spearman))
    f.write('![](http://42.120.173.6/draw/html/'+image+')  \n')


if __name__ == "__main__":
    for range_line in range_f:
        words = range_line.split()
        if len(words) > 2:
            feature_range[words[0]] = (int(words[1]), int(words[2]), float(words[3]))
    
    os.system('rm -f machine2.md')
    feature_count = 1
    for metadata_line in metadata_f:
        if feature_count >= fea_start:
            words = metadata_line.split()
            feature_name = words[0]
            feature_weight = words[2]
            fea_title = '## '+ str(feature_count) + ' ' + feature_name + '(权重：' + feature_weight + ' %)  \n'
            f.write(fea_title)
            #crawl_query(feature_name)
            f.write('  \n')
            os.system ('echo " %s   " >> machine2.md' % (fea_title))
            os.system('./feature.py reorder_label_train_merge_5feature.final.fad %s >> machine2.md' % (feature_name))
        feature_count += 1
        if feature_count > fea_end:
            break

    
    f.close()
    metadata_f.close()
    range_f.close()
    range_f = open(range_fname, 'w')
    for feature_name in feature_range:
        range_f.write(feature_name + ' ' + 
                str(feature_range[feature_name][0]) +' ' +  
                str(feature_range[feature_name][1]) +' ' +  
                str(feature_range[feature_name][2]) +' ' +  
                '# comment  \n' )

    range_f.close()







