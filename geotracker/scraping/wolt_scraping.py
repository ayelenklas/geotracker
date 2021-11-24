# scraping imports
import requests
from bs4 import BeautifulSoup

# data wrangling imports
import numpy as np
import pandas as pd

# data visualization imports
import matplotlib.pyplot as plt

# other imports
import csv

# method to extract and create a list with all zip codes
filename = '../../raw_data/Berlin Zip Codes - Sheet1.csv'
def zip_codes(file):
    zip_codes_list = []
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            zip_codes_list.append(row[1])
    return zip_codes_list[1:]

# list with all Berlin zipcodes
zip_code_list = zip_codes(filename)
