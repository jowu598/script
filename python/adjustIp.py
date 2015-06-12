#!/usr/bin/python
import sys, getopt, os,  os.path,  re,  codecs
from xml.dom import minidom
from xml.dom.minidom import Document


changeReg = '[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}'
filePath = '/home/yj/testip'

def regexFind(regex, ip):
    if not os.path.isfile(filePath):
    	return false
    f = open(filePath, r)
    str = f.read()
    if (str):
        if (regEx.search(regEx, str)):
            return true;
   	return false;

def regexChange(regex, ip):
	f = open(filePath, "r")
	str = f.read()

	if (str):
	    str = regex.sub(ip, str)	
	    fout = open(filePath, "w")
	    fout.write(str)
	    fout.close()

if __name__ == '__main__':     
	if (len(sys.argv) !=2):
		exit(1)

	ip = sys.argv[1]
	# if (!regexFind(re.compile(changeReg), ip)):
	# 	exit(1)

	regexChange(re.compile(changeReg), ip)
