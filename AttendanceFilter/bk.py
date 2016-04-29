#!/usr/bin/env python
#--coding:utf-8-- 


import xlrd
from datetime import datetime 

data = xlrd.open_workbook('2016.xls')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
summary = {}
curno = None
scandates = [4,5,6,7,8,11,12,13,14,15,18,19,20,21,22,25,26,27,28,29]
for i in range(len(scandates)):
	scandates[i] += 42369
print scandates

namemap = {}

for i in range(1, nrows):
	pname = table.cell(i, 1).value
	pno = table.cell(i, 2).value
	pdatetime = (table.cell(i, 3).value)
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
			rowno += 1

f.close()
book.save('output.xls')







