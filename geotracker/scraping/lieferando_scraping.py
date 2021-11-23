import pickle
from bs4 import BeautifulSoup
from selenium import webdriver


# Unpickle zip code list
with open('geotracker/data/zip.pkl', 'rb') as f:
    zip_codes = pickle.load(f)

print(zip_codes)