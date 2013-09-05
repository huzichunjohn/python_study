#!/bin/env python
import time
import thread

count = 0
lock = thread.allocate_lock()
def test():
    global count, lock
    lock.acquire()
    for i in range(0,10000):
	count += 1
    lock.release() 

for i in range(0,10):
    thread.start_new_thread(test,())

time.sleep(5)
print count
    



