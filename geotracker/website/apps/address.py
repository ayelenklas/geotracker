from typing import Container
from pkg_resources import compatible_platforms
import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
#import matplotlib.pyplot as plt

''' SEARCH '''

cuisine_options = ['African', 'American', 'Asian', 'Vegetarian or Vegan', 'Steak',
                  'South American', 'Snacks', 'Seafood', 'Russian', 'Poke', 'Middle Eastern',
                  'Mexican', 'Mediterranean', 'Italian', 'International', 'Indian', 'Healthy',
                  'Greek', 'Fastfood', 'European', 'Cafes', 'Breakfast/Dessert', 'Bars']

def app():
    st.title('Restaurants Analysis')
    ''' filters '''
    col1, col2 = st.columns(2)
    with col1:
        address = st.text_input('Insert the adress to search by:')
        range = st.slider('Choose the lenght of the radius:',
                          help='Shown in kilometers.',
                          min_value= 0.5,
                          max_value=5.0,
                          step= 0.1)
    with col2:
        score = st.slider('Choose the minimum reviews score:',
                          max_value=10,
                          step=1)
        cuisine = st.multiselect('Choose the cuisine type:', options= cuisine_options)

    ''' graphs '''
    lieferando, wolt, allrestos = st.columns(3)

    if st.button('Search'):

        with lieferando:
            st.write()
            #ayelen charts



    ''' mapa '''
    st.header('Take a look at all restaurants:')
    colchoose, colmap = st.columns([1,5])

    with colchoose:
        alw = st.radio('Choose a delivery company:', options=['All restaurants','Lieferando','Wolt'])
    with colmap:
        if alw == 'All restaurants':
            a = folium.Map(
                location=[52.520008, 13.404954],
                zoom_start=10,
                prefer_canvas=True,)
            with open("geotracker/website/data/geojson.json") as f:
                file = json.load(f)

            folium.GeoJson(file, name="geojson.json").add_to(a)

            samples = pd.read_csv("geotracker/website/data/r4map.csv")
            a.add_child(FastMarkerCluster(samples[['lat', 'lon']].values.tolist()))

            folium_static(a)
        if alw == 'Lieferando':
            l = folium.Map(
                location=[52.520008, 13.404954],
                zoom_start=10,
                prefer_canvas=True,
            )
            with open("geotracker/website/data/geojson.json") as f:
                file = json.load(f)

            folium.GeoJson(file, name="geojson.json").add_to(l)

            samples = pd.read_csv("geotracker/website/data/r4map_lieferando.csv")
            l.add_child(
                FastMarkerCluster(samples[['lat', 'lon']].values.tolist()))

            folium_static(l)
        if alw == 'Wolt':
            w = folium.Map(
                location=[52.520008, 13.404954],
                zoom_start=10,
                prefer_canvas=True,
            )
            with open("geotracker/website/data/geojson.json") as f:
                file = json.load(f)

            folium.GeoJson(file, name="geojson.json").add_to(w)

            samples = pd.read_csv("geotracker/website/data/r4map_wolt.csv")
            w.add_child(
                FastMarkerCluster(samples[['lat', 'lon']].values.tolist()))

            folium_static(w)
