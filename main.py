# Autor: Pedro Lucas Berto - Versão: 01 - Data: 30/04/2025 - Norven
#from idlelib.multicall import MC_ENTER

# -------------------------------------------------------------------------------------------------------------------- #

# Bibliotecas:

import pandas as pd
import streamlit as st
import numpy as np
import matplotlib as plt
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

from altair.vegalite.v5.theme import theme
from streamlit import sidebar

# -------------------------------------------------------------------------------------------------------------------- #

#Importações adicionais:
from funcoes import ler_excel, grafico_relevancia,plotar_indice,definicao_periodo,escolha_indice,abilitar_correlação_dolar,grafico_correlação




# -------------------------------------------------------------------------------------------------------------------- #

#Interface:
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Sobre'

# Expande a sidebar automaticamente ao mudar para "Análises específicas"
if st.session_state.active_tab == 'Análises específicas':
    st.session_state.sidebar_state = 'expanded'
elif st.session_state.active_tab == 'Sobre':
    st.session_state.sidebar_state = 'expanded'
else:
    st.session_state.sidebar_state = 'collapsed'


st.set_page_config(
    page_title="Dashboard de Índices de Saneamento",
    page_icon="💧",
    layout="wide",
)



guias = ['Sobre','Relevância do índices','Análises específicas','Conclusões Norven']

st.session_state.active_tab = st.radio("Escolha uma análise:", guias, horizontal=True, label_visibility='collapsed')


# -------------------------------------------------------------------------------------------------------------------- #

# Caminhos para leitutra:

caminho_descritivo_indices_atualizacao_monetaria_utilizados = r'PLB_Tabela_indices_demais_empresas.xlsx'

caminho_indices_atualizacao_monetaria = r'Tabela_indices.xlsx'

aba_leitura_caminho_relevancia_indices_atualizacao_monetaria_utilizados = 'PLB_Relevância dos índices'

aba_leitura_caminho_indices_atualizacao_monetaria = 'ÍNDICES_PARA_GRÁFICO'

aba_leitura_caminho_descritivo_indices_atualizacao_monetaria_utilizados = 'Descritivo índices'

aba_leitura_conclusoes_descritivo_indices_atualizacao_monetaria_utilizados = 'Conclusões Norven'

# Leitura dos arquivos:

relevancia_indices_atualizacao_monetaria_utilizados = ler_excel(caminho_descritivo_indices_atualizacao_monetaria_utilizados,aba_leitura_caminho_relevancia_indices_atualizacao_monetaria_utilizados)

indices_atualizacao_monetaria = ler_excel(caminho_indices_atualizacao_monetaria,aba_leitura_caminho_indices_atualizacao_monetaria)

descritivo_indices_atualizacao_monetaria_utilizados =ler_excel(caminho_descritivo_indices_atualizacao_monetaria_utilizados,aba_leitura_caminho_descritivo_indices_atualizacao_monetaria_utilizados)

conclusoes_norven = ler_excel(caminho_descritivo_indices_atualizacao_monetaria_utilizados,aba_leitura_conclusoes_descritivo_indices_atualizacao_monetaria_utilizados)
# -------------------------------------------------------------------------------------------------------------------- #
if st.session_state.active_tab == 'Relevância do índices':


    #Ajuste de layout:
    col1,col2 =st.columns([3,2])


    col_indice = 'índices'
    col_sap = 'Código SAP'
    col_relevancia = 'Relevância'

    # descritivo_resumido = descritivo_indices_atualizacao_monetaria_utilizados.drop(columns=['Relevância', 'Qtd.Empresa'])

    grafico_relevancia_indices = grafico_relevancia(relevancia_indices_atualizacao_monetaria_utilizados,col_indice,col_sap,col_relevancia)


    with col1:
        st.subheader('Rpresentatividade de alguns índices utilizados na valoração de ativos no setor de saneamento:')
        st.plotly_chart(grafico_relevancia_indices,use_container_width=True)
    with col2:
        st.subheader('Descritivo dos índices:')
        st.dataframe(descritivo_indices_atualizacao_monetaria_utilizados,hide_index=True,width=500,height=600,row_height=52)


# -------------------------------------------------------------------------------------------------------------------- #
elif st.session_state.active_tab == 'Análises específicas':

    data_inicial, data_final = definicao_periodo()

    # Ajuste descritivo:
    descritivo_indices_atualizacao_monetaria_utilizados.loc[
            descritivo_indices_atualizacao_monetaria_utilizados['Código SAP'] == '-', 'Código SAP'] = \
            descritivo_indices_atualizacao_monetaria_utilizados['índices']

    chave_nome_indice_codigo_sap = descritivo_indices_atualizacao_monetaria_utilizados.set_index('índices')[
            'Código SAP'].to_dict()

    escolha_indice = escolha_indice(chave_nome_indice_codigo_sap)

    codigo_sap = [chave_nome_indice_codigo_sap[indice] for indice in escolha_indice]

    plotar_indice(indices_atualizacao_monetaria, codigo_sap, data_inicial, data_final)

elif st.session_state.active_tab == 'Sobre':

    #with st.sidebar:
        gif_path = r"C:\Users\pedro.NORVEN\Desktop\DashBoard_SABESB\imagens\animação-logo-e-frase.gif"  # Caminho local para o GIF

        with open(gif_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode("utf-8")

        st.markdown(
            f"""
                <div style="text-align: center;">
                    <img src="data:image/gif;base64,{encoded}" alt="GIF animado" width=1200">
                </div>
                """,
            unsafe_allow_html=True
        )
        with sidebar:
            st.markdown(
                "<h3 style='color: #1B1B1B; font-family: \"Styrene A Regular\", sans-serif;'>" "Dashboard Norven: Índices de atualização monetária</h3>",
                unsafe_allow_html=True)

elif st.session_state.active_tab == 'Conclusões Norven':
    
    st.dataframe(
        conclusoes_norven,
        hide_index=True,
        use_container_width=True,
        height=900,  # define a altura da tabela com scroll se necessário
        row_height=100  # ajusta a altura de cada linha
        )






