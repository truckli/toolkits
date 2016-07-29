#!/usr/bin/env python
#--coding:utf-8-- 


import xlrd, xlwt
import sys, os
import copy
from datetime import * 

input_name = 'InOutData.xls'
input_base = os.path.splitext(input_name)[0]
data = xlrd.open_workbook(input_name)

table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols


rawrecords = []

for i in range(nrows):
    pdatetime = (table.cell(i, 1).value)
    if type(pdatetime) != type(3.0): continue
    checkdate = int(pdatetime)
    checktime = pdatetime - checkdate
    pname = table.cell(i, 0).value
    rawrecords.append((checkdate, checktime, pname))


checkcounts = {}

staff = set() #set
employee_model = {}
staff_records = {}


def excelDate2Str(off):
    return str(date(1899,12,30) + timedelta(days=off))

for checkdate, checktime, pname in rawrecords:
    checkcounts.setdefault(checkdate, 0)
    checkcounts[checkdate] += 1
    staff.add(pname)
    
countfilter = 0.2 * len(staff)
for day in checkcounts:
    if checkcounts[day] > countfilter:
        employee_model[day] = [1000, -1000]

for name in staff:
    staff_records[name] = copy.deepcopy(employee_model)
        
for checkdate, checktime, pname in rawrecords:
    if checkdate not in employee_model: continue
    if checktime < 0.5:
        staff_records[pname][checkdate][0] = min(checktime, staff_records[pname][checkdate][0])
    else:
        staff_records[pname][checkdate][1] = max(checktime, staff_records[pname][checkdate][1])
       
def getReport(in_late, out_early):    
    absent_threshold = 120 
    if in_late >= absent_threshold and out_early >= absent_threshold:
        return u"全天未打卡"
    result = ""
    if in_late > 0 and in_late <= absent_threshold:
        result += u"迟到  %d 分钟." % int(in_late)
    elif in_late > absent_threshold:
        result += u"上班未打卡." 
    if out_early > 0 and out_early <= absent_threshold:
        result += u"早退  %d 分钟." % int(out_early)
    elif out_early > absent_threshold:
        result += u"下班未打卡." 
    return result
        
book = xlwt.Workbook()
sheet1 = book.add_sheet('Sheet1')
date_format = xlwt.XFStyle()
date_format.num_format_str = u'yyyy年mm月dd日'
rowno = 1
for name in staff_records:
    for day in staff_records[name]:
        in_late = (staff_records[name][day][0] - (9.0/24))*24*60
        if ((date(2016,7,22)-date(1899,12,30)).days > day): 
            in_late = (staff_records[name][day][0] - (8.5/24))*24*60
        out_early = ((17.0/24)- staff_records[name][day][1])*24*60
        in_late = int(in_late)
        out_early = int(out_early)
        if in_late > 0 or out_early > 0:
            report = getReport(in_late, out_early)
            sheet1.write(rowno, 0, day, date_format)
            sheet1.write(rowno, 1, name)
            sheet1.write(rowno, 2, report)
            rowno += 1
   
 
sheet1.col(0).width = 6000
sheet1.col(1).width = 6000
sheet1.col(2).width = 6000
sheet1.col(3).width = 6000
sheet1.col(4).width = 6000
book.save('output/'+input_base + '-output.xls')

sys.exit(0)






