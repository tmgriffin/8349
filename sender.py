import socket
import sys
import signal
import threading
import thread
import audiogen
import os
import contextlib

#handles the SIGINT
def handler(signal, frame):
	if thread.get_ident() == MAINTHREAD:
		sys.__stdout__.write('End of file!')
		sock = frame.f_locals['clientSocket']
		sock.send('\0')
		sock.close()
		exit()
	"""
	else:
		audiogen.sampler.play(audiogen.util.crop(audiogen.tone(3000), .2),True)
		thread.exit()
		os.kill(os.getpid(),signal.SIGINT)
	"""

#context manager to avoid unnecessary prints
@contextlib.contextmanager
def nullPrint():
	try:
		old_stdout = sys.stdout
		sys.stdout = open(os.devnull, 'w')
		yield
	finally:
		sys.stdout = old_stdout

#The method to be threaded to read the file and beep a lot
def soundSend():

	#Generators for each of the pitches. Need to adjust numbers
	#zeroGen = (audiogen.util.crop(audiogen.tone(1000), .2))
	#oneGen = (audiogen.util.crop(audiogen.tone(2000), .2))
	#controlGen = (audiogen.util.crop(audiogen.tone(3000), .2))
	#audiogen.sampler.play(zeroGen)

	with open(sys.argv[2], 'rb') as f, nullPrint():
		byte = f.read(1)
		mask = 1
		char = 'a'
		#print "Hello: ",byte
		while len(byte) > 0:
			bit = 0
			byte = ord(byte)
			for i in reversed(range(1,8)):
				
				#Two commented lines are used to reconstruct bytes
				#bit += (mask & (byte>>i))
				#bit = bit<<1
				bit = (mask & (byte>>i))
				if bit == 0:
					audiogen.sampler.play(audiogen.util.crop(audiogen.tone(1000), .2),True)
				else:
					audiogen.sampler.play(audiogen.util.crop(audiogen.tone(2000), .2),True)
				
				#print "Step",i,": ",bit
			#bit += (mask & (byte))
			
			#print "After:",chr(bit)
			byte = f.read(1)
			
				
def main():
	PORT = 8349
	global MAINTHREAD
	MAINTHREAD = thread.get_ident()
	
	if len(sys.argv) < 3:
		print "Usage: $python sender.py <destination IP> <Secret File>"
		exit()

	#Test run of method, before putting in own thread
	#soundSend()
	soundThread = threading.Thread(target=soundSend)
	soundThread.start()
	
	#Set signal handler and create socket
	signal.signal(signal.SIGINT, handler)
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((sys.argv[1],8349)) 

	print "Type data to send, or CTRL-C to finish"

	#send lines of text until interrupt
	while True:
		line = raw_input()
		clientSocket.send(line)
		clientSocket.send("\n")
	
	
if __name__ == "__main__":
	main()
	#soundSend()
