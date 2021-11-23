''' Scraping Food Panda's website'''

import csv

lat = []
lon = []
with open('Berlin Zip Codes - Sheet1.csv') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        lat.append(row['Lat'])
        lon.append(row['Lon'])

print (lat)




