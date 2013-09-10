#!/bin/env python
import threading

count = 0

class Test(threading.Thread):
    def __init__(self):
 	super(Test,self).__init__()

    def get_count(self):
	global count
        return count

    def set_count(self,num):
	global count
	count = num

class Test2(threading.Thread):
    def __init__(self):
        super(Test2,self).__init__()

    def get_count(self):
	global count
        return count

    def set_count(self,num):
	global count
        count = num


if __name__ == "__main__":
    test1 = Test()
    print test1.get_count()
    test1.set_count(3)

    test2 = Test2()
    print test2.get_count()
    test2.set_count(5)
    print test1.get_count()
    print test2.get_count()

















