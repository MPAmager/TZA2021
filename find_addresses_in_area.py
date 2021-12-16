"""
This script needs a Google Maps key, as well as a json file called points.json,
which should be dictionary like. Keys should a string of longitude, latitude like '55.66163, 12.58914',
and values should be the radius to search in meters around that point.
"""

from time import sleep
import json
from tqdm.autonotebook import tqdm
import googlemaps

KEY = ''
with open('points.json', 'r') as f:
    points = json.load(f)

gmaps = googlemaps.Client(key=KEY)


def get_nearby_places(loc_str, rad):
    gmaps_results = []
    params = {'location': loc_str, 'radius': rad}
    data = gmaps.places_nearby(**params)
    gmaps_results.extend(data['results'])
    sleep(10)

    while True:
        if 'next_page_token' in data:
            params['page_token'] = data['next_page_token']
            data = gmaps.places_nearby(**params)
            gmaps_results.extend(data['results'])
            sleep(10)
        else:
            break

    return gmaps_results


places = []
for loc_str, rad in tqdm(points.items()):
    res = get_nearby_places(loc_str, rad)
    places.extend(res)

with open('addresses.json') as f:
    json.dump(places, f)
