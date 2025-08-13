import streamlit as st
import pandas as pd 

conn = st.connection("sql")
views = conn.query('''
                   SELECT 
                   "contentId",
                   "Content"."title" AS "contentTitle",
                   "Content"."moduleId" AS "moduleId",
                   "Module"."name" AS "moduleName",
                   SUM(CASE WHEN "totalViews" > 10 THEN 10 ELSE "totalViews" END) AS "totalViews"
                   FROM public."ContentView"
                   INNER JOIN public."Content" ON "Content"."id" = "ContentView"."contentId"
                   INNER JOIN public."Module" ON "Module"."id" = "Content"."moduleId"
                   WHERE "totalViews" != 0
                   GROUP BY "contentId","moduleId","contentTitle","moduleName"
                   ;''')

tabelaModule = []

views = pd.DataFrame(views)
views = views.sort_values(by="totalViews", ascending=False)


for row in views.itertuples():
    if row.moduleId not in [item["id"] for item in tabelaModule]:
        tabelaModule.append({
            "id": row.moduleId,
            "title": row.moduleName,
            "totalModuleViews": row.totalViews
        })
    else:
        for item in tabelaModule:
            if item["id"] == row.moduleId:
                item["totalModuleViews"] += row.totalViews

tabelaModule = pd.DataFrame(tabelaModule)
tabelaModule = tabelaModule.sort_values(by="totalModuleViews", ascending=False)

st.title("Ranking de Módulos")
st.dataframe(tabelaModule, column_config={
    "id": None,
    "title": "Nome do Modulo",
    "totalModuleViews": "Total de Views",

},
    hide_index=True,
)

st.title("Ranking de Conteúdos")
st.dataframe(views, column_config={
    "contentId": None,
    "contentTitle": "Nome do Conteúdo",
    "totalViews": "Total de Views",
    "moduleId":None,
    "moduleName":"Módulo",
},
    hide_index=True,
)
