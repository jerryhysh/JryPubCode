from multiprocessing import Process,Queue
import os,time,random
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler
import time

#recieve raw message from every client
q = Queue()
max_list = 10
filename = 'raw.txt'
#Socket server for recieve message 
class Server(ThreadingMixIn, TCPServer): pass

class Handler(StreamRequestHandler):

  def handle(self):
    global q
    addr = self.request.getpeername()
    print 'Got connection from ',addr
    data = self.request.recv(1024)
    print "recv from ",self.client_address[0],":",data

    data = str("recv from "+self.client_address[0]+":"+data)
    #write send ip address to the queue
    q.put(data)
    self.wfile.write('Thank you for connection')

def write(q):
	print('Process to write:%s'% os.getpid())
	for value in ['A','B','C','D']:
		print('Put %s to queue...' % value)
		q.put(value)
		time.sleep(random.random())

def read(q):
	print('Process to read: %s' %os.getpid())
	# init a list
	message_list = []
	while True:
		# if the items of the set is > 1000 then deal the set 
		# if deal the set ok then clear the set
		deallist = 0
		if len(message_list)>max_list:
			print message_list
			deallist = deal_list(message_list)
			message_list = []
		if (deallist != max_list):
			dealmore_list(deallist) 
			#message_list = []
		value = q.get(True)
		message_list.append(value)
		#print message_list
		#deal the json style value then appendding the value to a set

		print('Get %s from queue.' % value)

def deal_list(value):
	ISOTIMEFORMAT='%Y-%m-%d %X'
	filecon = '';
	for message in value:
		filecon = str (filecon + str(message+'. '))
	filelen = len(filecon)
	print "\r\n"
	print filelen
	timep = time.strftime( ISOTIMEFORMAT, time.localtime() )
	txtcon = 'save message at :' + str(timep) + "\r\n"
	filecon = filecon[0:len(filecon)-2]
	output = open(filename,'a+')
	filecon = str(filecon)
	filecon +='\r\n'
	txtcon += filecon
	output.write(txtcon)
	output.close()
def dealmore_list(value):
	pass
	# the value must save in the memory of this process
def deal_listdatabase(value):
	pass
	#save the message to the mysql database

if __name__=='__main__':

	pr = Process(target=read,args=(q,))

	#pw.start()

	pr.start()
	#pw.join()
	
	print('Process to write:%s'% os.getpid())
	server = Server(('', 1234), Handler)  
  	server.serve_forever()  
	pr.terminate()