from argparse import ArgumentParser
import boto3
import os
import sys
from os import environ
import cv2
import sys
import time
from time import sleep

def get_client():
  key_id = os.getenv('KEY_THAT_MIGHT_EXIST', 'AKIAIJFQ6JL7JQ3MCTVQ')
  secret_key = os.getenv('blhhh','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')
  if not key_id or not secret_key:
    raise Exception('Missing AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, or AWS_SESSION_TOKEN')
  client = boto3.client('rekognition', region_name='us-west-2', verify=False,aws_access_key_id=key_id,aws_secret_access_key=secret_key)
  return client

 
def search_face():
   client = get_client()
  
   with open(path, 'rb') as image:
      response = client.search_faces_by_image(CollectionId='trial',Image={'Bytes': image.read()},MaxFaces=1)
   try:    
      print "face ID: %s" % response['FaceMatches'][0]['Face']['FaceId'] 
      print "hello %s" % response['FaceMatches'][0]['Face']['ExternalImageId']
   except IndexError:
     index_face()
   
   
   
def index_face():
   client = get_client()
   
   name= raw_input("You look new, please enter your name: ")
   with open(path, 'rb') as image:
       response = client.index_faces(CollectionId='trial',Image={'Bytes': image.read()},ExternalImageId=name)
   print "congo, your face has been stored in database"
   




cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
i=0
count=0
blhh=0
flag = 0
path = '/Users/parasmanisharma/Desktop/frame0.jpg'

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    cv2.waitKey(10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if flag == 0:
       start = time.time()
    flag = flag+1

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
      x =faces.size
      lap1= time.time()           #NEED CODE IMPROVISATION HERE
      flag = 0
      if (start- lap1 ) > 5:
        
        if x>0 :     #face detected by opencv
           cv2.imwrite("frame%d.jpg" % count, frame)     # save frame as JPEG file
           img_file= "frame%d.jpg" % count
           print "file saved %s" % img_file
           
           
        if blhh==0:
           blhh = blhh+1
           sleep(1)
        else:  
           blhh=0
           print "calling face detection"
           search_face()
    
    # Display the resulting frame
    
   
