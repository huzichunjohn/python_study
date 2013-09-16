#!/bin/env python

def compare(x, y):
    if x >= y:
	return 1
    else:
	return 0 
	
if __name__ == "__main__":
    print compare(1,2)
    print compare(3,3)
    print compare(7,5)
