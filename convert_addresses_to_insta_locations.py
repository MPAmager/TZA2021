"""
This should be a json file containing a list of addresses, eg. from the
find_addresses_in_area.py script """

import json
import instaloader
from tqdm.autonotebook import tqdm


with open('addresses.json', 'r') as f:
    addresses = json.load(f)

L = instaloader.Instaloader()

locations = {}
for place in tqdm(addresses):
    search = instaloader.TopSearchResults(L.context, place)
    sub_locs = [loc for loc in search.get_locations()]
    locations[place] = sub_locs

with open('locations.json', 'w') as f:
    json.dump(locations, f)
