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

def load_data_csv(file):
    # Detectar a codificação do arquivo
    result = chardet.detect(file.read())
    encoding = result['encoding']
    file.seek(0)  # Resetar o ponteiro do arquivo para o início

    # Ler o arquivo CSV com a codificação detectada
    df = pd.read_csv(file, delimiter="\t", encoding=encoding)
    return df

arquivo_csv = st.sidebar.file_uploader("Escolha arquivo tipo csv", type="csv")

if arquivo_csv is not None:
    tabela = load_data_csv(arquivo_csv)
    tabela_filtrada = filtrar_dados_csv_atividades(tabela)

    # Sidebar para navegação
    pagina = st.sidebar.selectbox("Escolha a página", ["Tabela", "Gráficos de Pizza", "Gráficos de Barras"])

    if pagina == "Tabela":
        st.write(tabela_filtrada)
    elif pagina == "Gráficos de Pizza":
        fazer_graficos_pie(tabela_filtrada)
    elif pagina == "Gráficos de Barras":
        criar_graficos_barras(tabela_filtrada)
else:
    st.warning("Inserir arquivo CSV")
