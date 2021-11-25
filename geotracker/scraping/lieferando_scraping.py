#! python3
# Author: Malte Berneaud
# Date: 24.11.2021
import pickle
from termcolor import cprint
import re
import time
import pandas as pd
import numpy as np
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


def scroll_down(driver):
    """A method for scrolling the page to the bottom."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height


def get_restaurants(zip_codes, start=0, headless=True):
    """
    Takes a list of zip codes and a start integer and then iterates the scraper
    over all zip codes starting from start, scraping the lieferando zip code
    pages for information about restaurants.

    If the scrape failed at a certain iteration previous, we can resume at that
    iteration by setting the start variable to correspond with the index of the last
    correct restaurant list pickle in
    raw_data/lieferando_pickles/restaurant_lists
    """

    # Create iterable list of URLS for the scraper
    base_url = "https://www.lieferando.de/en/delivery/food/berlin-"



    print("##### FIRST LOOP: ZIP CODE PAGES #######")


    # Set selenium options and start driver
    options = Options()
    if headless:
        options.add_argument("--headless")  # Starts driver without opening a window
    driver = webdriver.Firefox(options=options)
    time.sleep(10)

    # Continue iteration from pre-existing pickles if start parameter is specified
    if start != 0:
        with open(
            f"../../raw_data/lieferando_pickles/restaurant_lists/restaurant_list_{start}.pkl", "rb"
        ) as f:
            restaurant_list = pickle.load(f)
    else:
        restaurant_list = []


    # Early exit if all Zip Codes have already been scraped
    if start == len(zip_codes) - 1:
        print("ZIP code page scrape complete, jumping to restaurant page scrape")
        return restaurant_list, driver

    ############
    ### FIRST LOOP: ZIP CODE LEVEL
    ############

    for index, zip_code in enumerate(zip_codes[start:]):

        url = base_url + zip_code
        print("you are on iteration:", index+start)
        print("starting on url:", url)

        # Try loop because sometimes page loads with scroll and sometimes it doesn't
        successful = False
        while not successful:
            print("trying to get restaurantname notranslate")
            driver.get(url)  # Open page
            time.sleep(8)  # Wait some time
            scroll_down(driver)  # Scroll down

            # Restaurant names and URLS
            restaurants_names = driver.find_elements(
                By.XPATH, "//a[@class='restaurantname notranslate']"
            )
            restaurant_urls = []
            restaurant_names = []
            for restaurant in restaurants_names:
                restaurant_urls.append(restaurant.get_attribute("href"))
                restaurant_names.append(restaurant.text)

            # Repeat the function from the beginning if the url list comes back empty
            if len(restaurant_urls) != 0:
                successful = True
                print("succesfully obtained restaurant list")

        # Dump page source into Beautiful Soup for subsequent steps
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Reviews
        reviews = soup.find_all("div", class_="review-rating")[: len(restaurant_names)]

        restaurant_reviews = []
        for review in reviews:
            rating = review.find("span").get("style")
            restaurant_reviews.append(convert_rating(rating))

        # Number of ratings
        total_ratings = soup.find_all("span", class_="rating-total")[
            : len(restaurants_names)
        ]

        restaurant_rating_totals = []
        for ratings in total_ratings:
            total_rating = ratings.text.strip()
            total_rating = re.search(r"[0-9]{1,5}", total_rating)[0]
            restaurant_rating_totals.append(int(total_rating))

        # Cuisines
        kitchens = soup.find_all("div", class_="kitchens")[: len(restaurant_names)]

        restaurant_kitchens = [kitchen.find("span").text for kitchen in kitchens]

        # Restaurant list at the end of the ZIP CODE LEVEL LOOP
        for (
            restaurant_name,
            restaurant_url,
            restaurant_review,
            restaurant_rating_total,
            restaurant_kitchen,
        ) in zip(
            restaurant_names,
            restaurant_urls,
            restaurant_reviews,
            restaurant_rating_totals,
            restaurant_kitchens,
        ):
            restaurant_list.append(
                dict(
                    restaurant_name=restaurant_name,
                    restaurant_url=restaurant_url,
                    avg_review_score=restaurant_review,
                    reviews=restaurant_rating_total,
                    type_of_cuisine=restaurant_kitchen,
                )
            )

        # Intermediate results pickle
        with open(
            f"../../raw_data/lieferando_pickles/restaurant_lists/restaurant_list_{index+start}.pkl",
            "wb",
        ) as f:
            pickle.dump(restaurant_list, f)

    return restaurant_list, driver


def get_addresses(restaurant_list, driver, start=0):
    """
    takes restaurant list generated by get_restaurants and an initiated selenium
    driver as an input and returns a df of that input list enriched with
    address data scraped from restaurant pages.

    If a previous scrape has failed, we can start again at index start that
    corresponds to the index of the most recent pickle dumps in
    raw/data/lieferando_pickles/
    """
    ############
    ### SECOND LOOP: Restaurant Pages
    ############

    print("##### SECOND LOOP: Restaurant Pages #######")
    print("dropping duplicate restaurants")
    print(f"starting scraper from index: {start}")

    # Load data if there is something already
    if start != 0:
        with open(
            f"../../raw_data/lieferando_pickles/street_lists/street_list_{start}.pkl",
            "rb",
        ) as f:
            street_list = pickle.load(f)
        with open(
            f"../../raw_data/lieferando_pickles/zip_code_lists/zip_code_list_{start}.pkl",
            "rb",
        ) as f:
            zip_code_list = pickle.load(f)
        with open(
            f"../../raw_data/lieferando_pickles/city_lists/city_list_{start}.pkl", "rb"
        ) as f:
            city_list = pickle.load(f)
    else:
        street_list = []
        zip_code_list = []
        city_list = []

    df = pd.DataFrame(restaurant_list)
    df.drop_duplicates(subset=["restaurant_url"], inplace=True)

    # Restaurant urls for iteration
    restaurant_urls = list(df["restaurant_url"])

    print(f"{len(restaurant_urls)-start} restaurant pages left to scrape")

    for index, restaurant_url in enumerate(restaurant_urls[start:]):
        print(f"scraping: {restaurant_url} ------ at position: {start+index}")

        # Print progress and pickle intermediate results
        if index % 10 == 0 and index != 0:
            #print(f"reached restaurant number:{index+start}")

            # Pickling intermediate objects
            with open(
                f"../../raw_data/lieferando_pickles/street_lists/street_list_{index+start}.pkl",
                "wb",
            ) as f:
                pickle.dump(street_list, f)
            with open(
                f"../../raw_data/lieferando_pickles/zip_code_lists/zip_code_list_{index+start}.pkl",
                "wb",
            ) as f:
                pickle.dump(zip_code_list, f)
            with open(
                f"../../raw_data/lieferando_pickles/city_lists/city_list_{index+start}.pkl",
                "wb",
            ) as f:
                pickle.dump(city_list, f)


        # Starting restaurant Loop
        successful = False
        tries = 3
        while not successful:
            print(f"trying to get info js button. Remaining tries: {tries}")
            driver.get(restaurant_url)
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(
                ec.visibility_of_element_located(
                    (By.XPATH, "//button[@class='info info-icon js-open-info-tab']")))
            except:
                cprint("failed to locate info info-icon js-open-info-tab. Trying again.", "red")
                tries -= 1
            else:
                successful = True
                cprint("Successfully located info info-icon js-open-info-tab", "green")
            finally:
                if tries == 0:
                    cprint("failed to locate info button after 5 tries. Continuing to next iteration", "red", attrs=['bold'])
                    street_list.append("not found")
                    zip_code_list.append("not found")
                    city_list.append("not found")
                    break

        if tries == 0:
            continue





        # Clicking the button to show the address
        button = driver.find_element(
            By.XPATH, "//button[@class='info info-icon js-open-info-tab']"
        )
        button.click()

        # Wait after button click
        wait.until(
            ec.visibility_of_element_located(
                (By.XPATH, "//section[@class='card-body notranslate']")
            )
        )

        # Extract the street, zip_code and city from the address box
        address = driver.find_element(
            By.XPATH, "//section[@class='card-body notranslate']"
        ).text

        try:
            street = re.search(r".*", address)[0]
        except TypeError:
            street = "not found"

        try:
            zip_code = re.search(r"[0-9]{5}", address)[0]
        except TypeError:
            zip_code = "not found"

        try:
            city = re.search(r"[\w]+$", address)[0]
        except TypeError:
            city = "not found"


        # add the new variables to dictionaries in restaurant_list

        street_list.append(street)
        zip_code_list.append(zip_code)
        city_list.append(city)
        time.sleep(np.random.randint(1, 3))

    ##########
    ### EXPANDING A DATA FRAME AND EXPORT
    ##########
    df["street"] = street_list
    df["zip_code"] = zip_code_list
    df["city"] = city

    # Consideration: Export the partial df to disc after a certain number of iterations
    # in order to preserve data in case I get banned halfway through

    return df


def main():
    # Unpickle zip code list
    with open("../data/zip.pkl", "rb") as f:
        zip_codes = pickle.load(f)
    # get the restaurant list
    restaurant_list, driver = get_restaurants(zip_codes, start=189)
    # get addresses
    restaurant_df = get_addresses(restaurant_list, driver, start=2300)
    restaurant_df.to_csv("../data/lieferando_restaurants.csv")


if __name__ == "__main__":
    main()
