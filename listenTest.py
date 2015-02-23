"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
"""Modified with code from : https://chrisbaume.wordpress.com/2013/02/09/aubio-alsaaudio/" """
import pyaudio,struct
from aubio.task import *
import socket
import SocketServer
import thread
import threading
from multiprocessing.pool import ThreadPool

class Listener:


	def main(self):
		# #Open listening stream
		# self.p = pyaudio.PyAudio()
		# self.stream = self.p.open(format=self.FORMAT,
		#                 channels=self.CHANNELS,
		#                 rate=self.RATE,
		#                 input=True,
		#                 frames_per_buffer=self.CHUNK)

		#Setup socet server
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(('localhost', self.PORT))
		self.serversocket.listen(5) # become a server socket, maximum 5 connections

		print "Hello world"

		#thread.start_new_thread(self.Read_Covert_Message, ())
		self.Listen_for_PT_Message()
		#Read_Covert_Message()

	def Listen_for_PT_Message( self ):
		while True:
		    connection, address = self.serversocket.accept()
		    
		    thread.start_new_thread(self.Read_PT_Message, (connection, ))

		    thread.start_new_thread(self.Read_Covert_Message, () )

	def Read_PT_Message( self, connection ):
		buf = connection.recv(1024)
		eof = False
		msg = "PT: "
		while (len(buf) > 0) and (not eof):
			msg = msg . buf
			if(ord('\n') in buf):
				eof = True
			else:
				buf = connection.recv(1024)

		with open("msg.txt","a+") as f:
			f.write( str(msg) )

	def Read_Covert_Message(self ):
		
		global soundDone
		soundDone = False

		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT,
			                channels=self.CHANNELS,
			                rate=self.RATE,
			                input=True,
			                frames_per_buffer=self.CHUNK)

			# set up pitch detect
		detect = new_aubio_pitchdetection(self.CHUNK,self.CHUNK/2,self.CHANNELS,
			                self.RATE,self.PITCHALG,self.PITCHOUT)
		
		frames = []
		frameCount = 0
		while( not soundDone):
			
			buf = new_fvec(self.CHUNK,self.CHANNELS)

			print("* recording")

			
			data = None

			#Record audio for given time
			for i in range(0, int(self.RATE / self.CHUNK)):
			    try:
			    	data = stream.read(self.CHUNK)
			    except IOError:
			    	print "Dropped Frame"

			    if i%5 == 0:
			    	floats = struct.unpack('f'*(len(data)/4),data)
			    	frames.append(floats)


			#self.Process_Covert_Message(frames, buf, detect)
			print("* done recording")

			#self.Process_Covert_Message(frames, buf, detect, frameCount)
			thread.start_new_thread(self.Process_Covert_Message,(frames, buf, detect, frameCount ))

		#print frames
		stream.stop_stream()
		stream.close()
		p.terminate()

		print "closed"
		print self.valuesHeard
		#exit()


	def Process_Covert_Message(self, frames, buf, detect, count):
		print "processing"
			#Write the sample's values into the required data structure
		for i in range(len(frames[count])):
			fvec_write_sample(buf, frames[count][i], 0, i)
	 
		  # find pitch of audio frame
			freq = aubio_pitchdetection(detect,buf)
	 
		  # find energy of audio frame
			#energy = vec_local_energy(buf)
	 
		print "\n\n\n\nHEY LISTEN \n{:10.4f}".format(freq)
		#del_fvec(buf)
		#buf = new_fvec(CHUNK,CHANNELS)
		
		#decide what pitch it was
		if freq < 200:
			print "No pitch"
			self.valuesHeard.append(-1)
		elif freq > 400 and freq < 600:
			print "Read a 0"
			self.valuesHeard.append(0)
		elif freq > 900 and freq < 1100:
			print "Read a 1"
			self.valuesHeard.append(1)
		elif freq > 1400 and freq < 1600:
			print "Read Control sound"
			self.valuesHeard.append(2)
			soundDone = True
		else:
			print "Unknown pitch"

	def Decode_Covert_Message(self ):
		#stuff
		print "Hello world"


	def __init__(self):
		print "Hello world"

		# Defines constants for the audio components. Don't change probably
		self.CHUNK = 1024
		self.FORMAT = pyaudio.paFloat32
		self.CHANNELS = 2
		self.RATE = 44100
		self.RECORD_SECONDS = 3
		self.PITCHALG    = aubio_pitch_yin
		self.PITCHOUT    = aubio_pitchm_freq

		# Server consts
		self.PORT = 8349
		self.valuesHeard = []
		self.main()

if __name__ == "__main__":
	listen = Listener()
	#listen.main()

