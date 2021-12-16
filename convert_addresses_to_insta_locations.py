import json
import instaloader
from tqdm.autonotebook import tqdm


with open('addresses.json', 'r') as f:
    addresses = json.load(f)  # This should be a json file containing a list of addresses

L = instaloader.Instaloader()

locations = {}
for place in tqdm(addresses):
    search = instaloader.TopSearchResults(L.context, place)
    g = search.get_locations()

    sub_locs = []  # Each place may return multiple locations
    while True:
        loc = next(g)
        sub_locs.append(loc)

    locations[place] = sub_locs

with open('locations.json', 'w') as f:
    json.dump(locations, f)
