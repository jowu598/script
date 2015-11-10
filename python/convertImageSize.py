#!/usr/bin/python
import os,glob
import Image
import math


def convertSize():
	img = Image.open('/home/yj/1.bmp')
	newImg = img.resize((100,100),Image.ANTIALIAS)
	newImg.save("/home/yj/1_1.bmp")

if __name__ == '__main__':
	convertSize()
