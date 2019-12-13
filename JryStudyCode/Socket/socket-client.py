#!/usr/bin/env python
import socket
import os
for i in range(107):
	ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ss.connect(('127.0.0.1',1234))
	#f=open('aa','wb')
	stro =  'hello server send'+str(i)
	ss.sendall(stro)
	#os.system('sleep 1')
	#ss.send('EOF')
	data=ss.recv(1024)
	print "server recv %s"%data
	ss.close()