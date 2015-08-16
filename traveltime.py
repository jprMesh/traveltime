import requests
import json

baseURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
lat = 42.4030636
lon = -71.1256341
home = str(lat)+','+str(lon)
dests = []
for x in xrange(36):
    dests.append(str(lat+0.001*(x//6))+','+str(lon+0.001*(x%6)))
destinations = '|'.join(dests)
call = 'origins='+home+'&destinations='+destinations
r = requests.get(baseURL+call)
resp = json.loads(r.text)

print(json.dumps(resp, indent=1))
for location in resp["rows"][0]["elements"]:
    print(location["duration"]["text"])

#print(json.dumps(json.loads(r.text)['match'], indent=1))
