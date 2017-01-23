import json
import sys
import httplib, urllib, base64
import os
import glob

headers = {
       # Request headers
       'Content-Type': 'application/octet-stream',
       'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
   }
   
   
body1={}
body1['personGroupId']='1210'
body1['personId']='--fill you person id here--'
body1_d=json.dumps(body1)
params = urllib.urlencode(body1)
body=""
path = '/Users/parasmanisharma/Desktop/images'   # change path to your directory
for filename in os.listdir(path): 
   file = path + "/" + filename
   f = open(file, "rb")
   body = f.read()
   f.close()

   try:
       conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
       conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params,body,headers)
       response = conn.getresponse()
       data = response.read()
       print(data)
       conn.close()
   except Exception as e:
       print("[Errno {0}] {1}".format(e.errno, e.strerror))
       
print "your images has been uploaded successfully!"
       
