import pandas as pd
from geotracker.recommender.functions import (
    get_circlegrid_list,
    restaurants_in_circle,
    restaurants_meeting_criteria,
)


def create_circles_csv(kmradius, overlap_percent,
                      top_left=(52.635010, 13.198130),
                      bottom_right=(52.39405827510934, 13.596147274545292),
                      **weighting_criteria):
    """
    Loads the combined dataframe of all restaurants from disk and then
    calculates the weighting of circles drawn on the map of Berlin. Circle
    size and location is determined by the radius in km and the amount of overlap
    desired.
    Circle weights are essentially counts of restaurants in a circle that match
    the weighting criteria. check recommender.functions.restaurants_meeting_criteria
    for all available criteria.

    Params:
    kmradius: size of the circle area desired in km
    overlap_percent: number of overlap in percent (20 = 20% overlap in the circles)
    top_left: top left coordinate from which to create the circlegrid
    bottom_right: bottom right coordinate from which to create the circlegrid

    Writes two DFs as CSV:
    circle_weights.csv: properties of all the circles and their weights
    Weights: number of restaurants depending on weighting criteria
    passed to the function.

    matched_restaurants: number of restaurants that were matched with the
    specific weighting criteria


    Returns: None
    """
    restaurants_df = pd.read_csv("geotracker/data/deliveries_data.csv")

    # Convert overlap in percent from UI tu usable overlap for functions
    overlap = overlap_percent/100 + 1

    # Instatiate empty lists for export later
    circle_list = []
    restaurant_list = []
    # get center coords for circles and their radius in degrees

    center_coords, degradius = get_circlegrid_list(top_left, bottom_right,
                                                   kmradius, overlap)

    # MAIN LOOP: Loop over each center for each circle
    for index, center_coord in enumerate(center_coords):
        # Get all restaurants in the circle
        restaurants_in_circle_df = restaurants_in_circle(
            restaurants_df, center_coord[0], center_coord[1], degradius
        )

        # Add circle index to restaurants_in_circle and save to list of dfs
        if len(restaurants_in_circle_df) != 0:
            restaurants_in_circle_df.insert(0, "circle_id", index)
            restaurants_in_circle_df.insert(1, "kmradius", kmradius)

        # Match only restaurants taht meet pre-defined criteria
        matched_restaurants = restaurants_meeting_criteria(
            restaurants_in_circle_df, **weighting_criteria
        )
        if len(matched_restaurants) != 0:
            matched_restaurants["circle_id"] = index
            restaurant_list.append(matched_restaurants)

        circle_dict = dict(
            circle_id=index,
            kmradius=kmradius,
            center_lat=center_coord[0],
            center_lon=center_coord[1],
            degradius=degradius,
            circle_weight=len(matched_restaurants),
        )
        circle_list.append(circle_dict)

    # Write DF of circles to disk
    circle_df = pd.DataFrame(circle_list)
    circle_df.to_csv("geotracker/data/circle_weights.csv", index=False)

    # write DF of restaurants that were used in calculating the weight to disk
    matched_restaurants_df = pd.concat(restaurant_list)
    matched_restaurants_df.to_csv(
        "geotracker/data/matched_restaurants_by_circle.csv", index=False
    )

    return None

## name == main functions for testing

if __name__ == "__main__":
    create_circles_csv(kmradius=2, overlap_percent=20,
                      good_review_threshold=7,
                      avoid_lieferando=False, avoid_wolt=False)
