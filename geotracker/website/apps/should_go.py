import streamlit as st

'''Lists of all infos, or optionally put in another csv or txt file'''
neighs = [
    'Charlottenburg-Wilmersdorf', 'Friedrichshain-Kreuzberg', 'Lichtenberg',
    'Marzahn-Hellersdorf', 'Mitte', 'Neukölln', 'Pankow', 'Reinickendorf',
    'Spandau', 'Steglitz-Zehlendorf', 'Tempelhof-Schöneberg',
    'Treptow-Köpenick']
#do we want the main 'boroughs' or actually all the neighborhoods?

cuisines = [] #list of cuisines

#list_of_another_filters = []



def should_go():
    st.title('Where can I expand?')
    '''Filter part'''
    select_neig = st.selectbox(options=['Select a neighborhood', neighs])
    range = st.slider('Choose the lenght of the radius:\n range in kilometers', max_value=10) #max radius?
    select_cui = st.multiselect('Cuisine', cuisines, default=None)
    #other options for the client to filter by?

    '''Map part'''
    if st.button('Predict location'):
        st.map() #data
        # data = inputs above can be transformed in a np.array to call the information from our API/data
        #this map is the simple version, I can make it prettier and colorful etc if we want and have the time
        # (also space in heroku hehe oops, the package is called folium)


        #do we want to write or display something other than the map?
        '''Expand part'''
        with st.expander('See info of the restaurants displayed'):
            st.write()#list of restaurants and the infos selected in the filter)
