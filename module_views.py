import streamlit as st
import pandas as pd
from home import tabelaModule

conn = st.connection("sql")
opcao = st.selectbox("Selecione o modulo", options=tabelaModule.title.values, key="selectModule", index=1)

linha = tabelaModule[tabelaModule["title"] == opcao].iloc[0]

conteudos = conn.query(f'SELECT "id" FROM public."Content" WHERE "moduleId" = {linha.id};')

raw_dateViews = conn.query(f'''
                   SELECT 
                   "contentId",
                    CASE WHEN "totalViews" > 10 THEN 10 ELSE "totalViews" END AS "totalViews",
                   "createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS "createdAt"
                   FROM public."ContentView"
                   WHERE "contentId" IN ({','.join(map(str, conteudos.id.values))})
                   AND "totalViews" > 0
                   ''')

st.write(raw_dateViews)

views = []
raw_views = raw_dateViews.sort_values(by="createdAt", ascending=True)

for row in raw_views.itertuples():
    if row.contentId not in [item["contentId"] for item in views]:
        views.append({
            "contentId": row.contentId,
            "totalViews": row.totalViews,
            "createdAt": [{ str(row.createdAt)[0:10]: row.totalViews }]
        })
    else:
        for item in views:
            if item["contentId"] == row.contentId:
                item["totalViews"] += row.totalViews
                if str(row.createdAt)[0:10] not in [list(d.keys())[0] for d in item["createdAt"]]:
                    item["createdAt"].append({ str(row.createdAt)[0:10]: row.totalViews })
                else:
                    for d in item["createdAt"]:
                        if list(d.keys())[0] == str(row.createdAt)[0:10]:
                            d[list(d.keys())[0]] += row.totalViews

views = pd.DataFrame(views)
st.write(views)
tabelaModuleHistory = {}
for row in views.itertuples():
    if tabelaModuleHistory == {}:
        tabelaModuleHistory = {
        "moduleId": linha.id,
        "totalViews": row.totalViews,
        "createdAt": row.createdAt
        }
    else:
        tabelaModuleHistory["totalViews"] += row.totalViews
        for date in row.createdAt:
            if str(list(date.keys())[0]) not in [str(d) for d in tabelaModuleHistory["createdAt"]]:
                tabelaModuleHistory["createdAt"].append(date)
            else:
                for d in tabelaModuleHistory["createdAt"]:
                    print(d)

tabelaModuleHistory = pd.DataFrame(tabelaModuleHistory)
st.write(tabelaModuleHistory)


#df = pd.DataFrame([
#    {"Data": list(item.keys())[0], "Views": list(item.values())[0]}
#    for item in moduloViews[0]["moduleViewedAt"]
#])

#df["Data"] = pd.to_datetime(df["Data"])
#df.set_index("Data", inplace=True)

#st.area_chart(df["Views"])