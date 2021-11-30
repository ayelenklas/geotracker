from typing import Container
import streamlit as st
#import matplotlib.pyplot as plt

''' SEARCH '''

cuisine_options = ['African', 'American', 'Asian', 'Vegetarian or Vegan', 'Steak', 'South American',
'Snacks', 'Seafood', 'Russian', 'Poke', 'Middle Eastern', 'Mexican', 'Mediterranean', 'Italian', 'International',
'Indian', 'Healthy', 'Greek', 'Fastfood', 'European', 'Cafes', 'Breakfast/Dessert', 'Bars']

def app():
    st.title('Restaurants Analysis')

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


    liferando, wolt, allrestos = st.columns(3)

    if st.button('Search'):
        with liferando:
            st.write()
            #ayelen charts

    #do columns for maps to show
