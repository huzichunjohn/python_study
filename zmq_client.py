#!/bin/env python
import zmq

context = zmq.Context()

print "Connect to server ......"
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

for i in range(10):
    print "Sending request ", i, " ......"
    socket.send("hello")

    message = socket.recv()
    print "Received reply ", i, "[", message, "]"
