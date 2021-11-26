import numpy as np

class Utils:
    def __init__(self):
        pass

    def get_circlegrid(self, topleft, bottomright, spacing=2, overlap=1):

        lats = np.linspace(topleft[0], bottomright[0], spacing)
        lons = np.linspace(bottomright[1], topleft[1], spacing)

        counter = 0
        points = {}
        for lat in lats:
            for lon in lons:
                points[counter] = f'{lat},{lon}'
                counter += 1

        side_lenght = bottomright [0] - topleft[0]
        degradius = (side_lenght/(2 * (spacing - 1))) * overlap
        mradius = abs(1000*(degradius * (40075 * np.cos(topleft[1]) / 360)))

        return points, mradius


    def get_circlegrid_list(self, topleft, bottomright, spacing=2, overlap=1)->list:

        lats = np.linspace(topleft[0], bottomright[0], spacing)
        lons = np.linspace(bottomright[1], topleft[1], spacing)

        points = []
        for lat in lats:
            for lon in lons:
                points.append((lat, lon))

        side_lenght = bottomright [0] - topleft[0]
        degradius = (side_lenght/(2 * (spacing - 1))) * overlap
        mradius = abs(1000*(degradius * (40075 * np.cos(topleft[1]) / 360)))

        return points, mradius








# def size_in_meters(topleft, bottomright):

#     lat_1_rad, lon_1_rad = np.radians(topleft[0]), np.radians(topleft[1])
#     lat_2_rad, lon_2_rad = np.radians(bottomright[0]), np.radians(bottomright[1])
#     dlon = lon_2_rad - lon_1_rad
#     dlat = lat_2_rad - lat_1_rad

#     a = np.sin(dlat / 2.0) ** 2 + np.cos(lat_1_rad) * np.cos(lat_2_rad) * np.sin(dlon / 2.0) ** 2
#     c = 2 * np.arcsin(np.sqrt(a))
#     ipoinm = 6371 * c / 1000
#     catethus = np.sqrt((ipoinm ** 2)/2)

#     return catethus

# if __name__=="__main__":
