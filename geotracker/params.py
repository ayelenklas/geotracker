from geotracker.utils import Utils

URL = 'https://places.ls.hereapi.com/places/v1/discover/search'

with open('key.txt') as f:
    HERE_API_KEY = f.readlines()[0]

SIZE=100

TL = (52.635010,13.198130)
BR = (52.39405827510934,13.596147274545292)

# arg[0] -> top left arg[1] -> bottom right
points, radius = Utils().get_circlegrid(TL, BR, 9, 1.2)

# example "in=52.521,13.3807;r=7768"
PARAMS = []
for value in points.values():
    PARAMS.append(
        dict(
        q="restaurant",
        size=SIZE,
        apiKey=HERE_API_KEY,
        **{"in":f'{value};r={radius}'}
        )
    )

with open('key.txt') as f:
    HERE_API_KEY = f.readlines()[0]
