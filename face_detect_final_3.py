import cv2
import sys
import httplib, urllib, base64
import json
import os
from time import sleep


def add_face(person_id):
   headers = {
       # Request headers
       'Content-Type': 'application/octet-stream',
       'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }
   
   
   body1={}
   body1['personGroupId']='1210'
   body1['personId']=person_id
   body1_d=json.dumps(body1)
   params = urllib.urlencode(body1)
   body=""
   f = open(img_file, "rb")
   body = f.read()
   f.close()

   try:
       conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
       conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params,body,headers)
       response = conn.getresponse()
       data = response.read()
       print(data)
       print "Your face has been added to your person Id"
       conn.close()
   except Exception as e:
       print("[Errno {0}] {1}".format(e.errno, e.strerror))
       



def add_person(name):
  headers = {
      # Request headers
      'Content-Type': 'application/json',
      'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
  }

  params = urllib.urlencode({
    'personGroupId':'1210'
  })
  body = {}
  body["name"]= name
  body_d=json.dumps(body)
  
 
  conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
  conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % params, body_d, headers)
  response = conn.getresponse()
  data = response.read()
  print "please note down your Unique person ID while i am training myself"
  print(data)
  person_id=json.loads(data)
  person__id=person_id['personId']
  conn.close()
  add_face(person__id)

       
       
       
       
def train_group(): 
   headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }

   params = urllib.urlencode({
   'personGroupId':'1210'
   })

   try:
       conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
       conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/train?%s" % params, "{}", headers)
       response = conn.getresponse()
       data = response.read()
       print(data)
       print "Training complete"
       conn.close()
   except Exception as e:
       print("[Errno {0}] {1}".format(e.errno, e.strerror))
       





def face_detection():
   k='0'
   headers = {
        # Request headers
       'Content-Type': 'application/octet-stream',
       'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }
   
   params = urllib.urlencode({
       # Request parameters
       'returnFaceId': 'true',
       'returnFaceLandmarks': 'false'
   })

   body=""
   f = open(img_file, "rb")
   body = f.read()
   f.close()

   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
   conn.request("POST", "/face/v1.0/detect?%s" % params,body, headers)
   response = conn.getresponse()
   data = response.read()

   #checking if any face is detected
   if data=="[]": 
      j=2000
   else:
      kim = json.loads(data)
      l= kim[0]['faceId']   #faceId received
      print l
      k =json.dumps(l)

    
    
   #################################################
      #sending faceId to server for identification
   
   headers = {
       # Request headers
       'Content-Type': 'application/json',
       'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }
   
   
   params = urllib.urlencode({
   })
    
    
   conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
   conn.request("POST", "/face/v1.0/identify?%s" % params, '{"personGroupId":"1210","faceIds":['+k+']}',headers)
    
    #personId recieved
   response = conn.getresponse()
   data = response.read()
   data_json=json.loads(data)
   print data
   try :
      if data_json['error']['code'] == 'FaceNotFound': 
          j=2000
   except TypeError:
       print "exception 1 successfully applied"
   try: 
      candidate=data_json[0]['candidates']
      #if new face, ask for name
      if candidate==[] :
          name = raw_input("You look new, please enter your name:")
          add_person(name)
          train_group()
   except KeyError:
       print "exception 2 successfullt applied" 
   
   print(data)     
   conn.close()
       
   
       

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
i=0
count=0
blhh=0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    cv2.waitKey(10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
        if x>0 :     #face detected by opencv
           cv2.imwrite("frame%d.jpg" % count, frame)     # save frame as JPEG file
           img_file= "frame%d.jpg" % count
           print "file saved %s" % img_file
        else :
           print "eroor capturing image"
        if blhh==0:
           blhh = blhh+1
           sleep(1)
        else:  
           blhh=0
           print "calling face detection"
           face_detection()
    
    # Display the resulting frame
    
    
    
  
    
    
