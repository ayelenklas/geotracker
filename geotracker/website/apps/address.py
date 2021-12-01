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

cuisine_options = ['African', 'American', 'Asian', 'Vegetarian or Vegan', 'Steak',
                  'South American', 'Snacks', 'Seafood', 'Russian', 'Poke', 'Middle Eastern',
                  'Mexican', 'Mediterranean', 'Italian', 'International', 'Indian', 'Healthy',
                  'Greek', 'Fastfood', 'European', 'Cafes', 'Breakfast/Dessert', 'Bars']

def app():
    st.write('Test')
    st.write('sredzkistrasse 43, 10435, Berlin')
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

        '''' Infos needed for the columns '''

        cmap = "tab20c"
        hex_colors = ["#3182bd","#fd8d3c", "#a1d99b","#dadaeb", "#d9d9d9"]
        autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else ''
        fontsize = 10

        wolt_num_restos = pd.read_csv('geotracker/data/wolt_restaurants_from_api_2.csv')

        good_restos_rankingbase = 7.5
        regular_restos_rankingbase = 5

        st.set_option('deprecation.showPyplotGlobalUse', False)


        ''' graphs '''

        ''' number of restaurants '''
        num_lief, num_wolt, num_all = st.columns(3)
        with num_lief:
            st.header('Lieferando')
            num_restos_lieferando = all_data[
                (all_data.database == "lieferando")
                & search_limits].shape[0]
            st.metric('Total of restaurants', value=num_restos_lieferando)
        with num_wolt:
            st.header('Wolt')
            num_restos_wolt = wolt_num_restos[
                search_limits & (wolt_num_restos.street != 'This is a virtual venue')].shape[0]
            st.metric('Total of restaurants', value=num_restos_wolt)
        with num_all:
            st.header('All')
            num_restos_maps = all_data[(all_data.database == "here_maps")
                                       & search_limits].shape[0]
            # fixing num of restos for maps: there can't be more restos in a delivery platform than in the maps
            num_restos_maps = max(num_restos_wolt, num_restos_lieferando,
                                  num_restos_maps)
            st.metric('Total of restaurants', value=num_restos_maps)



        ''' Breakdown by type of cuisine '''
        st.subheader('Breakdown by type of cuisine:')
        cui_lief, cui_wolt, cui_all = st.columns(3)

        with cui_lief:
            st.subheader('Lieferando')
            # select from df
            cuisine_lief = all_data[(all_data.database == "lieferando")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)
            # top n
            n = 7
            cuisine_lief_top10 = cuisine_lief[:n].copy()
            # others
            others_lief = pd.DataFrame(
                data={
                    'type_of_cuisine': ['others'],
                    'value': [cuisine_lief['restaurant_name'][n:].sum()]
                })
            # combining data
            cuisine_bkdwn_wolt = pd.concat([cuisine_lief_top10,
                                            others_lief])["restaurant_name"]
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = cuisine_bkdwn_wolt.index
            sizes = cuisine_bkdwn_wolt
            cuisine_bkdwn_wolt.plot(kind='pie',
                                    autopct=autopct,
                                    cmap=cmap,
                                    fontsize=fontsize)
            #plt.title("Lieferando - Breakdown by type of cuisine", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")
            st.pyplot()

        with cui_wolt:
            st.subheader('Wolt')
            # select from df
            cuisine_wolt = all_data[(all_data.database == "wolt")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)
            # top n
            n = 8
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
            #plt.title("Wolt - Breakdown by type of cuisine", fontsize=15)
            #st.subheader('Breakdown by type of cuisine')
            plt.ylabel(" ")
            plt.xlabel(" ")
            st.pyplot()

        with cui_all:
            st.subheader('All restaurants')
            # select from df
            cuisine_wolt = all_data[(all_data.database == "here_maps")
                                    & search_limits].groupby(
                                        by="type_of_cuisine").count()[[
                                            "restaurant_name"
                                        ]].sort_values(by="restaurant_name",
                                                    ascending=False)
            # top n
            n = 7
            cuisine_wolt_top10 = cuisine_wolt[:n].copy()
            # others
            others_wolt = pd.DataFrame(
                data={
                    'type_of_cuisine': ['others'],
                    'value': [cuisine_wolt['restaurant_name'][n:].sum()]
                })
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
            #plt.title("All Restaurants - Breakdown by type of cuisine", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")
            st.pyplot()


        ''' Breakdown by restaurant quality '''
        qual_lief, qual_wolt, qual_all = st.columns(3)
        st.subheader('Breakdown by restaurant quality:')
        with qual_lief:
            st.subheader('Lieferando')
            # select from df
            good_restos_liefe = all_data[
                (all_data.database == "lieferando")
                & search_limits & (all_data.avg_review_score >=
                                good_restos_rankingbase)].count()["restaurant_name"]

            regular_restos_liefe = all_data[
                (all_data.database == "lieferando")
                & search_limits & (all_data.avg_review_score >= regular_restos_rankingbase)
                & (all_data.avg_review_score <
                good_restos_rankingbase)].count()["restaurant_name"]

            bad_restos_liefe = all_data[
                (all_data.database == "lieferando")
                & search_limits & (all_data.avg_review_score <
                                regular_restos_rankingbase)].count()["restaurant_name"]


            # Pie chart, where the slices will be ordered and plotted counter-clockwise, only for categories >0
            info = [("good", good_restos_liefe), ("regular", regular_restos_liefe),
                    ("bad", bad_restos_liefe)]

            labels = [x[0] for x in info if x[1] > 0]
            sizes = [x[1] for x in info if x[1] > 0]

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,
                    autopct=autopct,
                    labels=labels,
                    colors=["#64bb63","#5a9dcd", "#ec772f"]
                    );
            #plt.title("Lieferando - Breakdown by restaurant quality", fontsize=15)
            plt.ylabel(" ")
            # plt.legend(labels);
            plt.xlabel(" ")
            st.pyplot()

        with qual_wolt:
            st.subheader('Wolt')
            # select from df
            good_restos_wolt = all_data[
                (all_data.database == "wolt")
                & search_limits & (all_data.avg_review_score >=
                                good_restos_rankingbase)].count()["restaurant_name"]


            regular_restos_wolt = all_data[
                (all_data.database == "wolt")
                & search_limits & (all_data.avg_review_score >= regular_restos_rankingbase)
                & (all_data.avg_review_score <
                good_restos_rankingbase)].count()["restaurant_name"]

            bad_restos_wolt = all_data[
                (all_data.database == "wolt")
                & search_limits & (all_data.avg_review_score <
                                regular_restos_rankingbase)].count()["restaurant_name"]

            # Pie chart, where the slices will be ordered and plotted counter-clockwise, only for categories >0
            info = [("good", good_restos_wolt), ("regular", regular_restos_wolt),
                    ("bad", bad_restos_wolt)]

            labels = [x[0] for x in info if x[1]>0]
            sizes = [x[1] for x in info if x[1] > 0]


            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,
                    autopct=autopct,
                    labels=labels,
                    colors=["#64bb63", "#5a9dcd", "#ec772f"])
            #plt.title("Wolt - Breakdown by restaurant quality" , fontsize=15)
            plt.ylabel(" ")
            # plt.legend(labels)
            plt.xlabel(" ")
            st.pyplot()

        with qual_all:
            st.subheader('All')
            st.caption('Not available')



        ''' Top ranked categories '''
        top_lief, top_wolt, top_all = st.columns(3)
        st.subheader('Top ranked categories:')
        with top_lief:
            st.subheader('Lieferando')
            top_n = 10
            top10cats_liefe = all_data[(all_data.database == "lieferando")
                           & search_limits].groupby(
                               by=["type_of_cuisine"
                                   ]).mean()["avg_review_score"].sort_values(
                                       ascending=True)[-top_n:]
            top10cats_liefe = top10cats_liefe.reset_index()
            # creating plot
            fig, ax = plt.subplots()

            labels = top10cats_liefe.avg_review_score.tolist()
            figure = ax.barh(
                top10cats_liefe.type_of_cuisine.tolist(),
                labels,
                align='center',
                color=hex_colors)

            ax.bar_label(figure, fmt='%.2f', fontsize=12, fontweight='bold')
            ax.set_xlim(right=10)
            #plt.title("Lieferando - Top 10 ranked categories", fontsize=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot()

        with top_wolt:
            st.subheader('Wolt')
            top_n = 10
            top10cats_wolt = all_data[(all_data.database == "wolt")
                                    & search_limits].groupby(
                                        by=["type_of_cuisine"
                                            ]).mean()["avg_review_score"].sort_values(
                                                ascending=True)[-top_n:]
            top10cats_wolt = top10cats_wolt.reset_index()

            # creating plot
            fig, ax = plt.subplots()

            labels = top10cats_wolt.avg_review_score.tolist()
            figure = ax.barh(top10cats_wolt.type_of_cuisine.tolist(),
                    labels,
                    # xerr=error,
                    align='center', color = hex_colors);

            ax.bar_label(figure, fmt='%.2f', fontsize=12, fontweight='bold')
            ax.set_xlim(right=10);
            plt.title("Wolt - Top 10 ranked categories", fontsize=15);
            ax.spines['top'].set_visible(False);
            ax.spines['right'].set_visible(False);
            st.pyplot()

        with top_all:
            st.subheader('All')
            st.caption('Not available')



        ''' Breakdown by budget-type restaurants '''
        st.subheader('Breakdown by budget-type restaurants:')
        bud_lief, bud_wolt, bud_all = st.columns(3)
        with bud_lief:
            st.subheader('Lieferando')
            price_2_limit = 1.5
            price_3_limit = 2.5
            price_4_limit = 3.5

            na_values = all_data[(all_data.database == "lieferando") & search_limits &
                    (all_data.pricyness == 0)]["restaurant_name"].count()

            pricyness_1 = all_data[(all_data.database == "lieferando") & search_limits &
                    (all_data.pricyness > 0) &
                    (all_data.pricyness < price_2_limit)].count()['restaurant_name']

            pricyness_2 = all_data[(all_data.database == "lieferando") & search_limits &
                                (all_data.pricyness >= price_2_limit) &
                                (all_data.pricyness <
                                    price_3_limit)].count()['restaurant_name']

            pricyness_3 = all_data[(all_data.database == "lieferando") & search_limits &
                                (all_data.pricyness >= price_3_limit) &
                                (all_data.pricyness <
                                    price_4_limit)].count()['restaurant_name']

            pricyness_4 = all_data[(all_data.database == "lieferando") & search_limits &
                                (all_data.pricyness >= price_4_limit)].count()['restaurant_name']

            # Pie chart, where the slices will be ordered and plotted counter-clockwise, only for categories >0
            info = [("n.a.", na_values), ("€", pricyness_1), ("€€", pricyness_2),
                    ("€€€", pricyness_3), ("€€€€", pricyness_4)]

            labels = [x[0] for x in info if x[1]>0]
            sizes = [x[1] for x in info if x[1] > 0]

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,
                    autopct=autopct,
                    labels=labels,
                    colors=[
                        "#bed3e8"
                        ,"#64bb63",
                        "#5a9dcd",
                        "#ec772f",
                        "#8b8ab8",
                        "#9ecd8e",
                    ])
            #plt.title("Lieferando - Breakdown by pricyness", fontsize=15)
            plt.ylabel(" ")
            # plt.legend(labels)
            plt.xlabel(" ")
            st.pyplot()

        with bud_wolt:
            st.subheader('Wolt')
            bkdn_byprice_wolt = all_data[(all_data.database == "wolt") & search_limits].groupby(
                by="pricyness").count()['restaurant_name']
            # Pie chart, where the slices will be ordered and plotted counter-clockwise:
            labels = ["€","€€","€€€","€€€€"]
            sizes = bkdn_byprice_wolt.tolist()
            bkdn_byprice_wolt.plot(kind='pie',
                                autopct=autopct,
                                labels=labels,
                                colors=["#3182bd", "#fd8d3c", "#a1d99b", "#dadaeb"])
            #plt.title("Wolt - Breakdown by pricyness", fontsize=15)
            plt.ylabel(" ")
            plt.xlabel(" ")
            st.pyplot()

        with bud_all:
            st.subheader('All')
            st.caption('Not available')




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
