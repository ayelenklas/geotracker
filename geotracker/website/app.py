import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import FastMarkerCluster
import json
import pandas as pd


m = folium.Map(location=[52.520008, 13.404954],
                zoom_start=11,
                prefer_canvas=True,
                tiles = "Stamen Terrain")

with open("geotracker/website/data/geojson.json") as f:
    file = json.load(f)

samples = pd.read_csv("geotracker/website/data/r4map.csv")

m.add_child(FastMarkerCluster(samples[['lat', 'lon']].values.tolist(), name="Restaurants"))
m.add_child(folium.ClickForMarker())

# for _, Name in pd.read_csv("geotracker/website/data/r4map.csv").iterrows():

#     folium.Marker(
#         location=[Name.lat, Name.lon],
#         popup=Name.Name,
#         icon=folium.Icon(color="red", icon="dot"),
#     ).add_to(m)

folium.GeoJson(
    file,
    name="geojson.json"
    ).add_to(m)

folium_static(m)