import streamlit as st
import pandas as pd

''' PREDICT '''

def app():
    st.title('Predict The Best Location')
    '''Filter part'''

    col1, col2 = st.columns(2)
    with col1:
        address = st.text_input('Insert the adress to search by:')
        range = st.slider('Choose the lenght of the radius:',
                          help='Shown in kilometers.',
                          min_value=0.5,
                          max_value=5.0,
                          step=0.1)
    with col2:
        overlap = st.slider(
            'Choose the overlapping amount in percentage:',
            help='The more they overlap, more accurate the prediction will be.',
            max_value=50,
            step=1)
        score = st.slider('Choose the minimum reviews score:', max_value=10, step=1)

    #get input filters from csv data
    params = []

    df = pd.read_csv('')




    '''Map part'''
    if st.button('Predict'):
        st.map() #data
        # data = inputs above can be transformed in a np.array to call the information from our API/data
        #this map is the simple version, I can make it prettier and colorful etc if we want and have the time
        # (also space in heroku hehe oops, the package is called folium)


        #do we want to write or display something other than the map?
        '''Expand part'''
        with st.expander('See info of the restaurants displayed'):
            st.write()#list of restaurants and the infos selected in the filter)
