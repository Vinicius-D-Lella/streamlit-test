import streamlit as st
import pandas as pd 

conn = st.connection("sql")
conteudos = conn.query('SELECT "id","title","moduleId" FROM public."Content";')
subscriptions = conn.query('SELECT "userId" FROM public."Subscription";')
freeContent = conn.query('SELECT "moduleId","contentId" FROM public."OfferAccess" WHERE "offerId" = 3;')
raw_views = conn.query('''SELECT "createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo', CASE WHEN "totalViews" > 10 THEN 10 ELSE "totalViews" END AS "totalViews","contentId","userId" FROM public."ContentView" WHERE "totalViews" != 0;''')
modulos = conn.query('SELECT "id","name","createdAt" FROM public."Module";')

views = []
raw_views = raw_views.sort_values(by="timezone", ascending=True)

for row in raw_views.itertuples():

    if row.contentId not in [item["contentId"] for item in views]:
        views.append({
            "contentId": row.contentId,
            "moduleId": conteudos[conteudos.id == row.contentId].moduleId.values[0],
            "totalViews": row.totalViews,
            })
    else:
        for item in views:
            if item["contentId"] == row.contentId:
                item["totalViews"] += row.totalViews
                            
views = pd.DataFrame(views)

tabelaContent = []
tabelaModule = []

for row in views.itertuples():
    if row.contentId in conteudos.id.values:
        tabelaContent.append({
            "title": conteudos[conteudos.id == row.contentId].title.values[0],
            "moduleId": row.moduleId,
            "moduleName": modulos[modulos.id == row.moduleId].name.values[0],
            "views": row.totalViews,
            "contentId": row.contentId
            })

tabelaContent = pd.DataFrame(tabelaContent)

for row in tabelaContent.itertuples():
    if row.moduleId in modulos.id.values: 
        if row.moduleId not in [item["id"] for item in tabelaModule]:
            tabelaModule.append({
                "id": modulos[modulos.id == row.moduleId].id.values[0],
                "title": modulos[modulos.id == row.moduleId].name.values[0],
                "totalModuleViews": row.views,
            })
        else:
            for item in tabelaModule:
                if item["id"] == row.moduleId:
                    item["totalModuleViews"] += row.views

tabelaModule = pd.DataFrame(tabelaModule)

st.title("Ranking de Módulos")
tabelaModule = tabelaModule.sort_values(by="totalModuleViews", ascending=False)
st.dataframe(tabelaModule, column_config={
    "id": None,
    "title": "Nome do Modulo",
    "totalModuleViews": "Total de Views",

},
    hide_index=True,
)
