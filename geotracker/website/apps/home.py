import streamlit as st

''' HOME '''


def app():
    st.title('GeoCompetitor Tracker')
    st.subheader('By Ayelen Klas, Edmondo Castoldi, Malte Berneaud-Kötz and Nicole C. Dressler')
    st.caption('Le Wagon Data Science - Batch 735')
    st.image("https://images.unsplash.com/photo-1526367790999-0150786686a2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8ZGVsaXZlcnklMjBzZXJ2aWNlfGVufDB8fDB8fA%3D%3D&w=1000&q=80")
    st.markdown('''
    :heavy_exclamation_mark::heavy_exclamation_mark:Problem found:\n
    \n
    Food Delivery apps struggle to have visibility over their competitors,
    therefore they lose focus on where to expand/adapt their strategy geographically.\n
    \n
    :white_check_mark: Proposed solution:\n
    \n
    We provide an insight-tracker tool to make business decisions,
    such as where to focus or how to adapt the business model/strategy by
    scraping data from the main delivery apps and comparing their main KPIs in Berlin.\n
    \n
    ''')
    st.subheader('Usage instructions')
    st.markdown('''The **Search** page will give you an overall analysis on the restaurants,
    as a total and filtered by delivery company. There, you'll enter the Zipcode desired to obtain the informations
    on that location.''')
    st.markdown(
        ''':sleuth_or_spy:Choose the filters accordingly to your preference and search the location!'''
    )
    st.markdown('''The **Recommend** page will provide a prediction on the best location to
    expand a delivery business in the city of Berlin.''')
    st.markdown(
        ''':sleuth_or_spy:Again, choose the filters accordingly to your preference and predict the location!'''
    )
    st.subheader('Have a nice tracking!')
