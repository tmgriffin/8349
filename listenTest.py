"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
"""Modified with code from : https://chrisbaume.wordpress.com/2013/02/09/aubio-alsaaudio/" """
import pyaudio,struct
from aubio.task import *
import socket
import SocketServer
import threading
from multiprocessing.pool import ThreadPool


# Defines constants for the audio components. Don't change probably
CHUNK = 1024 
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
PITCHALG    = aubio_pitch_yin
PITCHOUT    = aubio_pitchm_freq

# Server consts
PORT = 8349


#Open listening stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

#Setup socet server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', PORT))
serversocket.listen(5) # become a server socket, maximum 5 connections

Listen_for_PT_Message()

def Listen_for_PT_Message():
	while True:
	    connection, address = serversocket.accept()
	    
	    thread.start_new_thread(Read_PT_Message, (connection, ))

	    thread.start_new_thread(Read_Covert_Message, () )

def Read_PT_Message( connection ):
	buf = connection.recv(1024)
	eof = False
	msg = "PT: "
	while len(buf) > 0 && !eof:
		msg = msg . buf
		if(ord('\0') in buf):
			eof = True
		else:
			buf = connection.recv(1024)

	with open("msg.txt","a+") as f:
		f.write( str(msg) )

def Read_Covert_Message():
	# set up pitch detect
	detect = new_aubio_pitchdetection(CHUNK,CHUNK/2,CHANNELS,
	                                  RATE,PITCHALG,PITCHOUT)
	buf = new_fvec(CHUNK,CHANNELS)

	eof = False

	while(!eof):
		print("* recording")

		frames = []

		#Record audio for given time
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    
		    if i%5 == 0:
				floats = struct.unpack('f'*(len(data)/4),data)
				frames.append(floats)

		print("* done recording")

		thread.start_new_thread( Process_Covert_Message,( frames, ) )

	#print frames
	stream.stop_stream()
	stream.close()
	p.terminate()

	#exit()


def Process_Covert_Message(frames):
	for j in range(len(frames)):
		
		#Write the sample's values into the required data structure
		for i in range(len(frames[j])):
			fvec_write_sample(buf, frames[j][i], 0, i)
	 
		  # find pitch of audio frame
			freq = aubio_pitchdetection(detect,buf)
	 
		  # find energy of audio frame
			#energy = vec_local_energy(buf)
	 
		print "\n\n\n\nHEY LISTEN \n{:10.4f}".format(freq)
		#del_fvec(buf)
		#buf = new_fvec(CHUNK,CHANNELS)


def Decode_Covert_Message():
	#stuff
	print "Hello world"
