import streamlit as st

def address():
    '''Part 1'''
    st.title('Where can I expand?')
    address = st.text_input('Insert the address desired here:')
    range = st.slider('Choose the lenght of the radius:\n range in kilometers', max_value=10)  #max radius?
    #select_cui = st.multiselect('Cuisine', cuisines, default=None)
    # CTRL C, CTRL V, same thing as 'should_go' other options for the client to filter by?

    index, liferando, wolt = st.columns(3)#([3,1,2]) pick width if needed

    #or instead of fancy charts we can just display the dataframe,
    # depends on the time we have to plot it and make it pretty

    '''Part 2'''
    if st.button('Predict'):
        with index: #here display all infos from the restos, filters will be displayed on the map
            st.write('Name')
            st.write('Types of\ncuisine')
            st.write('Budget')
            st.write('Stars')
            st.write('Number of\nreviews')
            st.write('Average delivery\nfee')
            st.write('Average delivery\ntime')
            st.write('Average minimum\norder value')
            st.write('anything else?')

        with liferando:
            st.image('https://liferandos_logo.jpg')
            st.write(fig)  #all restos with liferando in the radius chosen
            #leave the structure empty and with button reasign values
            st.pyplot() #pie chart of cuisines
            st.pyplot() #pie chart of budget
            st.pyplot() #avg delivery fee
            st.pyplot() #avg delivey time
            st.pyplot() #avg min order
            st.pyplot() #what else
            #matplotlibs only need t o be coded once for both columns,
            #to be done when we have the data

        with wolt:
            st.image('https://wolts_logo.jpg')
            #leave the structure empty and with button reasign values
            st.write(fig)  #all restos with wolt in the radius chosen
            st.pyplot()  #pie chart of cuisines
            st.pyplot()  #pie chart of budget
            st.pyplot()  #avg delivery fee
            st.pyplot()  #avg delivey time
            st.pyplot()  #avg min order
            st.pyplot()  #what else


    '''Part 3'''
    col_pick, col_map = st.columns([1,5])

    with col_pick:
        del_comp = st.radio('Pick a delivery company:', ['Liferando', 'Wolt'])

    with col_map:
        if del_comp == 'Liferando':
            st.map() #show only lifs restos
        if del_comp == 'Wolt':
            st.map()  #show only wolts restos
        else:
            st.map() #same shisss as 'should_go' Ctrl C + Ctrl V, show all
