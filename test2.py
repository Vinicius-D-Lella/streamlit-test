import streamlit as st
import pandas as pd

pages = {
    "Pages": [
        st.Page("home.py", title="Home"),
        st.Page("module_views.py", title="Graficos de área"),
        st.Page("multi_area.py", title="Grafico de área multipla"),
    ]
}

pg = st.navigation(pages)
pg.run()

