import pyaudio
import wave
import audioop
from collections import deque
import os
import urllib2
import urllib
import time
import math
import argparse
import base64
import json
import httplib2


from termios import tcflush, TCIOFLUSH
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')

LANG_CODE = 'en-US'  # Language to use
speech_file= 'output.wav'

# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
num_samples=25
abg = []
for i in range(100):
   abg.append(0)

def send_request():
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    print "Sending Request\n" 
    with open(speech_file, 'rb') as speech:
        speech_content = base64.b64encode(speech.read())
        
        
        
        credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)
        
    service = build('speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
    
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'sampleRate': 44100,  # 16 khz
                'languageCode': 'en-IN',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    response = service_request.execute()
    print(json.dumps(response))
    
    # DO STUFF HERE WITH RECIEVED RESPONSE
    
    




def start_recording() :
  print("* listening")
  stream.stop_stream()
  os.system("say 'listening'")
  stream.start_stream()
  
  average_intensity=2000
  k=0
  

  frames = []

  while average_intensity > 400 :
      k=k+1
      data=stream.read(CHUNK)
      values = [math.sqrt(abs(audioop.avg(data, 4))) for x in range(num_samples)] 
      frames.append(data)
      values = sorted(values, reverse=True)
      r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
      abg[k]=abg[k-1] + r
      if k == 90:
         average_intensity = abg[90]/90
         print average_intensity
         k=0
    

  print("* done listening")
  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()
  send_request()

 
while True :
    
    r = 1500
    print "Getting intensity values from mic."
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    while True:
        values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) for x in range(num_samples)] 
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        
        print "value of intensity is is %d \n" % (r)
        
        if (r>2000) :   # change intensity here according to need of mitra's mic
           start_recording()
           stream.stop_stream()
           time.sleep(6)
           stream.start_stream()
    print " Finished "
    print " Average audio intensity is ", r
    stream.close()
    p.terminate() 
