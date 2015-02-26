import socket
import sys
import signal
import threading
import thread
import audiogen
import os
import contextlib
import time

#handles the SIGINT
def handler(signal, frame):
	if thread.get_ident() == MAINTHREAD:
		sys.__stdout__.write('End of file!')
		sock = frame.f_locals['clientSocket']
		sock.send('\0')
		sock.close()
		exit()

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

	# open file with secret message
	with open(sys.argv[2], 'rb') as f, nullPrint():
		byte = f.read(1)
		mask = 1
		char = 'a'
		
		#wait for the other side to start
		time.sleep(1)
		
		# process 1 byte at a time
		while len(byte) > 0:
			bit = 0
			# convert ascii into decimal equivalent
			byte = ord(byte)
			# convert decimal byte into binary bits
			# play corresponding tone for each bit
			for i in reversed(range(8)):
				bit = (mask & (byte>>i))
				if bit == 0:
					audiogen.sampler.play(audiogen.util.crop(audiogen.tone(1000), .2),True)
				else:
					audiogen.sampler.play(audiogen.util.crop(audiogen.tone(2000), .2),True)
				
			byte = f.read(1)
			
		# play tone signaling eof
		audiogen.sampler.play(audiogen.util.crop(audiogen.tone(3000), .4),True)
			
				
def main():
	PORT = 8349
	global MAINTHREAD
	MAINTHREAD = thread.get_ident()
	
	if len(sys.argv) < 3:
		print "Usage: $python sender.py <destination IP> <Secret File>"
		exit()

	#Read & process secret message on separate thread
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
	
	soundThread.join()
	
if __name__ == "__main__":
	main()
