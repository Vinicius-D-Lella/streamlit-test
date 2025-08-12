import streamlit as st
import pandas as pd

pages = {
    "Pages": [
        st.Page("home.py", title="Home"),
        st.Page("module_views.py", title="Histórico de views"),
        st.Page("multi_area.py", title="Comparação de histórico de views"),
        st.Page("bar_chart.py", title="Comparação entre views de graça ou pagas"),
    ]
}

pg = st.navigation(pages)
pg.run()

