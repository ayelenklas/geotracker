import numpy as np
import pandas as pd
<<<<<<< HEAD
from geopy import distance

def get_circlegrid_list(topleft, bottomright, kmradius, overlap_factor) -> list:
=======

def get_circlegrid_list(topleft, bottomright, kmradius, overlap) -> list:
>>>>>>> master
    """
    Takes as an input the topleft and bottomright coordinates of a square, as
    well as a user defined radius for the circle that we wish to draw in the square
    and then divides the square into evenly spaced circles of radius kmradius
    which overlap to the degree specified in overlap (1.2 = 20% overlap, roughly)
    """
<<<<<<< HEAD
    spacing_lat = ((1/110.574) * kmradius*2) * overlap_factor
    spacing_lon = (abs((1/(111.320 * np.cos(topleft[0]))) * kmradius*2)) * overlap_factor

    lats = np.arange(bottomright[0], topleft[0], spacing_lat)
    lons = np.arange(topleft[1], bottomright[1], spacing_lon)

    points = []
    for lat in lats:
        for lon in lons:
            points.append((lat, lon))
=======

    spacing_lat = abs((1/110_574) * kmradius)
    spacing_lon = abs((1/(111_320 * np.cos(topleft[0]))) * kmradius)

    lats = np.arange(bottomright[0], topleft[0], spacing_lat)
    lons = np.arange(topleft[1], bottomright[1], spacing_lon)



    points = []
    for lat in lats:
        for lon in lons:
            points.append((lat, lon))

    side_lenght = bottomright[0] - topleft[0]
    degradius = (side_lenght / (2 * (spacing_lat - 1))) * overlap
    #mradius = abs(1000 * (degradius * (40075 * np.cos(topleft[1]) / 360)))

    return points, degradius
>>>>>>> master

    return points


# def restaurant_distance(observation, center_lat, center_lon) -> bool:
#     """
#     Takes as an input one
#     """

#     obs_lat = observation["latitude"]
#     obs_lon = observation["longitude"]

#     return (obs_lat - center_lat) ** 2 + (obs_lon - center_lon) ** 2 <= degradius ** 2


def restaurants_in_circle(df, center_coord, kmradius) -> pd.DataFrame:
    """
    Takes as an input a dataframe and returns a dataframe of observations which
    fall into the circle
    """
    # disabling warnings
    pd.options.mode.chained_assignment = None

    # Dropping restaurants without Lats and Lons because they cannot be measured
    df_clean = df.dropna(subset=["latitude", "longitude"])
    # Create empty rows
    df_clean["distance_to_circle_center"] = np.nan

    for index, row in df_clean.iterrows():
        dist = distance.distance(center_coord, (row["latitude"], row["longitude"])).km
        df_clean.loc[index, "distance_to_circle_center"] = dist

    matched_restaurants = df_clean[df_clean["distance_to_circle_center"] <= kmradius]

    return matched_restaurants


def restaurants_meeting_criteria(
    restaurants_df, good_review_threshold=5, avoid_competitor=[], include_cuisines=[]
):
    """
    Returns a data frame with the restaurants that meet criteria specified
    in the arguments.

    TODO: implement functions that reduce size of restaurants based on other features
    """

    # Filtering out only good restaurants
    good_restaurants = restaurants_df[
        restaurants_df.avg_review_score > good_review_threshold]

    # avoid restaurants already serviced by one of the two competitors
    # If you want to specify both competitors, you cannot supply a review
    # threshold, as it's not available on the here data
    if avoid_competitor:
        pass

    if include_cuisines:
        pass

    return good_restaurants
