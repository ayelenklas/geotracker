from geotracker.utils import Utils

URL = 'https://places.ls.hereapi.com/places/v1/discover/search'

with open('key.txt') as f:
    HERE_API_KEY = f.readlines()[0]

SIZE=5
RANGE=4000

BL = (52.4027,13.2054)
TR = (52.631,13.598)

# arg[0] -> top right arg[1] -> bottom left
point = Utils().find_centers(TR, BL)

# example "in=52.521,13.3807;r=7768"
PARAMS = []
for value in point.values():
    PARAMS.append(
        dict(
        q="restaurant",
        size=SIZE,
        apiKey=HERE_API_KEY,
        **{"in":f'{value};r={RANGE}'}
        )
    )

with open('key.txt') as f:
    HERE_API_KEY = f.readlines()[0]