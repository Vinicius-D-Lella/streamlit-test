import streamlit as st
import pandas as pd

pages = {
    "Pages": [
        st.Page("page1.py", title="Home"),
        st.Page("page2.py", title="page 2"),
        st.Page("page3.py", title="page 3"),
    ],
    "Camera": [
        st.Page("camera.py", title="Camera"),
    ],
}

# Carregar dados
df = pd.read_json("assinaturas.json")

pg = st.navigation(pages)
pg.run()

