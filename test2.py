import streamlit as st
import pandas as pd

pages = {
    "Pages": [
        st.Page("home.py", title="Resumo do Dia"),
        st.Page("module_views.py", title="Análise de Módulo"),
        st.Page("bar_chart_solo.py", title="Comparação entre módulos"),
        #st.Page("multi_area.py", title="Comparação de histórico de views"),
        #st.Page("bar_chart.py", title="Comparação entre views de graça ou pagas"),
    ]
}

pg = st.navigation(pages)
pg.run()

