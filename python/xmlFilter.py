#!/usr/bin/python
import sys, getopt, os,  os.path,  re,  codecs
from xml.dom import minidom
from xml.dom.minidom import parse
import xml.dom.minidom



# DOMTree = xml.dom.minidom.parse("movies.xml")
# collection = DOMTree.documentElement
# if collection.hasAttribute("shelf"):
#    print "Root element : %s" % collection.getAttribute("shelf")
# movies = collection.getElementsByTagName("movie")
# for movie in movies:
#    print "*****Movie*****"
#    if movie.hasAttribute("title"):
#       print "Title: %s" % movie.getAttribute("title")

#    type = movie.getElementsByTagName('type')[0]
#    print "Type: %s" % type.childNodes[0].data
#    format = movie.getElementsByTagName('format')[0]
#    print "Format: %s" % format.childNodes[0].data
#    rating = movie.getElementsByTagName('rating')[0]
#    print "Rating: %s" % rating.childNodes[0].data
#    description = movie.getElementsByTagName('description')[0]
#    print "Description: %s" % description.childNodes[0].data



# class XmlParser():
# 	node = self.dom.getElementsByTagName(name)
# 	def readNode(self, nodeRoot):
		
# 		for node in nodeRoot:

# 	def filterXmlFile():


# 	def __init__(self, file):
# 		self.dom = minidom.parse(filename)
# 		self.root = self.dom.documentElement


g_filter = []

def shallFileter(name):

	for filter in g_filter:
		if name.find(filter) != -1:
			return True;
	return False;

def xmlFilter(filename, flitername):
	filterRoot = minidom.parse(flitername)
	filters = filterRoot.getElementsByTagName("filter")
	for filter in filters:
		fns = filter.getElementsByTagName("fn")
		for fn in fns:
			print "filtered fn == %s" % fn.childNodes[0].data
			g_filter.append(fn.childNodes[0].data)

	dom = minidom.parse(filename)
	root = dom.documentElement
	errors = root.getElementsByTagName("error")
	for err in errors:
		stacks = err.getElementsByTagName('stack')
		for stack in stacks:
			frame = stack.getElementsByTagName("frame")[0]
			obj = frame.getElementsByTagName("obj")[0]
			print "obj = %s" % obj.childNodes[0].data
			if (shallFileter(obj.childNodes[0].data)):
				print "remove node  with obj %s" % obj.childNodes[0].data
				root.removeChild(err)
				break
			else:
				print "node is not found with obj %s" % obj.childNodes[0].data

	print "write to file"
	f = codecs.open('1.xml','w','utf-8')  
	dom.writexml(f,addindent='  ',newl='\n',encoding = 'utf-8')  
	f.close() 

if __name__ == '__main__':
    xmlFilter("error.xml","filter.xml");


# <error>
#   <unique>0x99c</unique>
#   <tid>8</tid>
#   <kind>Race</kind>
#   <xwhat>
#     <text>Possible data race during read of size 4 at 0x555556C by thread #8</text>
#     <hthreadid>8</hthreadid>
#   </xwhat>
#   <stack>
#     <frame>
#       <ip>0x4F52BEE</ip>
#       <obj>/lib/libncmq.so</obj>
#       <fn>nutshell::NCMQOwn::incSeqnum()</fn>
#     </frame>
#   </stack>
#   <auxwhat>Address 0x555556C is 404 bytes inside a block of size 904 alloc'd</auxwhat>
#   <stack>
#     <frame>
#       <ip>0x4834348</ip>
#       <obj>/system/usr/lib/valgrind/vgpreload_helgrind-arm-linux.so</obj>
#       <fn>operator new(unsigned int, std::nothrow_t const&amp;)</fn>
#     </frame>
#     <frame>
#       <ip>0x4F563B7</ip>
#       <obj>/lib/libncmq.so</obj>
#       <fn>nutshell::NCMQSocket::create(int, nutshell::NCMQContext*, unsigned int, int)</fn>
#     </frame>
#   </stack>
# </error>

