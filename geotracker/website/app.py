import streamlit as st
from multiapp import MultiApp
from apps import home, should_go, address

st.set_page_config(layout="wide")

apps = MultiApp()

# Add application here
apps.add_app("Home", home.app)
apps.add_app("Search", address.app)
apps.add_app("Recommend", should_go.app)

apps.run()
