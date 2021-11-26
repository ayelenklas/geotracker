import numpy as np
import pandas as pd
from geotracker.utils import Utils

def square_around_coordinate(lat, lon, size) -> tuple:
    """
    Input: Latitude and Longitude for a point on Earth. Center of the square
    to be created.
    Size: height/width of the square in kilometers, use the radius from
    get_circle_grid as input

    Returns:  a tuple with two latitudes and two longitudes
    that define the upper and lower bounds of a square formed around the
    center point.

    Format of output is:
    (upper_lat, lower_lat, left_lon, right_lon).
    """

    # converting size of the square to latitude degrees for differencing
    # halved to accunt for the fact that we difference in both directions
    lat_difference = size * (1/110_574) / 2
    lon_difference = size * (1 / (111_320 * np.cos(lat))) / 2

    upper_lat = lat + lat_difference
    lower_lat = lat - lat_difference

    left_lon = lon - lon_difference
    right_lon = lon + lon_difference

    return (upper_lat, lower_lat, left_lon, right_lon)


def get_square_borders(spacing, top_left = (52.635010, 13.198130), bottom_right = (52.39405827510934, 13.596147274545292))->tuple:
    """
    Creates a list of upper and lower longitudes which can be used as centers
    to calculate the upper and lower bounds for squares which can then be used
    to capture restaurants.
    The bigger spacing is, the more restaurants will be returned.
    Spacing = Number of chunks for latitude and longitude so number of chunks is
    spacing ** 2

    For each input coord, four values will be returned, as well as the
    center coordinates and the radius in meter  for each square which are useful
    for mapping later
    """
# Top left and bottom right of a square covering the entiretty of Berlin

#  get a number of cirlces with the specified spacing.
    center_coords, mradius = Utils().get_circlegrid_list(top_left, bottom_right, spacing, 1.2)

    bounds = []
    for coord in center_coords:
        bounds.append(square_around_coordinate(coord[0], coord[1], mradius))

    return bounds, center_coords, mradius



def return_restaurants_in_square(df, bounds) -> list:
    """
    Returns a list of dataframes, where each dataframe corresponds
    to the restaurants that fall within each tuple in bounds
    """
    pass


def calculate_restaurant_weights(restaurant_df):
    """
    Returns a weight for each restaurant DF. Used for iteration over the
    restaurnt dfs retruned from the return restaurant in squares
    """
    pass
