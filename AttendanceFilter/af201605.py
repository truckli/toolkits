#!/usr/bin/env python
#--coding:utf-8-- 


import xlrd
import sys
from datetime import * 

data = xlrd.open_workbook('201605.xlsx')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
summary = {}
curno = None
scandates_m = [3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26]
scandates = []
# 2015/12/31 => 42369
# 1899/12/30 => 0 
for d in scandates_m:
    scandates.append((datetime(2016,5,d) - datetime(1899,12,30)).days)
    
namemap = {}

for i in range(1, nrows):
    pname = table.cell(i, 1).value
    pno = pname 
    pdatetime = (table.cell(i, 2).value)
    pdate = int(pdatetime)
    ptime = float(pdatetime) - pdate
    if pno != curno:
        curno = pno
        summary[pno] = {}
        namemap[pno] = pname
        for date in scandates:
            summary[pno][date] = {"in":10000, "out":-10000}
    if not pdate in scandates: continue
    if ptime < 0.5:
        summary[pno][pdate]["in"] = min(summary[pno][pdate]["in"], ptime)
    else:
        summary[pno][pdate]["out"] = max(summary[pno][pdate]["out"], ptime)



import xlwt
book = xlwt.Workbook()
sheet1 = book.add_sheet('Sheet 1')
rowno = 1
f=open('list.txt', 'w')
date_format = xlwt.XFStyle()
date_format.num_format_str = u'yyyy年mm月dd日'

for pno in summary:
    for date in summary[pno]:
        score = summary[pno][date]
        abnormal = False
        line = u'工号%s\t %s\t %d日\t' % (pno, namemap[pno], date-42369)
        in_late = (score["in"] - (8.5/24))*24*60
        out_early = ((17.0/24)-score["out"])*24*60
        in_info = ""
        out_info = ""
        if in_late > 60: 
            in_info = u"上班无记录"
            abnormal = True
        elif in_late > 3:
            in_info = u"迟到%d分钟" % (int(in_late))
            abnormal = True

        if out_early > 60: 
            out_info = u"下班无记录"
            abnormal = True
        elif out_early > 3:
            out_info = u"早退%d分钟" % (int(out_early))
            abnormal = True

        if abnormal:
            line = line + in_info + "\t" + out_info + "\t"
            f.write(line.encode('gb2312') + '\r\n')
            sheet1.write(rowno, 2, pno)
            sheet1.write(rowno, 3, namemap[pno])
            sheet1.write(rowno, 4, date)
            sheet1.write(rowno, 5, in_info)
            sheet1.write(rowno, 6, out_info)
            sheet1.write(rowno, 7, date, date_format)
            rowno += 1

f.close()
sheet1.col(5).width = 4000
sheet1.col(6).width = 4000
sheet1.col(7).width = 6000
book.save('output.xls')







