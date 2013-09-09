#!/bin/env python

import threading
import time

class TestThread(threading.Thread):
    is_stop = False

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print self.is_stop
	while not self.is_stop:
	    print "this is a test."
            time.sleep(2)
	print "exit ......"

    def stop(self):
	print "stop ......"
        self.is_stop = True

if __name__ == "__main__":
    t = TestThread()
    t.start()
    print "sleep 5s ......"
    time.sleep(5)
    t.stop()



