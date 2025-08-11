import streamlit as st
import pandas as pd
from home import tabelaModule

opcao = st.selectbox("Selecione o modulo", options=tabelaModule.title.values, key="selectModule", index=1)

linha = tabelaModule[tabelaModule["title"] == opcao].iloc[0]

df = pd.DataFrame([
    {"Data": list(item.keys())[0], "Views": list(item.values())[0]}
    for item in linha.moduleViewedAt
])

df["Data"] = pd.to_datetime(df["Data"])
df.set_index("Data", inplace=True)

st.area_chart(df["Views"])