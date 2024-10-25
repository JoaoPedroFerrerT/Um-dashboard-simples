import streamlit as st
import pandas as pd
import plotly.express as px
import chardet

st.set_page_config(layout="wide")

def fazer_graficos_pie(tabela_f):
    for i, coluna in enumerate(tabela_f.columns[:]):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        with col1 if i % 2 == 0 else col2:
            nome_f = tabela_f[coluna].dropna().unique()
            valor_f = tabela_f[coluna].dropna().value_counts()

            if len(nome_f) == len(valor_f):
                fig_pi = px.pie(values=valor_f, names=nome_f, title=f"{coluna}")
                st.write(fig_pi)
            else:
                st.write(f"Colunas tem valores diferentes {coluna}")

def criar_graficos_barras(tabela_f):
    for i, coluna in enumerate(tabela_f):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        with col1 if i % 2 == 0 else col2:
            valores = tabela_f[coluna].value_counts()

            fig_bar = px.bar(x=valores.index, y=valores.values, labels={'x': 'Status', 'y': 'Contagem'}, title=f'Conclusão da {coluna}')
            st.write(fig_bar)

def filtrar_dados_csv_atividades(tabela_f):
    tabela_f = tabela_f.reset_index(drop=True)
    colunas_para_remover = [col for col in tabela_f.columns if col.startswith("Unnamed:")]
    colunas_sem_importancia = ["Agende suas provas presencias", "Clique aqui", "Endereço de email"]
    
    # Remover colunas sem importância se existirem
    for coluna in colunas_sem_importancia:
        if coluna in tabela_f.columns:
            tabela_f = tabela_f.drop(columns=[coluna])
    
    tabela_f = tabela_f.drop(columns=colunas_para_remover)
    return tabela_f


    # Detectar a codificação do arquivo
file_path = "C:/Users/estagio.nead/Desktop/ESTAGIARIO - (JOÃO PEDRO)/Dashboard/Versão individual/progress.80009_epger_cicl.csv"
with open(file_path, "rb") as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

tabela = pd.read_csv(file_path, delimiter="\t", encoding=encoding)
    

tabela_filtrada = filtrar_dados_csv_atividades(tabela)

    # Sidebar para navegação
pagina = st.sidebar.selectbox("Escolha a página", ["Tabela", "Gráficos de Pizza", "Gráficos de Barras"])

if pagina == "Tabela":
    st.write(tabela_filtrada)
elif pagina == "Gráficos de Pizza":
    fazer_graficos_pie(tabela_filtrada)
elif pagina == "Gráficos de Barras":
    criar_graficos_barras(tabela_filtrada)

