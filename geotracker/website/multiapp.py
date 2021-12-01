"""Frameworks for running multiple Streamlit applications as a single app.
"""

import streamlit as st


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.sidebar.title("GeoCompetitor Tracker")
        app = st.sidebar.radio('Go to:',
                           self.apps,
                           format_func=lambda app: app['title'])
        st.sidebar.image(
            "https://dwj199mwkel52.cloudfront.net/assets/lewagon-logo-square-b6124eb974be375884558e4464efce48a9b5664f18422768156364363ecdd1fc.png",
            width=50)
        app['function']()
