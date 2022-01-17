"""
This was used as alternative way to find Instagram locations. We had more success with using
Google Maps script (find_addresses_in_area.py) followed by the
convert_addresses_to_insta_locations.py script.
"""

import random
import json
from time import sleep
from shapely.geometry import Point, shape
from ipyleaflet import Map, Marker, GeoJSON
import geocoder
import instaloader


def generate_random(area):
    minx, miny, maxx, maxy = area.bounds
    while True:
        if area.contains(pnt := Point(random.uniform(minx, maxx), random.uniform(miny, maxy))):
            return pnt


def find_insta_locs(L, address):
    locs = instaloader.TopSearchResults(L.context, address).get_locations()
    res = set()
    while True:
        try:
            res.add(next(locs))
        except KeyError:
            continue
        except StopIteration:
            break
    return res


with open("Boundary.geojson") as f:  # This could be a city boundary, for instance
    boundary = json.load(f)
areadata = boundary['features'][1]['geometry']
area = shape(areadata)


L = instaloader.Instaloader()

instalocs = set()
while True:  # This runs until you stop it
    sleep(3)
    p = generate_random(area)
    g = geocoder.osm([p.y, p.x], method='reverse')
    if area.contains(Point(g.lng, g.lat)):
        search_results = find_insta_locs(
            L, f'{g.street} {g.housenumber} {g.city}')
        for instaloc in search_results.difference(instalocs):
            if area.contains(Point(instaloc.lng, instaloc.lat)):
                instalocs.add(instaloc)
    with open('instalocations.json', 'w') as f:
        json.dump(instalocs, f)
