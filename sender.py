import socket
import sys
import signal
import threading
import audiogen

#handles the SIGINT
def handler(signal, frame):
	print('End of file!')
	sock = frame.f_locals['clientSocket']
	sock.close()
	exit()

#The method to be threaded to read the file and beep a lot
def soundSend():

	#Generators for each of the pitches. Need to adjust numbers
	zeroGen = audiogen.util.crop(audiogen.tone(1000), .2)
	oneGen = audiogen.util.crop(audiogen.tone(2000), .2)
	controlGen = audiogen.util.crop(audiogen.tone(3000), .2)
	#audiogen.sampler.play(zeroGen)

	with open(argv[2], 'rb') as f:
		byte = f.read(1)
		mask = 1
		char = 'a'
		while len(byte) > 0:
			bit = 0
			for i in reversed(range(8)):
				bit = byte & (mask<<i)
				bit = bit<<1
			print char(bit)
				
def main():
	PORT = 8349

	if len(sys.argv) < 3:
		print "Usage: $python sender.py <destination IP> <Secret File>"
		exit()

	#Test run of method, before putting in own thread
	#soundSend()

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
