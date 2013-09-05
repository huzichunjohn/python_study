#!/bin/env python

def test():
    for attr in [0,1,4,5,7,8]:
	for fore in [30,31,32,33,34,35,36,37]:
	    for back in [40,41,42,43,44,45,46,47]:
		color = "\x1B[%d;%d;%dm" % (attr,fore,back)
		print "%s %d-%d-%d\x1B[0m" % (color,attr,fore,back)
	    print ""

if __name__ == "__main__":
    test()




