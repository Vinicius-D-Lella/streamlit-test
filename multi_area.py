import streamlit as st
import pandas as pd
from home import tabelaModule

st.title("Gráfico de Área Múltipla")
titulos = [item.title for item in tabelaModule.itertuples()]
options = st.multiselect(
    "Quais módulos você quer ver?",
    titulos,
    default=[],
)

dataOptions = []
for item in tabelaModule.itertuples():
    if item.title in options:
        dataOptions.append({
            "title": item.title,
            "data": item.moduleViewedAt,
            "totalViews": item.totalModuleViews
        })


data = pd.DataFrame()
for item in dataOptions:
    df = pd.DataFrame([
        {"Data": list(view.keys())[0], "Views": list(view.values())[0]}
        for view in item["data"]
    ])
    df["Data"] = pd.to_datetime(df["Data"])
    df.set_index("Data", inplace=True)
    df.rename(columns={"Views": item["title"]}, inplace=True)
    if data.empty:
        data = df
    else:
        data = data.join(df, how='outer')
        
st.area_chart(data)