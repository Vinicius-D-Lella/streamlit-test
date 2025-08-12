import streamlit as st
import pandas as pd 

conn = st.connection("sql")
conteudos = conn.query('SELECT * FROM public."Content";')
subscriptions = conn.query('SELECT * FROM public."Subscription";')
freeContent = conn.query('SELECT * FROM public."OfferAccess" WHERE "offerId" = 3;')
user = conn.query('SELECT * FROM public."User";')
raw_views = conn.query('''SELECT "createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo', * FROM public."ContentView" WHERE "totalViews" != 0;''')
modulos = conn.query('SELECT * FROM public."Module";')


views = []
raw_views = raw_views.sort_values(by="timezone", ascending=True)



for row in raw_views.itertuples():
    totalViews = 0
    frcView = 0
    pacView = 0
    sfrView = 0
    spaView = 0
    ufrView = 0
    if row.totalViews > 10:
        totalViews = 10
    else:
        totalViews = row.totalViews
    if conteudos[conteudos.id == row.contentId].moduleId.values[0] in freeContent.moduleId.values or row.contentId in freeContent.contentId.values:
        if row.totalViews > 10:
            frcView = 10
        else:
            frcView = row.totalViews
    else:
        if row.totalViews > 10:
            pacView = 10
        else:
            pacView = row.totalViews
        
    if row.userId not in subscriptions.userId.values:
        if row.totalViews > 10:
            ufrView = 10
        else:
            ufrView = row.totalViews
    else:
        if conteudos[conteudos.id == row.contentId].moduleId.values[0] in freeContent.moduleId.values or row.contentId in freeContent.contentId.values:
            if row.totalViews > 10:
                sfrView = 10
            else:
                sfrView = row.totalViews
        else:
            if row.totalViews > 10:
                spaView = 10
            else:
                spaView = row.totalViews

    if row.contentId not in [item["contentId"] for item in views]:
        views.append({
            "contentId": row.contentId,
            "moduleId": conteudos[conteudos.id == row.contentId].moduleId.values[0],
            "totalViews": totalViews,
            "freeContentView":frcView,
            "paidContentView":pacView,
            "subFreeContentView": sfrView,
            "subPaidContentView": spaView,
            "unsubFreeContentView": ufrView,
            "viewedAt": [{str(row.timezone)[0:10] : totalViews}]
            })
    else:
        for item in views:
            if item["contentId"] == row.contentId:
                item["totalViews"] += totalViews
                item["freeContentView"] += frcView
                item["paidContentView"] += pacView
                item["unsubFreeContentView"] += ufrView
                item["subFreeContentView"] += sfrView
                item["subPaidContentView"] += spaView
                if str(row.timezone)[0:10] not in [list(view.keys())[0] for view in item["viewedAt"]]:
                    item["viewedAt"].append({str(row.timezone)[0:10] : totalViews})
                else:
                    for view in item["viewedAt"]:
                        if list(view.keys())[0] == str(row.timezone)[0:10]:
                            view[str(row.timezone)[0:10]] += totalViews


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
            "freeContentView":row.freeContentView,
            "paidContentView":row.paidContentView,
            "subFreeContentView":row.subFreeContentView,
            "subPaidContentView":row.subPaidContentView,
            "unsubFreeContentView":row.unsubFreeContentView,
            "viewedAt": row.viewedAt,
            "contentId": row.contentId
            })


tabelaContent = pd.DataFrame(tabelaContent)

for row in tabelaContent.itertuples(): #le a linha
    viewsDates = []
    freeViewsDates = []
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
                "freeContentView":row.freeContentView,
                "paidContentView":row.paidContentView,
                "subFreeContentView":row.subFreeContentView,
                "subPaidContentView":row.subPaidContentView,
                "unsubFreeContentView":row.unsubFreeContentView,
                "moduleViewedAt": viewsDates
            })
        else: #se o modulo está na lista faz isso
            for item in tabelaModule:
                if item["id"] == row.moduleId:
                    item["totalModuleViews"] += row.views
                    item["freeContentView"] += row.freeContentView
                    item["paidContentView"] += row.paidContentView
                    item["subFreeContentView"] += row.subFreeContentView
                    item["subPaidContentView"] += row.subPaidContentView
                    item["unsubFreeContentView"] += row.unsubFreeContentView
                    for view in viewsDates:
                        if list(view.keys())[0] not in [list(moduleView.keys())[0] for moduleView in item["moduleViewedAt"]]:
                            item["moduleViewedAt"].append(view)
                        else:
                            for moduleView in item["moduleViewedAt"]:
                                if list(moduleView.keys())[0] == list(view.keys())[0]:
                                    moduleView[list(view.keys())[0]] += list(view.values())[0]

tabelaModule = pd.DataFrame(tabelaModule)

#st.title("Ranking de Módulos")
tabelaModule = tabelaModule.sort_values(by="totalModuleViews", ascending=False)
#st.dataframe(tabelaModule, column_config={
#    "id": None,
#    "title": "Nome do Modulo",
#    "totalModuleViews": "Total de Views",
#    "moduleViewedAt": None,
#},
#    hide_index=True,
#)

st.write("views")
st.write(views)
st.write("tabelaContent")
st.write(tabelaContent)
st.write("tabelaModule")
st.write(tabelaModule)


