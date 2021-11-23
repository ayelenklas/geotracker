import pickle
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def convert_rating(rating_attribute):
    """
    Takes the rating string which looks like 'width: 100%;' and converts it into the 
    a 0-5 star rating 
    """
    found = re.search(r"[0-9]{1,3}", rating_attribute)
    return int(found[0]) / 20
    
convert_rating('width: 100%;')


def main():
    # Unpickle zip code list
    with open('../geotracker/data/zip.pkl', 'rb') as f:
        zip_codes = pickle.load(f)
        
    # Create iterable list of URLS for the scraper
    base_url = "https://www.lieferando.de/en/delivery/food/berlin-"
    urls = [base_url + zip_code for zip_code in zip_codes]

    # Set selenium options
    options = Options()
    options.add_argument("--headless")  # Starts driver without opening a window
    driver = webdriver.Firefox(options=options)
    soup = BeautifulSoup(driver.page_source, "html.parser") # dumping page source to BeautifulSoup
    
    
    
    # Restaurant list that contains all restaurants for all ZIP code iterations
    restaurant_list = []



    ############
    ### FIRST LOOP: ZIP CODE LEVEL 
    ############
    for url in urls:
        print("opening url:", url)
        driver.get(url)
        WebDriverWait(driver, 5)
        
        # Restaurant names and URLS 
        restaurants_names = driver.find_elements(By.XPATH, "//a[@class='restaurantname notranslate']")
        restaurant_urls = []
        restaurant_names = []
        for restaurant in restaurants_names:
            restaurant_urls.append(restaurant.get_attribute("href"))
            restaurant_names.append(restaurant.text)
            
        # Reviews 
        reviews = soup.find_all("div", class_="review-rating")[ :len(restaurant_names)]
        
        restaurant_reviews = []
        for review in reviews:
            rating = review.find("span").get("style")
            restaurant_reviews.append(convert_rating(rating))
        
        # Number of ratings
        total_ratings = soup.find_all("span", class_="rating-total")[ :len(restaurants_names)]
        
        restaurant_rating_totals = []
        for ratings in total_ratings:
            total_rating = ratings.text.strip()
            total_rating = re.search(r"[0-9]{1,5}", total_rating)[0]
            restaurant_rating_totals.append(int(total_rating))
        
        # Cuisines
        kitchens = soup.find_all("div", class_="kitchens")[ :len(restaurant_names)]

        restaurant_kitchens = [kitchen.find("span").text for kitchen in kitchens]
        
        # Restaurant list at the end of the ZIP CODE LEVEL LOOP 
        for restaurant_name, restaurant_url, restaurant_review, restaurant_rating_total, restaurant_kitchen in zip(restaurant_names, restaurant_urls, restaurant_reviews, restaurant_rating_totals, restaurant_kitchens):
            restaurant_list.append(
                dict(restaurant_name=restaurant_name,
                    restaurant_url=restaurant_url, 
                    avg_review_score=restaurant_review, 
                    reviews=restaurant_rating_total, 
                    type_of_cuisine=restaurant_kitchen))

        
    ############
    ### SECOND LOOP: Restaurant Pages
    ############
    print("##### SECOND LOOP: Restaurant Pages #######")
    print("dropping duplicate restaurants")
    df = pd.DataFrame(restaurant_list)
    df.drop_duplicates(subset=['restaurant_url'], inplace=True)
    
    # Restaurant urls for iteration
    restaurant_urls = list(df["restaurant_url"])
    print(f"scraping {len(restaurant_urls)} restaurant pages")
    
    street_list = []
    zip_code_list = []
    city_list = []
    for restaurant in restaurant_list:
        driver.get(restaurant.get("restaurant_url"))
        wait = WebDriverWait(driver, 15)
        wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//button[@class='info info-icon js-open-info-tab']")))

        # Clicking the button to show the address
        button = driver.find_element(By.XPATH, "//button[@class='info info-icon js-open-info-tab']")
        button.click()
        
        # Wait after button click
        wait.until(ec.visibility_of_element_located(
            (By.XPATH, "//section[@class='card-body notranslate']")))
        
        # Extract the street, zip_code and city from the address box
        address = driver.find_element(By.XPATH, "//section[@class='card-body notranslate']").text
        street = re.search(r".*", address)[0]
        zip_code = re.search(r"[0-9]{5}", address)[0]
        city = re.search(r"[\w]+$", address)[0]
        
        # add the new variables to dictionaries in restaurant_list
        street_list.append(street)
        zip_code_list.append(zip_code)
        city_list.append(city)
        
    ##########
    ### EXPANDING A DATA FRAME AND EXPORT
    ##########
    df["street"] = street_list
    df["zip_code"] = zip_code_list
    df["city"] = city
    
    df.to_csv("lieferando_restaurants.csv")


if __name__ == "__main__":
    main()
            