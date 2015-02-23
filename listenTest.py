"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
"""Modified with code from : https://chrisbaume.wordpress.com/2013/02/09/aubio-alsaaudio/" """
import pyaudio,struct
from aubio.task import *


# Defines constants for the audio components. Don't change probably
CHUNK = 512 
FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
PITCHALG    = aubio_pitch_yin
PITCHOUT    = aubio_pitchm_freq


#Open listening stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
                

# set up pitch detect
detect = new_aubio_pitchdetection(CHUNK,CHUNK/2,CHANNELS,
                                  RATE,PITCHALG,PITCHOUT)
buf = new_fvec(CHUNK,CHANNELS)

print("* recording")

frames = []

#Record audio for given time
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    if i%5 == 0:
		floats = struct.unpack('f'*(len(data)/4),data)
		frames.append(floats)
print("* done recording")

#print frames
stream.stop_stream()
stream.close()
p.terminate()

#exit()

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
