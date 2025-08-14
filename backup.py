initialDate = conn.query(f'''
                   SELECT 
                   CAST("createdAt" AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS DATE) AS "createdAt"
                   FROM public."ContentView"
                   WHERE "contentId" IN ({','.join(map(str, conteudos.id.values))})''')




today = datetime.now()

start_limit = initialDate.createdAt[0]
start_date = start_limit
end_date = today
end_limit = today

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

tabelaModuleHistory = contentViews.groupby("createdAt").sum().reset_index()
tabelaModuleHistory = pd.DataFrame(tabelaModuleHistory)

record = tabelaModuleHistory.sort_values(by="totalViews", ascending=False).iloc[0]
Tabela = tabelaModuleHistory.rename(columns={"totalViews": "Views","createdAt": "Data"})

chart = (
    alt.Chart(Tabela)
    .mark_area(
        color="steelblue",         
        opacity=0.5,              
        line={"color": "steelblue"},    
        point={"color": "steelblue"}     
    )
    .encode(
        x=alt.X("Data:T", title="Data", axis=alt.Axis(format="%d/%m/%y")),
        y=alt.Y("Views:Q", title="Visualizações"),
        tooltip=[alt.Tooltip("Data:T", format="%d/%m/%y"), "Views"]
    )
    .properties(
        width=700,
        height=350
    )
)

st.altair_chart(chart, use_container_width=True)

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