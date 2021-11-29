from streamlit_folium import folium_static
import streamlit as st
import folium
import json
import pandas as pd


m = folium.Map(location=[52.520008, 13.404954], zoom_start=11, prefer_canvas=True)

with open("geotracker/website/data/geojson.json") as f:
    file = json.load(f)

for _, Name in pd.read_csv("geotracker/website/data/r4map.csv").iterrows():

    folium.Marker(
        location=[Name.lat, Name.lon],
        popup=Name.Name,
        icon=folium.Icon(color="red", icon="map-pin"),
    ).add_to(m)

folium.GeoJson(
    file,
    name="geojson.json"
    ).add_to(m)

folium_static(m)