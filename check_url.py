#!/bin/env python
#-*- coding=utf-8 -*-
# Author:  John Hu
# Email:   huzichunjohn@126.com
# Date:    09-09
# Version: 1.0

import os
import optparse
import threading
import Queue
import time
import subprocess
import re

in_queue = Queue.Queue()
out_queue = Queue.Queue()

MAX_GET_THREADS = 100
MAX_PARSE_THREADS = 10

class Put(threading.Thread):
    is_stop = False
    def __init__(self,file):
        self.file = file
        super(Put,self).__init__()
	self.setDaemon(True)

    def run(self):
	global in_queue
        while True:
	    if not self.is_stop and in_queue.qsize() <= 10:
	        for url in get_content(self.file):
                    in_queue.put(url)
	    elif self.is_stop:
		break              
	print "Put Thread: exit ......"

    def stop(self):
        self.is_stop = True

class Get(threading.Thread):
    is_stop = False
    def __init__(self,i):
	self.i = i
	super(Get,self).__init__()
	self.setDaemon(True)

    def run(self):
	global in_queue,out_queue
	while True:
	    if not self.is_stop and in_queue.qsize() > 0:
	        url = in_queue.get()
		print "Thread %s:check [ %s ]" % (self.i,url)
        	cmd = ['/usr/bin/curl','-s','--connect-timeout','10','-m','15','-I',url,'-x',"localhost:6081"]
        	p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
        	result = p.communicate()[0]
        	if p.returncode == 0:
            	    infos = result.split('\r\n')
            	    for info in infos:
                        if re.match('HTTP/1.[0-1]',info):
                            status_code = info.split(' ')[1]
                            break
		    out_queue.put((url,status_code))
        	elif p.returncode == 28:
                    out_queue.put((url,"timeout"))
        	else:
            	    out_queue.put((url,"unknown"))
        	in_queue.task_done()
	    elif self.is_stop:
		break
	    else:
		time.sleep(2)
	print "Get Thread %s: exit ......" % self.i

    def stop(self):
	self.is_stop = True

class Parse(threading.Thread):
    is_stop = False
    def __init__(self):
        super(Parse,self).__init__()
	self.setDaemon(True)

    def run(self):
	global out_queue
	while True:
	    if not self.is_stop and out_queue.qsize() > 0:
		url,detail = out_queue.get()
                print url,detail
		out_queue.task_done()
	    elif self.is_stop:
		break
	    else:
		time.sleep(2)
	print "Parse Thread: exit  ......"

    def stop(self):
        self.is_stop = True

def parse_args():
    parser = optparse.OptionParser("Usage: %prog [options]")
    parser.add_option("-f","--file",dest="file",default="check_url.txt",help="The url list file which we will use to check.")
    parser.add_option("-t",type="int",dest="t",default="5",help="How long we will check.")
    parser.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="Output verbose infomations.")

    (options, args) = parser.parse_args()
    if options.verbose:
        print options, args
    return (options.file,options.t,options.verbose)

def get_content(file):
    result = []
    if os.path.exists(file):
        with open(file) as f:
            for line in f.readlines():
                result.append(line.strip())
	return result
    else:
        raise Exception("The url list file: %s is not exist, please check." % file)

def main():
    file, t, verbose = parse_args()
    put = Put(file)
    put.start()  
 
    get_threads = []
    for i in range(MAX_GET_THREADS):
        get = Get(i)
        get.start()
        get_threads.append(get)

    parse_threads = []
    for i in range(MAX_PARSE_THREADS):
	parse = Parse()
        parse.start()
        parse_threads.append(parse)
  
    try:	 
        print get_threads,parse_threads
        print t
        time.sleep(t)
        put.stop()
        [ t.stop() for t in get_threads ]
        [ t.stop() for t in parse_threads ]
        time.sleep(5)
        print "Master Thread: exit ......"
    except KeyboardInterrupt:
	put.stop()
        [ t.stop() for t in get_threads ]
        [ t.stop() for t in parse_threads ]
	print "Ctrl + c: exit ......"

if __name__ == "__main__":
    main()
