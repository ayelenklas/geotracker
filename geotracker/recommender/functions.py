import numpy as np
import pandas as pd

def get_circlegrid_list(topleft, bottomright, kmradius, overlap) -> list:
    """
    Takes as an input the topleft and bottomright coordinates of a square, as
    well as a user defined radius for the circle that we wish to draw in the square
    and then divides the square into evenly spaced circles of radius kmradius
    which overlap to the degree specified in overlap (1.2 = 20% overlap, roughly)
    """

    spacing_lat = abs((1/110_574) * kmradius)
    spacing_lon = abs((1/(111_320 * np.cos(topleft[0]))) * kmradius)

    lats = np.arange(bottomright[0], topleft[0], spacing_lat)
    lons = np.arange(topleft[1], bottomright[1], spacing_lon)

    import ipdb; ipdb.set_trace()

    points = []
    for lat in lats:
        for lon in lons:
            points.append((lat, lon))

    side_lenght = bottomright[0] - topleft[0]
    degradius = (side_lenght / (2 * (spacing_lat - 1))) * overlap
    #mradius = abs(1000 * (degradius * (40075 * np.cos(topleft[1]) / 360)))

    return points, degradius


def is_restaurant_in_circle(observation, center_lat, center_lon, degradius) -> bool:
    """
    Takes as an input one row of a dataframe and returns boolean indicating
    whether a restaurant falls into a circle specified center coordinates and the
    circle's radius in degrees.
    """

    obs_lat = observation["latitude"]
    obs_lon = observation["longitude"]

    return (obs_lat - center_lat) ** 2 + (obs_lon - center_lon) ** 2 <= degradius ** 2


def restaurants_in_circle(df, center_lat, center_lon, degradius) -> pd.DataFrame:
    """
    Takes as an input a dataframe and returns a dataframe of observations which
    fall into the circle
    """

    df_in_circle = df[
        (df["latitude"] - center_lat) ** 2 + (df["longitude"] - center_lon) ** 2
        <= degradius ** 2
    ]

    return df_in_circle


def restaurants_meeting_criteria(
    restaurants_df, good_review_threshold=5, avoid_lieferando=False, avoid_wolt=False
):
    """
    Returns a data frame with the restaurants that meet criteria specified
    in the arguments.

    TODO: implement functions that reduce size of restaurants based on other features
    """

    # Filtering out only good restaurants
    good_restaurants = restaurants_df[
        restaurants_df.avg_review_score > good_review_threshold
    ]

    # restaurants not already on Lieferando
    if avoid_lieferando:
        pass
    # restaurants not already on Wolt
    if avoid_wolt:
        pass

    return good_restaurants
