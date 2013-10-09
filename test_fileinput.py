#!/bin/env python
import fileinput
import os
import glob
import string

for line in fileinput.input("test.txt"):
    print line.strip()

for line in fileinput.input(glob.glob("*.txt")):
    if fileinput.isfirstline():
	print "########## read %s ##########" % fileinput.filename()
    print str(fileinput.lineno()) + string.upper(line.strip())
