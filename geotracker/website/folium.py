import json
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster

m = folium.Map(location=[52.520008, 13.404954],
                zoom_start=10, # map layout - no touch
                prefer_canvas=True,)

with open("geotracker/website/data/geojson.json") as f:
    file = json.load(f) #geojson file (berlin borders)

folium.GeoJson(
    file,
    name="geojson.json"
    ).add_to(m)

samples = pd.read_csv("geotracker/website/data/r4map.csv") # this is the part to swap based on the display:
 # samples and cluster selectors
m.add_child(FastMarkerCluster(samples[['lat', 'lon']].values.tolist()))

folium_static(m) # <- this outputs the map
#                      on the site