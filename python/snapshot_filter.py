#!/usr/bin/python
import re
import sys
import os

regBegin = "[\s]*?\[TC\:\d+\]\[TT\:\d+\][\s]*.?\[([a-zA-Z0-9_]+|[\-]{1,}QML[\-]{1,})\][\s]*.?\[[\w]+::[\w]+\][\s]*.?\[begin\][\s]{0,}(!!!\[net.suntec.app.[\w]+.application\]){0,1}$"
regEnd = "[\s]*?\[TC\:\d+\]\[TT\:\d+\][\s]*.?\[([a-zA-Z0-9_]+|[\-]{1,}QML[\-]{1,})\][\s]*.?\[[\w]+::[\w]+\][\s]*.?\[end\][\s]{0,}(!!!\[net.suntec.app.[\w]+.application\]){0,1}$"
regApp = "net.suntec.app.[\w]+.application"
regTime = "\[TC:\d+\]\[TT:\d+\]"
regModel = "\[([a-zA-Z0-9_]+|[\-]{1,}QML[\-]{1,})\]"
regFunc = "[\w]+::[\w]+"

global root

class LifeBlock:
    def __init__(self, parent, blockName="", modelName="", functionName="", btc="0", btt="0"):
        self.blockName = blockName
        self.modelName = modelName
        self.functionName = functionName
        self.begin_tc = btc
        self.begin_tt = btt
        self.end_tc = "0"
        self.end_tt = "0"
        self.clist = []

        if parent:
            self.setParent(parent)
    def setParent(self, p):
        self.parent = p
        p.clist.append(self)

def parseInfo(line):
	appName = ""
	if re.search(regApp, line) and re.search("\[begin\]", line):
		app = re.findall(regApp, line)
		appName = app[0]
		depth = 0

	m = re.findall("\[TC:\d+\]\[TT:\d+\]", line)
	n = re.findall("\d+", m[0])
	tc = n[0]
	tt = n[1]

	model = re.findall("\[([a-zA-Z0-9_]+|[\-]{1,}QML[\-]{1,})\]", line)
	modelName = model[0]

	function = re.findall("[\w]+::[\w]+", line)
	functionName = function[0]

	return appName,tc,tt,modelName,functionName

# def dump(block, depth):
# 	length = len(block.clist)
# 	# print ("set node [%s] with parent [%s]" %(node.functionName, parent.functionName))
# 	print("len ==== %d", length)
#     # if (len(block.clist) > 100):
#     #     for b in block.clist:
#     #         print("%s %s %s dump: [%s, %s]" %(b.blockName, b.modelName, b.functionName, b.begin_tc, b.begin_tt))
#     #         return

#     # for i in range(depth):
#     #     print("  ")
#     # print("%s %s %s Begin: [%s, %s]" %(block.blockName, block.modelName, block.functionName, block.begin_tc, block.begin_tt))
#     for b in block.clist:
#         print "root info : [%s %s] child count = %d" %(b.modelName, b.functionName, len(block.clist))
#         dump(b, depth+1)
#     # for i in range(depth):
#     #     print("  ")
#     # print("%s %s %s End: [%s, %s], Total Cost [%d, %d]" %(block.blockName, block.modelName, block.functionName, block.end_tc, block.end_tt, 
#     #     int(block.end_tc) - int(block.begin_tc), int(block.end_tt) - int(block.begin_tt)));


def dump(block, depth):
    length = len(block.clist)
    print("len ==== %d", length)
    for i in range(depth):
    	print "        "
    for b in block.clist:
        print "root info : [%s %s] child count = %d   %d" %(b.modelName, b.functionName, len(block.clist), depth)
        dump(b, depth+1)


file = open("snap.log")
root = LifeBlock(None, "Root")
stack = []
depth = 0
parent = root
for line in file.readlines():
    if not line:
        break
    elif re.search(regBegin, line) or re.search(regEnd, line):
        appName,tc,tt,modelName,functionName = parseInfo(line)
        if (functionName == "NQPngTexture::bind" or "updatePaintNode" in line or "loadResAfterSnapshot" in line):
            continue
        #print("appName %s tc %s tt %s modelName %s functionName %s" %(appName, tc, tt, modelName, functionName))
        if re.search("\[begin\]", line):
            depth = depth + 1
            node = LifeBlock(root, appName, modelName, functionName)
            #addChild(node, depth)
            node.begin_tc = tc
            node.begin_tt = tt
            node.setParent(parent);
            print ("set node [%s] with parent [%s]" %(node.functionName, parent.functionName))
            parent = node
            stack.append(node)
            #print("push depth %d app %s model %s function %s   [%s %s]", depth, appName, modelName, functionName, tc, tt)
        elif re.search("\[end\]", line):
                if len(stack) == 0:
                	print "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
                    #break
                lastNode = stack.pop()

                #print("pop depth %d app %s model %s function %s        [%s %s]", depth, lastNode.blockName, lastNode.modelName, lastNode.functionName, tc ,tt)
                depth = depth - 1
                if lastNode.modelName == modelName and lastNode.functionName == functionName:
                    lastNode.end_tc = tc
                    lastNode.end_tt = tt
                    #print("app %s depth %d model %s function %s  Total Cost [%d, %d]" %(lastNode.blockName, depth, lastNode.modelName, lastNode.functionName, 
                    #int(lastNode.end_tc) - int(lastNode.begin_tc), int(lastNode.end_tt) - int(lastNode.begin_tt)));
                    #break
                else:
                    print("lastNode.modelName %s lastNode.functionName%s" %(lastNode.modelName, lastNode.functionName));
                    print("modelName %s functionName%s" %(modelName, functionName));
                    print "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
                if (len(stack) == 0):
                    parent = root
                else:
                    parent = stack[len(stack) - 1]
                print ("pop---> parent [%s] [%s]" %(parent.modelName, parent.functionName))
        else:
            continue

#dump(root, 0)
file.close()

# for line in file.readlines():
#     if not line:
#         break
#     elif re.search(regBegin, line) or re.search(regEnd, line):
#         appName,tc,tt,modelName,functionName = parseInfo(line)
#         if (functionName == "NQPngTexture::bind" or "updatePaintNode" in line):
#             continue
#         #print("appName %s tc %s tt %s modelName %s functionName %s" %(appName, tc, tt, modelName, functionName))
#         if re.search("begin", line):
#             depth = depth + 1
#             node = LifeBlock(root, appName, modelName, functionName)
#             node.begin_tc = tc
#             node.begin_tt = tt
#             stack.append(node)
#             #print("push depth %d app %s model %s function %s   [%s %s]", depth, appName, modelName, functionName, tc, tt)
#         elif re.search("\[end\]", line):
#             while 1:
#                 if len(stack) == 0:
#                     break
#                 lastNode = stack.pop()
#                 #print("pop depth %d app %s model %s function %s        [%s %s]", depth, lastNode.blockName, lastNode.modelName, lastNode.functionName, tc ,tt)
#                 depth = depth - 1
#                 if lastNode.modelName == modelName and lastNode.functionName == functionName:
#                     lastNode.end_tc = tc
#                     lastNode.end_tt = tt
#                     print("app %s depth %d model %s function %s  Total Cost [%d, %d]" %(node.blockName, depth, node.modelName, node.functionName, 
#                     int(node.end_tc) - int(node.begin_tc), int(node.end_tt) - int(node.begin_tt)));
#                     break
#         else:
#             continue
