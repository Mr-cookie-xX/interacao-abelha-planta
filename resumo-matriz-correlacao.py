import pandas as pd
from sankey import SankeyGraph

df = pd.read_csv(filepath_or_buffer="data/resumo/interacoes.csv", header=0)\
    .rename(
        columns={
            "Visitante": "abelha",
            "n° do indivíduo": "id_individuo",
            "Em flor de:": "flor",
        }
    )\
    .drop(['id_individuo'], axis=1)\
    .drop_duplicates(subset=['abelha', 'flor'])

df.to_csv(
    path_or_buf='data/resumo/interacoes-unicas.csv',
    mode='w',
    header=True,
    index=False,
    sep=','
)

df_count = df\
    .groupby(['flor'])\
    .count()\
    .rename({'abelha': 'count'}, axis=1)\
    .sort_values(by=['count'], ascending=False)

size = 0

for name, row in df_count.iterrows():
    size += row['count']
    if size >= df_count.sum(axis=0).to_list()[0] / 2:
        break

dfs = [
    df[df['flor'].isin(df_count.loc[:name].index.to_list())],
    df[df['flor'].isin(df_count.loc[name:].index.to_list())],
]

for i in range(len(dfs)):

    df_interacoes = pd.DataFrame(
        0,
        index=dfs[i]['flor'].drop_duplicates().to_list(),
        columns=dfs[i]['abelha'].drop_duplicates().to_list()
    )

    for _, row in dfs[i].iterrows():
        df_interacoes.at[row['flor'], row['abelha']] = 1

    SankeyGraph(df=df_interacoes)\
        .write_html(
            file=f"data/resumo/interacoes-matriz-correlacao-{i}.html",
        )

    SankeyGraph(df=df_interacoes)\
            .write_image(
                file=f"data/resumo/interacoes-matriz-correlacao-{i}.png",
            )
