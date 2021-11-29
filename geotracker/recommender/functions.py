import numpy as np
import pandas as pd
from geotracker.utils import Utils


def get_circle_centers_radius(
    spacing,
    top_left=(52.635010, 13.198130),
    bottom_right=(52.39405827510934, 13.596147274545292),
) -> tuple:
    """
    Wrapper around the utils function get_circlegrid_list.
    Has Berlins top_left and bottom_right coordinates already coded in

    Returns a list of center coordinates and one radius in meters and one in
    degrees in order to allow us to check for whether coordinates are in the
    circle.
    Meters = for showing to users, because easy to interpret
    Degrees = necessary for calculations
    """
    # Top left and bottom right of a square covering the entiretty of Berlin

    #  get a number of cirlces with the specified spacing.
    center_coords, mradius, degradius = Utils().get_circlegrid_list(
        top_left, bottom_right, spacing, 1.2
    )

    return center_coords, mradius, degradius


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
    if len(restaurants_df) == 0:
        return 0

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

    return len(good_restaurants)
