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

    col1, col2 = st.columns(2)
    with col1:
        kmradius = st.slider('Choose the radius of your operations area in kilometers:',
                          help='The ',
                          min_value=1,
                          max_value=5,
                          step=1)
    with col2:
        overlap_percent = st.slider(
            'Choose the overlap amount in percentage:',
            help='The more they overlap, more accurate the prediction will be.',
            min_value=0,
            max_value=50,
            step=10 )


#### Functions to read and filter data

    def read_circle_data():
        return pd.read_csv("geotracker/data/precalculated_recommendations/precalc_circle_weights.csv")

    @st.cache
    def filter_circle_data(kmradius, overlap_percent):
        df = read_circle_data()

        # filter down to criteria
        df = df[df["kmradius"] == kmradius]
        df = df[df["overlap"] == overlap_percent]

        # Select the circle with the highest weight
        df = df[df["circle_weight"] == df["circle_weight"].max()].head(1)
        circle_id = df["circle_id"].values

        return df, int(circle_id)




    def read_circle_restaurants():
        return pd.read_csv("geotracker/data/precalculated_recommendations/precalc_matched_restaurants_by_circle.csv")

    @st.cache
    def filter_circle_restaurants(circle_id):
        df = read_circle_restaurants()

        df = df[df["circle_id"] == circle_id]
        df = df[["restaurant_name", "address","type_of_cuisine"]]
        df["address"] = df["address"].str.replace("\.0", "")
        df = df.assign(hack='').set_index('hack')
        df.columns = ["Name", "Address", "Type of Cuisine"]

        return df

    df, circle_id = filter_circle_data(kmradius, overlap_percent)
    center_coord = (df["center_lat"].values[0], df["center_lon"].values[0])

    '''Map part'''

    st.markdown(f"""
                #### We suggest you open your operations at the blue pin below.


                This way, your platform will be able to deliver from **{int(df['circle_weight'])}**
                restaurants.
                """)
#if st.button('Recommend'):

    m = folium.Map(location=[52.513001, 13.393947], zoom_start=12)
    folium.Circle(
        location=center_coord,
        radius=kmradius * 1000,
        popup=f"Ideal location: {int(df['circle_weight'])} restaurants in range",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)

    folium.Marker(
    location=center_coord,
    popup=f"Geographical center: {center_coord}",
    tooltip="Center of recommended delivery area"
    ).add_to(m)

    # Render map on Streamlit
    folium_static(m)

    '''Expand part'''
    with st.expander('See info on the restaurants in the suggested area'):
        circle_restaurants = filter_circle_restaurants(circle_id)
        st.write(circle_restaurants) #list of restaurants and the infos selected in the filter
