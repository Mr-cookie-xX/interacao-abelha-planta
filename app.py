import pandas as pd
import streamlit as st

from interacao_abelha_planta.process import (
    InteractionDataProcessor,
)
from interacao_abelha_planta.sankey import (
    SankeyGraph,
    SankeyTheme,
)

st.set_page_config(
    page_title="Interações Abelhas-Plantas",
    layout="wide",
)

st.title(
    body="Gráfico Sankey das Interações Abelhas-Plantas",
)

st.sidebar.header("Configurações")

uploaded = st.sidebar.file_uploader(
    label="Upload do arquivo de dados",
    type=[".csv"],
    accept_multiple_files=False,
)

group_by = st.sidebar.radio(
    label="Agrupar por:",
    options=["flor", "abelha"],
    horizontal=True,
)

pages = st.sidebar.slider(
    "Número de páginas",
    min_value=1,
    max_value=3,
    value=1,
    step=1,
)

st.sidebar.subheader("Configuração do Tema do Sankey Graph")
color_left = st.sidebar.color_picker("Cor dos elementos à esquerda", "#79E353")
color_rigth = st.sidebar.color_picker("Cor dos elementos à direita", "#DB7500")
font_color = st.sidebar.color_picker("Cor das fontes", "#000000")
font_family = st.sidebar.selectbox("Fonte", ["Comic Sans", "Roboto", "Arial", "Helvetica"])
font_size = st.sidebar.slider("Tamanho da fonte", 8, 20, 10)

theme = SankeyTheme(
    color_left=color_left,
    color_right=color_rigth,
    font_color=font_color,
    font_family=font_family,
    font_size=font_size,
)

if not uploaded:
    st.info("Faça o upload de um arquivo CSV.")

else:
    df = pd.read_csv(filepath_or_buffer=uploaded)
    st.subheader("Pré-visualização dos dados brutos")
    st.dataframe(data=df, width='stretch')
    
    processor = InteractionDataProcessor(df=df, group_by=group_by)
    matrix_full = processor.build_matrix()

    st.subheader("Matriz de Interações")
    st.dataframe(data=matrix_full, width='stretch')

    st.divider()
    
    st.subheader("Paginação das interações")

    graph = SankeyGraph(theme=theme)
    
    for page, matrix in processor.paginate(pages=pages):
        st.markdown(f"### Página {page}")
        
        st.dataframe(data=matrix, width="stretch")
    
        fig = graph.figure(df=matrix)
        st.plotly_chart(fig, width='stretch')

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="Download PNG",
                data=fig.to_image(format="png"),
                file_name=f"sankey_pagina_{page}.png",
                mime="download/png",
            )

        with col2:
            st.download_button(
                label="Download HTML",
                data=fig.to_html(),
                file_name=f"sankey_pagina_{page}.html",
                mime="download/html",
            )

        with col3:
            st.download_button(
                label="Download Matrizes de Interações",
                data=matrix.to_csv().encode("utf-8"),
                file_name=f"sankey_pagina_{page}.csv",
                mime="download/csv",
            )
