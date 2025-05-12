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
from funcoes import ler_excel, grafico_relevancia, plotar_indice, definicao_periodo, escolha_indice, \
    abilitar_correlação_dolar, grafico_correlação, descritivo_especifico, definicao_periodos_dinamicos, \
    escolha_indice_limitado, comparar_indice

# -------------------------------------------------------------------------------------------------------------------- #

#Interface:
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Página Inicial'

# Expande a sidebar automaticamente ao mudar para "Análises específicas"
if st.session_state.active_tab == 'Análises específicas':
    st.session_state.sidebar_state = 'expanded'
elif st.session_state.active_tab == 'Página Inicial':
    st.session_state.sidebar_state = 'expanded'
elif st.session_state.active_tab == 'Descritivo dos índices':
    st.session_state.sidebar_state = 'expanded'
elif st.session_state.active_tab == 'Comparativo entre índices':
    st.session_state.sidebar_state = 'expanded'
else:
    st.session_state.sidebar_state = 'collapsed'


st.set_page_config(
    page_title="Dashboard de Índices de Saneamento",
    page_icon="💧",
    layout="wide",
)



guias = ['Página Inicial','Descritivo dos índices','Relevância do índices','Comparativo entre índices','Análises específicas','Conclusões Norven']

st.session_state.active_tab = st.radio("Escolha uma análise:", guias, horizontal=True, label_visibility='collapsed')


# -------------------------------------------------------------------------------------------------------------------- #

# Caminhos para leitutra:

caminho_descritivo_indices_atualizacao_monetaria_utilizados = r'PLB_Tabela_indices_demais_empresas.xlsx'

caminho_indices_atualizacao_monetaria = r'PLB_Tabela_indices.xlsx'

caminho_detalhamento_indices = r'PLB_indices_economicos_dashboard.xlsx'

aba_leitura_caminho_relevancia_indices_atualizacao_monetaria_utilizados = 'Relevância dos índices'

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
    col_indice = 'índices'
    col_sap = 'Código SAP'
    col_relevancia = 'Relevância'

    grafico_relevancia_indices = grafico_relevancia(relevancia_indices_atualizacao_monetaria_utilizados,col_indice,col_sap,col_relevancia)
    with st.container():
        with st.expander("ℹ️ Informações"):
            st.write("""
            Os dados de relevância foram levantados considerando-se os índices de atualização monetária utilizados nas seguintes empresas:

            - AGEPAR  
            - AGR  
            - ARESC  
            - AGERGS  
            - ADASA
            """)
    with st.container():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader('Representatividade de alguns índices utilizados na valoração de ativos no setor de saneamento:')
            st.plotly_chart(grafico_relevancia_indices,use_container_width=True)
        with col2:
            st.subheader('Identificação de índices e abreviações:')
            descritivo_indices_atualizacao_monetaria_utilizados = descritivo_indices_atualizacao_monetaria_utilizados.drop(columns=['Código SAP'])
            st.dataframe(descritivo_indices_atualizacao_monetaria_utilizados,hide_index=True,width=500,height=600,row_height=52)
# -------------------------------------------------------------------------------------------------------------------- #
elif st.session_state.active_tab == 'Análises específicas':

    data_inicial, data_final = definicao_periodo()

    # Ajuste descritivo:
    descritivo_indices_atualizacao_monetaria_utilizados.loc[
            descritivo_indices_atualizacao_monetaria_utilizados['Código SAP'] == '-', 'Código SAP'] = \
            descritivo_indices_atualizacao_monetaria_utilizados['índices']

    chave_nome_indice_codigo_sap = descritivo_indices_atualizacao_monetaria_utilizados.set_index('índices')[
            'Descrição Abreviada'].to_dict()

    escolha_indice = escolha_indice(chave_nome_indice_codigo_sap)

    codigo_sap = [chave_nome_indice_codigo_sap[indice] for indice in escolha_indice]                                     #Agora recebe o nome abreviado do índice comentário:1

    plotar_indice(indices_atualizacao_monetaria, codigo_sap, data_inicial, data_final)
# -------------------------------------------------------------------------------------------------------------------- #
elif st.session_state.active_tab == 'Página Inicial':

    #with st.sidebar:
        gif_path = r"animação-logo-e-frase.gif"

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

# -------------------------------------------------------------------------------------------------------------------- #

elif st.session_state.active_tab == 'Conclusões Norven':
    
    st.dataframe(
        conclusoes_norven,
        hide_index=True,
        use_container_width=True,
        height=900,  # define a altura da tabela com scroll se necessário
        row_height=100  # ajusta a altura de cada linha
        )
# -------------------------------------------------------------------------------------------------------------------- #

elif st.session_state.active_tab == 'Descritivo dos índices':
    descritivo_indices_atualizacao_monetaria_utilizados.loc[
        descritivo_indices_atualizacao_monetaria_utilizados['Código SAP'] == '-', 'Código SAP'] = \
        descritivo_indices_atualizacao_monetaria_utilizados['índices']

    chave_nome_indice_codigo_aba = descritivo_indices_atualizacao_monetaria_utilizados.set_index('índices')[
        'Código SAP'].to_dict()

    escolha_aba = escolha_indice(chave_nome_indice_codigo_aba)
    codigo_aba = [chave_nome_indice_codigo_aba[indice] for indice in escolha_aba]
    descritivo_especifico(caminho_detalhamento_indices,codigo_aba)

# -------------------------------------------------------------------------------------------------------------------- #

elif st.session_state.active_tab == 'Comparativo entre índices':
    escolha_periodos = definicao_periodos_dinamicos()

    chave_nome_indice_codigo_sap2 = descritivo_indices_atualizacao_monetaria_utilizados.set_index('índices')[
        'Descrição Abreviada'].to_dict()

    escolha_indice = escolha_indice_limitado(chave_nome_indice_codigo_sap2)
    codigo_sap2 = [chave_nome_indice_codigo_sap2[indice] for indice in escolha_indice]

    Quadro_comparativo =comparar_indice(indices_atualizacao_monetaria, codigo_sap2,escolha_periodos)
    import io

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        Quadro_comparativo.to_excel(writer, index=False, sheet_name='Comparativo')

    # Depois de sair do bloco 'with', o Excel foi gravado no buffer
    st.download_button(
        label="📥 Baixar em Excel",
        data=buffer.getvalue(),
        file_name="quadro_comparativo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )     






