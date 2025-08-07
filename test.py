import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Teste de graficos", layout="centered")

st.title("Ranking de coletores da missão")
st.subheader("Onça neles")

df = pd.read_json("assinaturas.json")
ordem = st.radio("Ordenar por:", ["Nome (A-Z)", "Nome (Z-A)", "Mais assinaturas", "Menos assinaturas"])

if ordem == "Nome (A-Z)":
    df = df.sort_values(by="name", ascending=True)
elif ordem == "Nome (Z-A)":
    df = df.sort_values(by="name", ascending=False)
elif ordem == "Mais assinaturas":
    df = df.sort_values(by="assinaturas", ascending=False)
elif ordem == "Menos assinaturas":
    df = df.sort_values(by="assinaturas", ascending=True)

fig, ax = plt.subplots(figsize=(10, len(df) * 0.3))
ax.barh(df["name"], df["assinaturas"], color='skyblue')
ax.set_xlabel("Assinaturas")
ax.set_ylabel("Nome")
ax.invert_yaxis()
st.pyplot(fig)

