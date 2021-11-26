import pandas as pd
from geotracker.recommender.functions import get_circle_centers_radius, restaurants_in_circle, calculate_circle_weights

def main():
    """
    Loads the combined dataframe of all restaurants from disk and then
    creates four different sets of overlapping circles covering the entirety
    of Berlin. For each set of circles, then all restaurants within each circle
    are filtered out. Each circle is assigned a weight which is the number of
    good restaurants in the circle.
    Then, a CSV file of all circles and weights is for each spacing iteration
    is stored on disk.
    """
    restaurnts_df = pd.read_csv("../data/restaurants.csv")

    spacings = [20, 14, 10, 5]

    dict_list = []
    for spacing in spacings:
        center_coords, mradius, degradius = get_circle_centers_radius(spacing)
        for center_coord in center_coords:
            center_lat = center_coord[0]
            center_lon = center_coord[1]
            restaurants_in_circle_df = restaurants_in_circle(
                restaurnts_df, center_lat, center_lon, degradius
            )
            circle_weight = calculate_circle_weights(
                restaurants_in_circle_df,
                good_review_threshold=2.5)

            circle_dict = dict(
                center_lat = center_coord,
                center_lon = center_lon,
                mradius = mradius,
                degradius = degradius,
                spacing = spacing,
                circle_weight = circle_weight
            )
            dict_list.append(circle_dict)

    circle_df = pd.DataFrame(dict_list)
    circle_df.to_csv("../data/circle_weights.csv")

    return None



if __name__ == "__main__":
    main()
