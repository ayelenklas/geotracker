from numpy.random.mtrand import randint
import requests
import pickle
import time
import pandas as pd

def main():
    with open("../data/zip.pkl", "rb") as f:
        zip_codes = pickle.load(f)

    headers = {
    'authority': 'cw-api.takeaway.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'cw-true-ip': '78.54.23.171',
    'accept-language': 'de',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'x-requested-with': 'XMLHttpRequest',
    'x-session-id': '3fc8b9cd-a01d-49a6-acec-da1efbffd668',
    'x-country-code': 'de',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://www.lieferando.de',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'Cookie': '__cf_bm=ZJ4ig0EH9aWvHX9ljNvsdiS68p4HS3GXv7qZViANi04-1638119453-0-AYi7B/IzoaMAuId89+hXvD4zSNTUzcxbNFrhHe2yFGz9f9PgGSBdKn2ya84vJnTd6kU7Xx3fJbZaSJZhNoXWgN8Jt7RQY/v1K02uPTAd9Iti'
    }


    base_url = "https://cw-api.takeaway.com/api/v28/restaurants"

    # Main Program Loop

    for index, zip_code in enumerate(zip_codes):
        print(f"scraping ZIP code:{zip_code}---------- {index+1}/{len(zip_codes)}")
        params = {"postalCode": zip_code, "limit": 0}
        response = requests.get(base_url, headers=headers, params=params).json()

        restaurant_list = []
        for restaurant in response["restaurants"]:
            restaurant_dict = dict(
                restaurant_name = response["restaurants"][restaurant]["brand"]["name"],
                platform = "lieferando",
                reviews = response["restaurants"][restaurant]["rating"]["votes"],
                avg_review_score = response["restaurants"][restaurant]["rating"]["score"],
                street = response["restaurants"][restaurant]["location"]["streetAddress"],
                zip_code = zip_code,
                city = response["restaurants"][restaurant]["location"]["city"],
                latitude = response["restaurants"][restaurant]["location"]["lat"],
                longitude = response["restaurants"][restaurant]["location"]["lng"],
                type_of_cuisine = response["restaurants"][restaurant]["cuisineTypes"],
                avg_delivery_time = response["restaurants"][restaurant]["shippingInfo"]["delivery"]["duration"],
                pricyness = response["restaurants"][restaurant]["priceRange"],
                delivery_fee = response["restaurants"][restaurant]["shippingInfo"]["delivery"]["deliveryFeeDefault"],
                minimum_order_value = response["restaurants"][restaurant]["shippingInfo"]["delivery"]["minOrderValue"]
            )
            restaurant_list.append(restaurant_dict)

        time.sleep(randint(3, 6))

    output_df = pd.DataFrame(restaurant_list)
    output_df.to_csv("../data/lieferando_restaurants_from_api.csv", index=False)


    return None


if __name__ == "__main__":
    main()
