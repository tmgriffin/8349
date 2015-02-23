import socket
import sys
import signal
import threading
import audiogen

def handler(signal, frame):
	print('End of file!')
	sock = frame.f_locals['clientSocket']
	sock.close()
	exit()

def soundSend():

	#Generators for each of the pitches. Need to adjust numbers
	zeroGen = audiogen.util.crop(audiogen.tone(1000), .2)
	oneGen = audiogen.util.crop(audiogen.tone(2000), .2)
	controlGen = audiogen.util.crop(audiogen.tone(3000), .2)
	audiogen.sampler.play(zeroGen)

PORT = 8349

if len(sys.argv) < 3:
	print "Usage: $python sender.py <destination IP> <Secret File>"
	exit()

soundSend()

signal.signal(signal.SIGINT, handler)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((sys.argv[1],8349)) 

print "Type data to send, or CTRL-C to finish"

while True:
	line = raw_input()
	clientSocket.send(line)
	clientSocket.send("\n")
