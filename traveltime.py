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

mapjs = 'var heatMapData = \n'
mapitem = '  {{location: new google.maps.LatLng({latlon}), weight: {weight}}}'
mapjsBot = '''
];

var pindrop = new google.maps.LatLng({lat}, {lon});

map = new google.maps.Map(document.getElementById('map'), {{
  center: pindrop,
  zoom: 13,
  mapTypeId: google.maps.MapTypeId.SATELLITE
}});

var heatmap = new google.maps.visualization.HeatmapLayer({{
  data: heatMapData
}});
heatmap.setMap(map);
'''.format(lat=lat, lon=lon)

mapjs += ',\n'.join([mapitem.format(latlon=dests[index],
                   weight=resp["rows"][0]["elements"][index]["duration"]["value"]) for index in xrange(len(resp["rows"][0]["elements"]))])
# for index in xrange(len(resp["rows"][0]["elements"])):
#     mapjs += mapitem.format(latlon=dests[index], weight=resp["rows"][0]["elements"][index]["duration"]["value"])
mapjs += mapjsBot

print(mapjs)