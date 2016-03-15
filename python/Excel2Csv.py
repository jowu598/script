#! /usr/bin/python
#coding:utf-8
import sys
import os
import re
from multiprocessing import Process
try:
    import xlrd
except :
    print("*****************************************")
    print("module numpy not found!!!")
    print("please run command:")
    print("    sudo apt-get install python-xlrd")
    print("*****************************************")
    exit(-1)
import struct
class xls2csv:
    def __init__(self):
        print("---xml2csv----");
    def convert(self, xmlPath, csvPath):
        excel = xlrd.open_workbook(xmlPath)
        sheet = excel.sheet_by_name(u'StringTable')
        print("rows count = %d" %(sheet.nrows))
        print("col count = %d" %(sheet.ncols))
        csvFile = file(csvPath,'wb')
        csvFileWrite = csv.writer(csvFile)
        for colNum in range(0, int(sheet.ncols)):
            for rowNum in range(1,int(sheet.nrows)):
                row = sheet.row_values(rowNum)
                print("---")
               # print("%d,%d:" %(colNum),%(rowNum), %(row[colNum].encode("utf-8")))

if __name__ == '__main__' :
    if len(sys.argv) != 3:
        print("Input argv is not correct!")
        print("StrResCreate.py + string xls file path name + output path + out put name")
        print("exp:StrResCreate.py /media/webcloud/String/EmptyStringTbl.xls /media/webcloud/Result ProjectA")
    else :
        xlsResFilePathName = sys.argv[1]
        targetPath = sys.argv[2]


        print("Input information:")
        print("                        xlsResFilePathName:%s" % xlsResFilePathName)
        print("                        targetPath:%s" % targetPath)
        print("creating resource files...")

        creator = xls2csv()
        creator.convert(xlsResFilePathName, targetPath)

        print("done!")
