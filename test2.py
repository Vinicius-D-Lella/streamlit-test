import streamlit as st
import pandas as pd

pages = {
    "Pages": [
        st.Page("home.py", title="Home"),
        st.Page("module_views.py", title="Graficos de área"),
    ]
}

pg = st.navigation(pages)
pg.run()

