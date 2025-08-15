import altair as alt
import streamlit as st
import pandas as pd
from datetime import datetime
from home import tabelaModule

st.markdown("""
    <style>
        /* Centraliza todo o conteúdo */
        .block-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Análise de público")
select_module,select_date = st.columns(2)
activeContent,activeSpec = st.columns(2)
conn = st.connection("sql")
freeContent = conn.query('SELECT "moduleId","contentId" FROM public."OfferAccess" WHERE "offerId" = 3;')
subscriptions = conn.query('SELECT "userId" FROM public."Subscription";')
with select_module:
    opcao = st.selectbox("Selecione o módulo", options=tabelaModule.title.values, key="selectModule", index=1)
modulo = tabelaModule[tabelaModule["title"] == opcao].iloc[0]




conteudos = conn.query(f'SELECT "id" FROM public."Content" WHERE "moduleId" = {modulo.id};')

frcView = 0
pacView = 0
sfrView = 0
spaView = 0
ufrView = 0

initialDate = conn.query(f'''
                   SELECT 
                   CAST("createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS DATE) AS "createdAt"
                   FROM public."ContentView"
                   WHERE "contentId" IN ({','.join(map(str, conteudos.id.values))})''')

with activeContent:
    st.checkbox("Tipo de Conteudo", key="tipoConteudo", value=True)
with activeSpec:
    st.checkbox("Tipo de Espectador", key="tipoEspectador")

today = datetime.now()
start_limit = initialDate.createdAt[0]
start_date = start_limit
end_date = today
end_limit = today

with select_date:
    d = st.date_input(
    "Selecione o período",
    (start_date, end_date),
    start_limit,
    end_limit,
    format="DD/MM/YYYY",
    )


if len(d) == 2:
    start_date = d[0]
    end_date = d[1]

raw_dateViews = conn.query(f'''
                   SELECT 
                   "contentId",
                    "userId",
                    CASE WHEN "totalViews" > 10 THEN 10 ELSE "totalViews" END AS "totalViews",
                   CAST("createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS DATE) AS "createdAt"
                   FROM public."ContentView"
                   WHERE "contentId" IN ({','.join(map(str, conteudos.id.values))})
                   AND "totalViews" > 0
                   AND "createdAt" BETWEEN '{start_date}' AND '{end_date}'
                   ''')

raw_views = raw_dateViews.sort_values(by="createdAt", ascending=True)

contentViews = raw_views.groupby(["contentId", "createdAt"]).sum().reset_index()
contentViews = pd.DataFrame(contentViews)

if modulo.id in freeContent.moduleId.values:
    frcView = contentViews.totalViews.sum()
else:
    for row in contentViews.itertuples():
        if row.contentId in freeContent.contentId.values:
            frcView += row.totalViews
        else:
            pacView += row.totalViews

for row in raw_views.itertuples():
    if modulo.id in freeContent.moduleId.values:
        if row.userId not in subscriptions.userId.values:
            ufrView += row.totalViews
        else:
            sfrView += row.totalViews
    else:
        if row.userId not in subscriptions.userId.values and row.contentId in freeContent.contentId.values: ufrView += row.totalViews
        elif row.userId in subscriptions.userId.values and row.contentId in freeContent.contentId.values: sfrView += row.totalViews
        elif row.userId in subscriptions.userId.values and row.contentId not in freeContent.contentId.values: spaView += row.totalViews
        else: ufrView += row.totalViews
modulo = pd.DataFrame([modulo])

modulo = modulo.assign(
    frcView=frcView,
    pacView=pacView,
    sfrView=sfrView,
    spaView=spaView,
    ufrView=ufrView
)


dadosConteudo = []
dadosViewer = []
dadosConteudo.append({
            "Módulo":modulo.title.values[0],
            "Views":modulo.frcView.values[0],
            "Conteúdo":"Gratuito"
        })

dadosConteudo.append({
            "Módulo":modulo.title.values[0],
            "Views":modulo.pacView.values[0],
            "Conteúdo":"Pago"
        })

dadosViewer.append({
            "Módulo":modulo.title.values[0],
            "Views":modulo.ufrView.values[0],
            "Tipo de Visualização":"Unsub view gratuita"
        })
dadosViewer.append({
            "Módulo":modulo.title.values[0],
            "Views":modulo.sfrView.values[0],
            "Tipo de Visualização":"Sub view gratuita"
        })
dadosViewer.append({
            "Módulo":modulo.title.values[0],
            "Views":modulo.spaView.values[0],
            "Tipo de Visualização":"Sub view paga"
        })




dc = pd.DataFrame(dadosConteudo)
dv = pd.DataFrame(dadosViewer)
if dadosConteudo != []:
    if st.session_state.tipoConteudo:
        st.subheader("Gráfico de Barras - Conteúdo")
        st.bar_chart(dc, x="Módulo", y="Views", color="Conteúdo", stack=False, use_container_width=True)
    if st.session_state.tipoEspectador:
        st.subheader("Gráfico de Barras - Espectador")
        st.bar_chart(dv, x="Módulo", y="Views", color="Tipo de Visualização", stack=False, use_container_width=True)

