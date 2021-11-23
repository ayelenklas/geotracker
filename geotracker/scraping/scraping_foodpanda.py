''' Scraping Food Panda's website'''

import csv
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options=options,
                          executable_path=r'C:\path\to\chromedriver.exe')
driver.get('http://google.com/')


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


lat = []
lon = []
with open('Berlin Zip Codes - Sheet1.csv') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        lat.append(row['Lat'])
        lon.append(row['Lon'])


driver.get(
    "https://www.foodpanda.de/restaurants/new?lat={lat[0]}&lng={lon[0]}&vertical=restaurants"
)
print(driver.select_elements_by_css('*'))
