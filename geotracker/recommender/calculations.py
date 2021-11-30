import pandas as pd
from geotracker.recommender.functions import (
    get_circle_centers_radius,
    restaurants_in_circle,
    restaurants_meeting_criteria,
)


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
    restaurants_df = pd.read_csv("geotracker/data/wolt_clean_data.csv")

    spacings = [50, 30, 20, 15, 10, 5]

    restaurant_list = []
    circle_list = []
    for spacing in spacings:
        center_coords, mradius, degradius = get_circle_centers_radius(spacing)
        for index, center_coord in enumerate(center_coords):
            center_lat = center_coord[0]
            center_lon = center_coord[1]
            restaurants_in_circle_df = restaurants_in_circle(
                restaurants_df, center_lat, center_lon, degradius
            )

            # Add circle index to restaurants_in_circle and save to list of dfs
            if len(restaurants_in_circle_df) != 0:
                restaurants_in_circle_df.insert(0, "circle_id", index)
                restaurants_in_circle_df.insert(1, "spacing", spacing)
                restaurant_list.append(restaurants_in_circle_df)

            matched_restaurants = restaurants_meeting_criteria(
                restaurants_in_circle_df, good_review_threshold=5
            )

            circle_dict = dict(
                circle_id=index,
                spacing=spacing,
                center_lat=center_lat,
                center_lon=center_lon,
                mradius=mradius,
                degradius=degradius,
                circle_weight=len(matched_restaurants),
            )
            circle_list.append(circle_dict)

    # Write DF of circles to disk
    circle_df = pd.DataFrame(circle_list)
    circle_df.to_csv("geotracker/data/circle_weights.csv", index=False)

    # write DF of restaurants in circles to disk
    restaurants_in_circles = pd.concat(restaurant_list)
    restaurants_in_circles.to_csv(
        "geotracker/data/restaurants_in_circles.csv", index=False
    )

    return None


if __name__ == "__main__":
    main()
