#!/usr/bin/python

# <span style="margin: 0px; padding: 0px; ">Plist generation example:</span>

from biplist import *
from datetime import datetime
plist = {'aKey':'aValue',
         '0':1.322,
         'now':datetime.now(),
         'list':[1,2,3],
         'tuple':('a','b','c')
         }
try:
    writePlist(plist, "example.plist")
    out = readPlist("example.plist")
    print(out)
except (InvalidPlistException, NotBinaryPlistException), e:
    print "Something bad happened:", e


