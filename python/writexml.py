#!/usr/bin/python

from xml.dom import minidom

def testXml():
	doc = minidom.Document()
	doc = minidom.parse('/home/yj/rabbit_animations.plist')
	print "doc is read !!"


if __name__ == '__main__':
	testXml()
	print "transfrom done!!"