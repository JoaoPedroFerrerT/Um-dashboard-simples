import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

altura_figures = 225

def load_data(file):
    df = pd.read_excel(file, engine="odf")
    return df

carregar = st.sidebar.file_uploader("Escolher arquivo ods", type=".ods")



if carregar is not None:
    tabela = load_data(carregar)
    tabela.replace("-", np.nan, inplace=True)
    col1, col2, col3, col4 = st.columns(4)
#com coluna faça:
    with col1:
        numero_alunos = len(tabela["Nome"])
        fig1 = go.Figure(go.Indicator(
            mode = "number",
            value = numero_alunos,
            title = {"text": "Total de alunos"}))
        fig1.update_layout(height=altura_figures)
        st.plotly_chart(fig1)
    with col2:
    #alunos abaixo da média (7)
    #criar uma variavel que receba tabela e coluna tabela e vê os valores abaixo que 7 e não conte valores NaN e conte os valores
    #usar função len
    #acessar a coluna total do curso
    #pegar valores menor do que 7
    #tirar NaN(not a number)
    #usar o parametro subset para remover os NaN 
        alunos_abaixo_media = len(tabela[tabela["Total do curso (Real)"] < 7].dropna(subset=["Total do curso (Real)"]))
        fig2 = go.Figure(go.Indicator(
            mode= "number",
            value= alunos_abaixo_media,
            title= {"text": "Total de alunos abaixo da média"}
    ))
        fig2.update_layout(height=altura_figures)
        st.plotly_chart(fig2)
    with col3:
    #mesma coisa da col2 mas agora com alunos igual ou acima da média
        alunos_acima_media = len(tabela[tabela["Total do curso (Real)"] >= 7].dropna(subset=["Total do curso (Real)"]))
        fig3 = go.Figure(go.Indicator(
            mode= "number",
            value= alunos_acima_media,
            title= {"text": "Total de alunos acima da média"}
    ))
        fig3.update_layout(height=altura_figures)
        st.plotly_chart(fig3)
    with col4:
    #alunos sem nota(NaN)
        alunos_sem_media = tabela["Total do curso (Real)"].isna().sum()
        fig4 = go.Figure(go.Indicator(
            mode= "number",
            value= alunos_sem_media,
            title=  {"text": "Total de alunos sem nota"}
    ))
        fig4.update_layout(height=altura_figures)
        st.plotly_chart(fig4)
else:
    st.warning("Coloque um arquivo tipo ods")