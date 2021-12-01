# from typing import Container
# from pkg_resources import compatible_platforms
import streamlit as st
import pandas as pd
import json
# import numpy as np
import math
import requests
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
import matplotlib.pyplot as plt

''' SEARCH '''

# st.set_option('deprecation.showPyplotGlobalUse', False)

cuisine_options = ['African', 'American', 'Asian', 'Vegetarian or Vegan', 'Steak',
                  'South American', 'Snacks', 'Seafood', 'Russian', 'Poke', 'Middle Eastern',
                  'Mexican', 'Mediterranean', 'Italian', 'International', 'Indian', 'Healthy',
                  'Greek', 'Fastfood', 'European', 'Cafes', 'Breakfast/Dessert', 'Bars']

def app():
    # st.write('sredzkistrasse 43, 10435, Berlin')
    st.title('Restaurants Analysis')


    ''' filters '''
    col1, col2 = st.columns(2)
    with col1:
        adr = st.text_input('Insert the adress to search by:')
    with col2:
        rkm = st.slider('Choose the lenght of the radius:',
                          help='Shown in kilometers.',
                          min_value=0.0,
                          max_value=5.0,
                          step=0.1)


    ''' filters input '''
    if st.button('Search'):
        all_data = pd.read_csv("geotracker/data/all_data.csv").iloc[:, 1:]

        # range in km
        range = rkm
        address_searched = adr

        # from address to latlon converter
        def geocode(address):
            params = {"q": address, "format": "json"}
            places = requests.get(f"https://nominatim.openstreetmap.org/search",
                                params=params).json()
            return [places[0]['lat'], places[0]['lon']]

        # lat lon from address searched
        lat = float(geocode(address_searched)[0])
        lon = float(geocode(address_searched)[1])

        # radius limits - converting kms into coordinates and calculating boundaries
        distance_lat_degrees = (1/110.574) * range
        distance_lon_degrees = abs((1/(111.320 * math.cos(lat))) * range)

        min_lat = lat - distance_lat_degrees/2
        max_lat = lat + distance_lat_degrees/2
        min_lon = lon - distance_lon_degrees/2
        max_lon = lon + distance_lon_degrees/2

        search_limits = (all_data.latitude >= min_lat) & (all_data.latitude <= max_lat) & (all_data.longitude >= min_lon) & (all_data.longitude <= max_lon)

        '''' Breakdown by Type of Cuisine '''

        cmap = "tab20c"
        hex_colors = ["#3182bd","#fd8d3c", "#a1d99b","#dadaeb", "#d9d9d9"]
        autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else ''
        fontsize = 10



        ''' graphs '''
        lieferando, wolt, allrestos = st.columns(3)

        with lieferando:

            '''# number of restaurants'''
            #st.image('https://www.lieferkassen.de/wp-content/uploads/2018/08/logo-thuisbezorgd.jpg', width=100)
            st.subheader('Lieferando')
            num_restos_lieferando = all_data[
                (all_data.database == "lieferando")
                & search_limits].shape[0]
            st.subheader(num_restos_lieferando)

            '''# types of cuisine'''
        # select from df
            cuisine_lieferando = all_data[(all_data.database == "lieferando")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)

            # top n
            # try:
            n = 10
            cuisine_lieferando_top10 = cuisine_lieferando[:n].copy()

            # others
            others_lieferando = pd.DataFrame(
                data={'type_of_cuisine': ['others'],
                    'value': [cuisine_lieferando['restaurant_name'][n:].sum()]})

            # combining data
            
            cuisine_bkdwn_lieferando = pd.concat([cuisine_lieferando_top10,
                                                others_lieferando])["restaurant_name"]
            # except ValueError:
    

            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = cuisine_bkdwn_lieferando.index
            sizes = cuisine_bkdwn_lieferando
            cuisine_bkdwn_lieferando.plot(kind='pie',
                                    autopct=autopct,
                                    cmap=cmap,
                                    fontsize=fontsize)
            plt.title("Wolt - Breakdown by type of cuisine", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")
            try:
                st.pyplot()
            except ValueError:
                st.write(f"No restaurants affiliated \nwith Lieferando in the area")

        with wolt:

            '''# number of restaurants'''
            #st.image('https://cdn.freelogovectors.net/wp-content/uploads/2020/11/wolt_logo.png',width=80)
            st.subheader('Wolt')
            num_restos_wolt = all_data[(all_data.database == "wolt") & search_limits & (
                all_data.street != "This is a virtual venue")].shape[0]
            st.subheader(num_restos_wolt)


            '''# types of cuisine'''
            # select from df
            cuisine_wolt = all_data[(all_data.database == "wolt")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)

            # top n
            # try:
            n = 10
            cuisine_wolt_top10 = cuisine_wolt[:n].copy()

            # others
            others_wolt = pd.DataFrame(
                data={'type_of_cuisine': ['others'],
                    'value': [cuisine_wolt['restaurant_name'][n:].sum()]})

            # combining data            
            cuisine_bkdwn_wolt = pd.concat([cuisine_wolt_top10,
                                                others_wolt])["restaurant_name"]    

            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = cuisine_bkdwn_wolt.index
            sizes = cuisine_bkdwn_wolt
            cuisine_bkdwn_wolt.plot(kind='pie',
                                    autopct=autopct,
                                    cmap=cmap,
                                    fontsize=fontsize)

            plt.title("Wolt - Breakdown by type of cuisine", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")

            try:
                st.pyplot()
            except ValueError:
                st.write(f"No restaurants affiliated \nwith Wolt in the area")


        with allrestos:

            # number of restaurants
            st.subheader('All')
            num_restos_maps = all_data[(all_data.database == "here_maps")
                           & search_limits].shape[0]
            # fixing num of restos for maps: there can't be more restos in a delivery platform than in the maps
            num_restos_maps = max(num_restos_wolt, num_restos_lieferando, num_restos_maps)
            st.subheader(num_restos_maps)

            # types of cuisine
            # select from df
            cuisine_restos_maps = all_data[(all_data.database == "here_maps")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)

            # top n
            # try:
            n = 10
            cuisine_restos_maps_top10 = cuisine_wolt[:n].copy()

            # others
            others_restos_maps = pd.DataFrame(
                data={'type_of_cuisine': ['others'],
                    'value': [cuisine_restos_maps['restaurant_name'][n:].sum()]})

            # combining data            
            cuisine_bkdwn_restos_maps = pd.concat([cuisine_restos_maps_top10,
                                                others_restos_maps])["restaurant_name"]    

            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = cuisine_bkdwn_restos_maps.index
            sizes = cuisine_bkdwn_restos_maps
            cuisine_bkdwn_restos_maps.plot(kind='pie',
                                    autopct=autopct,
                                    cmap=cmap,
                                    fontsize=fontsize)

            plt.title("Wolt - Breakdown by type of cuisine", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")

            try:
                st.pyplot()
            except ValueError:
                st.write(f"No data available on \nrestaurants in the area")



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
