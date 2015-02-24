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
		self.Process_Covert_Message()
		self.Decode_Covert_Message()
		#Read_Covert_Message()

	def Listen_for_PT_Message( self ):
		connection, address = self.serversocket.accept()
		
		plainText = threading.Thread(target=self.Read_PT_Message,args =(connection,) )
		#thread.start_new_thread(self.Read_PT_Message, (connection, ))

		#thread.start_new_thread(self.Read_Covert_Message, () )
		covertText = threading.Thread(target=self.Read_Covert_Message )
		
		plainText.start()
		covertText.start()
		
		plainText.join()
		covertText.join()

	def Read_PT_Message( self, connection ):
		buf = connection.recv(1024)
		eof = False
		msg = "PT: "
		while buf and (len(buf) > 0) and (not eof):
			msg = msg+buf
			if(str('\0') in buf):
				eof = True
			else:
				buf = connection.recv(1024)

		self.doneListen.set()
		with open("msg.txt","a+") as f:
			f.write( str(msg) )

	def Read_Covert_Message(self ):
		
		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT,
			                channels=self.CHANNELS,
			                rate=self.RATE,
			                input=True,
			                frames_per_buffer=self.CHUNK)

			# set up pitch detect
		
		
		
		while( not self.doneListen.is_set()):
			
			#print("* recording")

			data = None

			#Record audio for given time
			try:
				for i in range(0, int((self.RATE / self.CHUNK)/20)):
					data = stream.read(self.CHUNK)

					if i%5 == 0 and data!=None:
						floats = struct.unpack('f'*(len(data)/4),data)
						self.frames.append(floats)

			except IOError:
				print "Dropped Frame"
			#else:
				#print "Some other sort of error?"

		#print frames
		stream.stop_stream()
		stream.close()
		p.terminate()

		print "closed"
		#exit()


	def Process_Covert_Message(self):
		print "processing"
			#Write the sample's values into the required data structure
		detect = new_aubio_pitchdetection(self.CHUNK,self.CHUNK/2,self.CHANNELS,
			                self.RATE,self.PITCHALG,self.PITCHOUT)
		
		buf = new_fvec(self.CHUNK,self.CHANNELS)
		
		for count in range(len(self.frames) ):	                
				
			for i in range(len(self.frames[count])):
				fvec_write_sample(buf, self.frames[count][i], 0, i)
	 
			  # find pitch of audio frame
			freq = aubio_pitchdetection(detect,buf)
	 
		#print "\n\n\n\nHEY LISTEN \n{:10.4f}".format(freq)
		
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
			
		#del_fvec(buf)
		#del_aubio_pitchdetection(detect)

	def Decode_Covert_Message(self ):
		#stuff
		print "Decoding!"
		
		readyForChar = True
		char = 0
		bits = []
		secretMessage = ""
		
		for i in range(len(self.valuesHeard)-1):
			
			#has found a gap between sounds
			if self.valuesHeard[i] == -1:
				readyForChar = True
				continue
			
			#windowing, size of 2
			if self.valuesHeard[i] != self.valuesHeard[i+1]:
				print "Failed windowing"
				continue
			
			#end of file sound
			if self.valuesHeard[i] == 2:
				break
			
			if readyForChar == True:
				bits.append(self.valuesHeard[i])
				readyForChar = False
				
		print "Bits Length:",len(bits)
		print bits
		
		with open("SecretMessage.txt","w") as outputFile:		
			for i in range(len(bits)/8):
				for j in range(7):
					print "i: {} j:{}".format(i,j)
					char += bits[i*8 + j]
					char <<= 1
				char += bits[i*8 + 7]
				print "Char:",chr(char)
				secretMessage += chr(char)
				char = 0
			outputFile.write(secretMessage)
			print "Secret Message:",secretMessage
			
		
	def __init__(self):
		print "Hello world"

		# Defines constants for the audio components. Don't change probably
		self.CHUNK = 2048
		self.FORMAT = pyaudio.paFloat32
		self.CHANNELS = 2
		self.RATE = 44100
		self.RECORD_SECONDS = 3
		self.PITCHALG    = aubio_pitch_yin
		self.PITCHOUT    = aubio_pitchm_freq

		# Server consts
		self.PORT = 8349
		self.valuesHeard = []
		self.doneListen = threading.Event()
		self.frames = []
		
		self.main()

if __name__ == "__main__":
	listen = Listener()
	#listen.main()

