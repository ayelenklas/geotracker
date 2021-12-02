import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit.legacy_caching.caching import cache
from streamlit_folium import folium_static

''' RECOMMENDATIONS '''

def app():
    st.title('Suggest the best location to open operations')
    '''Filter part'''

    st.write("""
             Enter the size of the area you wish to service on your
             delivery platform as a kilometer radius. The app will then
             recommend you an ideal location based on the densitiy of
             restaurants, suggesting you the area where you can service the most
             customers.

             Below, you find a list of all restaurants in the suggested area so
             you can start building your business today.



             """)


    st.markdown("### Select parameters")

    kmradius = st.slider('Choose the radius of your operations area in kilometers:',
                          help='The ',
                          min_value=1,
                          max_value=5,
                          step=1)

    cuisines = st.multiselect("Choose which cuisines you want to include",
                              options= ['All', 'Seafood', 'Asian', 'International', 'European', 'Greek',
                                        'Breakfast/dessert', 'Mediterranean', 'Fastfood', 'Italian',
                                        'Middle eastern', 'Steak', 'American', 'Bars', 'Mexican',
                                        'Healthy', 'Snacks', 'Russian', 'Vegetarian or vegan',
                                        'South american', 'African', 'Indian'],
                              default="All")


#### Functions to read and filter data

    def read_circle_data():
        """Wrapper function to read the circle data"""
        return pd.read_csv("geotracker/data/precalculated_recommendations/precalc_circle_weights.csv")

    @st.cache
    def filter_circle_data(kmradius):
        """
        Reads circle data and filters it down to the correct radius
        """
        df = read_circle_data()

        # filter down to criteria
        df = df[df["kmradius"] == kmradius]


        return df


    def read_circle_restaurants():
        """Wrapper function to read the circle data"""
        return pd.read_csv("geotracker/data/precalculated_recommendations/precalc_matched_restaurants_by_circle.csv")

    @st.cache
    def filter_circle_restaurants(kmradius, cuisines):
        """
        Reads restaurant data and filters it down to the correct kmradius
        and
        """
        df = read_circle_restaurants()

        # Filter down to restaurants for specific radius and for selected cuisines
        df = df[df["kmradius"] == kmradius]
        df.drop_duplicates(inplace=True)
        if "All" not in cuisines:
            df = df[df["type_of_cuisine"].isin(cuisines)]


        return df

    @st.cache
    def determine_best_circle(circle_df, restaurant_df):
        """
        Takes the two dfs and returns the circle df and the restaurant df for
        the circle with the highest restaurant count
        """
        # group restaurant_df by circle_id and count the rows
        circle_ranks = restaurant_df.groupby("circle_id", as_index=False).agg(
            number_of_restaurants = ("circle_id", pd.Series.count))

        # Extract the best circle and the number of restaurants from it
        selected_circle = circle_ranks[circle_ranks["number_of_restaurants"] == circle_ranks.number_of_restaurants.max()].head(1)

        # Filter the restaurant df to only include restaurants from best circle
        restaurant_df = restaurant_df[restaurant_df["circle_id"] == selected_circle.circle_id.values[0]]

        best_circle = circle_df[circle_df["circle_id"] == selected_circle.circle_id.values[0]]

        return best_circle, restaurant_df




    @st.cache
    def clean_restaurant_df_for_output(restaurant_df):
        """
        Cleans the restaurant df given for output so that it can be displayed in a
        table that looks nice.
        """
        # Cleaning output for display
        df = restaurant_df[["restaurant_name", "address","type_of_cuisine"]]
        df["address"] = df["address"].str.replace("\.0", "")
        df = df.assign(hack='').set_index('hack')
        df.columns = ["Name", "Address", "Type of Cuisine"]

        return df



    @st.cache
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    if st.button('Show me the ideal location'):

        try:

            circle_df = filter_circle_data(kmradius)

            restaurant_df = filter_circle_restaurants(kmradius, cuisines)

            best_circle, restaurant_df = determine_best_circle(circle_df, restaurant_df)

            display_df = clean_restaurant_df_for_output(restaurant_df)

            center_coord = (best_circle["center_lat"].values[0], best_circle["center_lon"].values[0])

            '''Map part'''


            st.markdown(f"""
                #### We suggest you open your operations in the highlighted area.


                This way, your platform will be able to deliver from **{len(display_df)}**
                restaurants.""")

            m = folium.Map(location=[52.513001, 13.393947], zoom_start=12)
            folium.Circle(
                location=center_coord,
                radius=kmradius * 1000,
                popup=f"Ideal location: {len(display_df)} restaurants in range",
                color="#e95952",
                fill=True,
                fill_color="#e95952",
            ).add_to(m)

            # folium.Marker(
            # location=center_coord,
            # popup=f"Geographical center: {center_coord}",
            # tooltip="Center of recommended delivery area"
            # ).add_to(m)

            # Render map on Streamlit
            folium_static(m)

            '''Expand part'''
            with st.expander('See info on the restaurants in the suggested area'):
                st.write(display_df) #list of restaurants and the infos selected in the filter
                csv = convert_df(display_df)

                st.download_button(
                            label="Download data as CSV",
                            data=csv,
                            file_name='restaurants.csv',
                            mime='text/csv',
                        )

        except:
            st.markdown("## Your search didn't return any restaurants. Try again with different parameters.")
