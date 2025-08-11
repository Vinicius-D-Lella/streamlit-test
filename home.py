import streamlit as st
import pandas as pd 

conn = st.connection("sql")
conteudos = conn.query('SELECT * FROM public."Content";')
raw_views = conn.query('''SELECT "createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo', * FROM public."ContentView";''')
modulos = conn.query('SELECT * FROM public."Module";')

views = []
raw_views = raw_views.sort_values(by="timezone", ascending=True)


for row in raw_views.itertuples():
    if not row.totalViews == 0:
        if row.contentId not in [item["contentId"] for item in views]:
        
            views.append({
                "contentId": row.contentId,
                "totalViews": row.totalViews,
                "viewedAt": [{str(row.timezone)[0:10] : row.totalViews}]
                })
        else:
            for item in views:
                if item["contentId"] == row.contentId:
                    item["totalViews"] += row.totalViews
                    if str(row.timezone)[0:10] not in [list(view.keys())[0] for view in item["viewedAt"]]:
                        item["viewedAt"].append({str(row.timezone)[0:10] : row.totalViews})
                    else:
                        for view in item["viewedAt"]:
                            if list(view.keys())[0] == str(row.timezone)[0:10]:
                                view[str(row.timezone)[0:10]] += row.totalViews

views = pd.DataFrame(views)


tabelaContent = []
tabelaModule = []
for row in views.itertuples():
    if row.contentId in conteudos.id.values:
        tabelaContent.append({
            "title": conteudos[conteudos.id == row.contentId].title.values[0],
            "moduleId": conteudos[conteudos.id == row.contentId].moduleId.values[0],
            "moduleName": modulos[modulos.id == conteudos[conteudos.id == row.contentId].moduleId.values[0]].name.values[0],
            "views": row.totalViews,
            "viewedAt": row.viewedAt,
            "contentId": row.contentId
            })


tabelaContent = pd.DataFrame(tabelaContent)

for row in tabelaContent.itertuples(): #le a linha
    viewsDates = []
    for obj in row.viewedAt:
        for item, date in obj.items():
            if item not in [list(view.keys())[0] for view in viewsDates]: #verifica se a data já está na lista
                viewsDates.append({
                    item: date
                })
            else:
                for view in viewsDates:
                    if list(view.keys())[0] == item:
                        view[item] += date
                
    if row.moduleId in modulos.id.values: #verifica se o conteudo tem modulo
        if row.moduleId not in [item["id"] for item in tabelaModule]: #se o modulo não está na lista faz isso
            tabelaModule.append({
                "id": modulos[modulos.id == row.moduleId].id.values[0],
                "title": modulos[modulos.id == row.moduleId].name.values[0],
                "totalModuleViews": row.views,
                "moduleViewedAt": viewsDates,
            })
        else: #se o modulo está na lista faz isso
            for item in tabelaModule:
                if item["id"] == row.moduleId:
                    item["totalModuleViews"] += row.views
                    for view in viewsDates:
                        if list(view.keys())[0] not in [list(moduleView.keys())[0] for moduleView in item["moduleViewedAt"]]:
                            item["moduleViewedAt"].append(view)
                        else:
                            for moduleView in item["moduleViewedAt"]:
                                if list(moduleView.keys())[0] == list(view.keys())[0]:
                                    moduleView[list(view.keys())[0]] += list(view.values())[0]


tabelaModule = pd.DataFrame(tabelaModule)

select = 11

st.title("Ranking de modulos")
tabelaModule = tabelaModule.sort_values(by="totalModuleViews", ascending=False)
st.dataframe(tabelaModule, column_config={
    "id": None,
    "title": "Nome do Modulo",
    "totalModuleViews": "Total de Views",
    "moduleViewedAt": None,
},
    hide_index=True,
)


