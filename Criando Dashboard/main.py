import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
#iniciar pagina em wide mode 
st.set_page_config(layout="wide")

def load_data(file):
    df = pd.read_excel(file)
    return df

#criar um upload file de arquvio xlsx
arquivo_xlsx = st.sidebar.file_uploader("Escolha um arquivo Excel", type="xlsx")

#inicializar df como None
df = None

#se arquivo xlsx não estiver vazio, carregar o arquivo
if arquivo_xlsx is not None:
    df = load_data(arquivo_xlsx)
    #exibir a planilha apenas se o df não for None
    with st.expander("Visualizar planilha"):
        st.dataframe(df, column_config={
            "Valor Unitário": st.column_config.NumberColumn(format="R$ %.2f",help="Valor unitário em reais"),
            "Valor Final": st.column_config.NumberColumn(format="R$ %.2f"),
            "Data": st.column_config.DateColumn(format="DD/MM/YYYY"),
            "Código Venda": st.column_config.NumberColumn(format="%d")
        })
    plot_fig_hist = px.histogram(df, 
        x="ID Loja",
        y="Quantidade",
        color="Produto",
        title="Quantidade por Loja",
        barmode="group"
    )
    st.write(plot_fig_hist)

    col1, col2, col3 = st.columns(3)
    
    with col1:
       #criar um metric que mostra o total de vendas
       total_vendas = df["Valor Final"].sum()
       st.metric("Total de Vendas", f"R$ {total_vendas:,.2f}")
    with col2:
        total_produtos_vendidos = df["Quantidade"].sum()
        st.metric("Total de Produtos Vendidos", total_produtos_vendidos)
    with col3:
        lojas = df["ID Loja"].nunique()
        st.metric("Total de Lojas", lojas)
else:
    st.warning("Inserir arquivo Excel")
