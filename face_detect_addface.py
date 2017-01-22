import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '80693c2ebacf44eb919f8554b48ae038',
}

params = urllib.urlencode({
    # Request parameters
    'personGroupId':'4',
    'personId':'6488c3f6-5e86-4c51-ba87-594e3afda66d'
})

body=""
f = open("IMG_7028.jpg", "rb")
body = f.read()
f.close()
try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))