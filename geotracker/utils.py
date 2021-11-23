class Utils():

    def __init__(self):
        pass

    def find_centers(self, topright, bottomleft):
        lats = []
        lons = []
        point = {}
        unit = (topright[0] - bottomleft[0])/2
        for i in range(3):
            lats.append(bottomleft[0]+i*unit)
            lons.append(bottomleft[1]+i*unit)
        for e in range(3):
            point[e] = f"{lats[e]},{lons[e]}"
        point[3] = f'{lats[2]},{lons[0]}'
        point[4] = f'{lats[0]},{lons[2]}'
        return point

# if __name__=="__main__":
