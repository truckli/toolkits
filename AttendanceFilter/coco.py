#!/usr/bin/env python
# -*- coding:utf-8 -*-
import  xdrlib ,sys
import xlrd
import xlwt
import copy
def open_excel(filename):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception,e:
        print str(e)
#获取人员姓名,工号
def excel_get_name(filename,colnameindex=0,by_index=0):
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    name = table.cell_value(1,1)
    number = table.cell_value(1,2)
    namelist = [name]
    numberlist = [number]
    for rownum in range(2,nrows):
         newname = table.cell_value(rownum,1)
         newnumber = table.cell_value(rownum,2)
         if (newname == name and newnumber == number):
             continue
         else:
             name = newname
             number = newnumber    
             namelist.append(name)
             numberlist.append(number)#获取人员姓名,工号
   
    return namelist,numberlist

#获取上班时间
def excel_get_standarddate(filename,colnameindex=0,by_index=0):
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    datelist = []
    namelist,numberlist = excel_get_name(filename,colnameindex=0,by_index=0)
    for rownum in range(1,nrows):
        dt_value = xlrd.xldate_as_tuple(table.cell_value(rownum,3),data.datemode)
        date_value = dt_value[:3]
        datelist.append(date_value)
    standarddate = []
    for i in range(len(datelist)):
        n = datelist.count(datelist[i])
        if n>= len(namelist)/2 and datelist[i] not in standarddate:
            standarddate.append(datelist[i])
    return standarddate
            
#判断异常
def excel_get_error(filename,colnameindex=0,by_index=0):
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    namelist,numberlist = excel_get_name(filename,colnameindex=0,by_index=0)
    standarddate = excel_get_standarddate(filename,colnameindex=0,by_index=0)
    # 人员工作日打卡空表格
    staff_records,employee_model = {},{}
    for name in namelist:
        for date in standarddate:
            employee_model[date] = [(24,0,0),(0,0,0)]
        staff_records[name] = copy.deepcopy(employee_model)
    #读表格
    
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        dt_value = xlrd.xldate_as_tuple(row[3],data.datemode)
        date_value = dt_value[:3]
        time_value = dt_value[3:]
        if staff_records[row[1]].has_key(date_value):
            n = staff_records[row[1]][date_value]
            if time_value <= (12,0,0) and time_value < n[0]:
                staff_records[row[1]][date_value][0] = time_value
            elif time_value >= (13,0,0) and time_value > n[1]:
                staff_records[row[1]][date_value][1] = time_value
    #处理打卡表格
    staff_error, error_model = {},{}
    state = [ ]
    for name in namelist:
        for date in standarddate:
            if staff_records[name][date][0] == (24,0,0):
                state.append(u"上午未打卡")
            elif staff_records[name][date[0]] > (8,30,0):
                state.append(u"上午迟到")
            if staff_records[name][date][1] == (0,0,0):
                state.append(u"下午未打卡")
            elif staff_records[name][date][1] < (17,0,0):
                state.append(u"下午迟到")
            error_model[date] = copy.deepcopy(state)
        staff_error[name] = copy.deepcopy(error_model) 
    return staff_error


#写文件
def write_excel():
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    row0 = [u'姓名',u'考勤号码',u'日期',u'异常']
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i]) 
    namelist,numberlist = excel_get_name(r'C:\Users\coco\Desktop\2016.xls',0,0)
    for i in range(1,len(namelist)):
        sheet1.write(i,0,namelist[i-1])#第一列
    for i in range(1,len(numberlist)):
        sheet1.write(i,1,numberlist[i-1])#第二列
    f.save('result.xls')
def main():
    #write_excel()
    print excel_get_error(r'C:\Users\coco\Desktop\2016.xls',0,0)
     

if __name__=="__main__":
    main()
