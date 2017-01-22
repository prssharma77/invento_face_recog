import cv2
import sys
import httplib, urllib, base64
import json


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
   conn.request("POST", "/face/v1.0/identify?%s" % params, '{"personGroupId":"4","faceIds":['+k+']}',headers)
    
   response = conn.getresponse()
   data = response.read()
    
   #personId received
   print(data)     
   conn.close()
       
       
#Using opencv to detect face in frame and then passing it to API
cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
i=0
count=0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        x =faces.size
        if x>0 :
           cv2.imwrite("frame%d.jpg" % count, frame)     # save frame as JPEG file
           img_file= "frame%d.jpg" % count
           print "file saved %s" % img_file
        else :
           print "0"
        print "calling face detection"
        face_detection()
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    
  
    
    
