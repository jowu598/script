#!/usr/bin/python

import sys, getopt, os, os.path, re

changReg = '/\*{1,2}[\s\S]*?\*/'
content = '/*********************/'

def readFile(file):
    f = open(file, 'r')
    content = f.read()
    f.close()
    return content

def regexChange(file, reg, str):
	if not os.path.isfile(file):
		return ''
	f = open(file, 'r')
	content = f.read()
	if (content):
		content = reg.sub(str, content)
		fout = open(file, 'w')
		fout.write(content)
		fout.close()	

def changeDiscription(path, newStr):
	for f in os.listdir(path):
		sourceF = os.path.join(path, f)
		if os.path.isfile(sourceF):
			regexChange(sourceF, re.compile(changReg), newStr)
		if os.path.isdir(sourceF):
			changeDiscription(sourceF, newStr)

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print("error input")
		exit(1)
	path = os.getcwd() + '/swapContent.txt'
	newStr = readFile(path)
	changeDiscription(sys.argv[1], newStr)
	print("done")


