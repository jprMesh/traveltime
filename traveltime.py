import requests
import json

GRIDSIZE = 8

baseURL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
lat = 42.4030636
lon = -71.1256341
home = str(lat)+','+str(lon)
dests = []
for x in xrange(GRIDSIZE**2):
    dests.append(str(lat+0.001*(x//GRIDSIZE))+','+str(lon+0.001*(x%GRIDSIZE)))
destinations = '|'.join(dests)
call = 'origins='+home+'&destinations='+destinations
r = requests.get(baseURL+call)
resp = json.loads(r.text)

mapjs = '''\
<!DOCTYPE html>
<html>
  <head>
    <style type="text/css">
      html, body { height: 100%; margin: 0; padding: 0; }
      #map { height: 100%; }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script type="text/javascript">

"use strict";
var map;
function initMap() {
  var heatMapData = [
'''
mapitem = '    {{location: new google.maps.LatLng({latlon}), weight: {weight}}}'
mapjsBot = '''
  ];
  var pindrop = new google.maps.LatLng({lat}, {lon});

  map = new google.maps.Map(document.getElementById('map'), {{
    center: pindrop,
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.SATELLITE
  }});

  var heatmap = new google.maps.visualization.HeatmapLayer({{
    data: heatMapData,
    dissipating: true,
    radius: 40
  }});
  heatmap.setMap(map);
}}

    </script>
    <script async defer
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCVfTNGdIPK1Unu6VAbsvpcUUv7uvExWVc&libraries=visualization&callback=initMap">
    </script>
  </body>
</html>
'''.format(lat=lat, lon=lon)

mapjs += ',\n'.join([mapitem.format(latlon=dests[index],
                    weight=resp["rows"][0]["elements"][index]["duration"]["value"]) for index in xrange(len(resp["rows"][0]["elements"]))])
# for index in xrange(len(resp["rows"][0]["elements"])):
#     mapjs += mapitem.format(latlon=dests[index], weight=resp["rows"][0]["elements"][index]["duration"]["value"])
mapjs += mapjsBot

#print(mapjs)
with open('bruh.html', 'w') as f:
    f.write(mapjs) 