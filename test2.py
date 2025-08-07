import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt


# Carregar dados
df = pd.read_json("assinaturas.json")
pizza = [{"vendas":57},{"vendas": 43}, {"vendas": 34}]

st.title("Título Principal")

st.subheader("Gráfico de barras")
st.text("gráfico para colocar quantas views cada video fez no primeiro dia ou na primeira semana")
#grafico para colocar quantas views cada video fez no primeiro dia ou na primeira semana
st.bar_chart(df[['name', 'assinaturas']].set_index('name'))

st.text("esse daqui seria bom pra fazer um grafico de views diarios no modulo com uma barra em cada lançamento de video")
#esse daqui seria bom pra fazer um grafico de views diarios no modulo com uma barra em cada lançamento de video
st.area_chart(df.set_index('name')['assinaturas'])

st.text("grafico de pizza que pode servir pra ver qual tipo de conteudo mais pega views do modulo")
#grafico de pizza que pode servir pra ver qual tipo de conteudo mais pega views do modulo
#valores = [item["vendas"] for item in pizza]
#fig, ax = plt.subplots()
#ax.pie(valores, autopct="%1.1f%%", startangle=140)
#ax.axis("equal")
#st.pyplot(fig)


# Filtro de ordenação (alfabética ou por número)
#ordem = st.radio("Ordenar por:", ["Nome (A-Z)", "Nome (Z-A)", "Mais assinaturas", "Menos assinaturas"])

#if ordem == "Nome (A-Z)":
#    df = df.sort_values(by="name", ascending=True)
#elif ordem == "Nome (Z-A)":
#    df = df.sort_values(by="name", ascending=False)
#elif ordem == "Mais assinaturas":
#    df = df.sort_values(by="assinaturas", ascending=False)
#elif ordem == "Menos assinaturas":
#    df = df.sort_values(by="assinaturas", ascending=True)

# Criar gráfico
#fig, ax = plt.subplots(figsize=(10, len(df) * 0.3))
#ax.barh(df["name"], df["assinaturas"], color='skyblue')
#ax.set_xlabel("Assinaturas")
#ax.set_ylabel("Nome")
#ax.invert_yaxis()  # Para o maior no topo
#st.pyplot(fig)
