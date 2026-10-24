import urllib.request
import urllib.parse
import json

url = "https://geometrygeeks.bike/prove-human-and-load-geometries/"
data = urllib.parse.urlencode({"type": "background"}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(e)
