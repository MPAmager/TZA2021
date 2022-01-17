import json
import folium

with open('places.json', 'r') as f:
    places = json.load(f)

m = folium.Map(location=[55.663493879220084,
                         12.584972585072657], zoom_start=15)

for place in places:
    folium.Marker(
        [place['geometry']['location']['lat'],
         place['geometry']['location']['lng']],
        popup=place['name']
    ).add_to(m)

m
