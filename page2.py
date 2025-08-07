import streamlit as st
import pandas as pd


df = pd.read_json("assinaturas.json")

st.text("esse daqui seria bom pra fazer um grafico de views diarios no modulo com uma barra em cada lançamento de video")
#esse daqui seria bom pra fazer um grafico de views diarios no modulo com uma barra em cada lançamento de video
st.area_chart(df.set_index('name')['assinaturas'])
