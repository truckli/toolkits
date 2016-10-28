#!/usr/bin/env python
#--coding:utf-8-- 

import os

rule_id = 0

for service in range(0, 136):
    for service_rule_count in (0, 20):
        print("add service %d type ud rule ud0=0xF400/0XFFFF ud1=0x%X/0xFFFF  hit_flag=on" % (service, rule_id)) 
        rule_id += 1


for service in range(136, 256):
    for service_rule_count in (0, 19):
        print("add service %d type ud rule ud0=0xF400/0XFFFF ud1=0x%X/0xFFFF  hit_flag=on" % (service, rule_id)) 
        rule_id += 1





