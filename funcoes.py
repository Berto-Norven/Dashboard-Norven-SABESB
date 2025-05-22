# Bibliotecas:

import pandas as pd
import streamlit as st
import numpy as np
import matplotlib as plt
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go




# -------------------------------------------------------------------------------------------------------------------- #
def escolha_indice(df):
    with st.sidebar:
        st.markdown(
            "<h3 style='color: #550899; font-family: \"Styrene A Regular\", sans-serif;'>" "2. Selecione os índices:</h3>",
            unsafe_allow_html=True)
        st.markdown("""
                <style>
                .stMultiSelect [data-baseweb="tag"] {
                    background-color: #AC4DFF !important;
                    color: white !important;
                }
                .stMultiSelect [data-baseweb="tag"] > div {
                    color: white !important;
                }
                </style>
                """, unsafe_allow_html=True)
        escolha_indice = st.multiselect('Escolha o índice para análise:', options=list(df.keys()),default='IPCA')
    return escolha_indice

def definicao_periodo():
    with st.sidebar:
        st.markdown("<h3 style='color: #550899; font-family: \"Styrene A Regular\", sans-serif;'>1. Selecione o intervalo de datas:</h3>", unsafe_allow_html=True)
        data_inicial, data_final = None, None

        if st.checkbox("Selecionar todo o período disponível"):
            data_inicial = datetime(1995, 1, 1)
            data_final = datetime(2025, 3, 1)
        else:
            try:
                data_inicial, data_final = st.date_input(
                    "Selecione as datas",
                    value=(datetime(2015, 1, 1), datetime(2025, 3, 1)),
                    min_value=datetime(1995, 1, 1),
                    max_value=datetime(2025, 3, 1)
                )
            except:
                st.warning('⚠️ Selecione um período válido.')
                data_inicial, data_final = None, None
    return data_inicial, data_final


#Função leitura de excel:

def ler_excel(caminho,nome_aba):
    df = pd.read_excel(caminho,sheet_name = nome_aba)
    return df


def grafico_relevancia(df,col_indice,col_sap,col_relevancia):
    df.loc[df['Código SAP'] == '-', 'Código SAP'] = df['índices']

    for i in range(len(df)):
        if df.at[i, 'índices'] == df.at[i, 'Código SAP']:
            df.at[i, 'eixo_x'] = df.at[i, 'índices']
        else:
            df.at[i, 'eixo_x'] = f"{df.at[i, 'índices']}-{df.at[i, 'Código SAP']}"
    fig = px.bar(
        df,
        x = 'eixo_x',
        y = col_relevancia,
        text = col_relevancia,
        labels={col_relevancia: 'Relevância (%)', 'eixo_x': 'índice - Código SAP'},

    )
    # Ajustes de layout
    fig.update_traces(texttemplate='%{text:.1%}', textposition='outside', marker_color='#550899')
    fig.update_layout(
        xaxis_tickangle=-45,  # inclina os rótulos para melhor visualização
        yaxis_tickformat=".0%",
        height=700,  # altura mais adequada
        width=900,
        margin=dict(t=80, b=150),
        xaxis=dict(categoryorder='total descending'),
        font=dict(size=14)

    )
    return fig

def abilitar_correlação_dolar():
    st.session_state.button = not st.session_state.button


def grafico_correlação(df):
    df_variacoes_mensais = df.loc[:,df.columns.str.contains('acumulada_')]

    correlacao_indices =  df_variacoes_mensais.corr()

    fig_correlacao = px.imshow(
        correlacao_indices,
        text_auto='.2f',
        aspect='auto',
        title='Correlação entre os índices selecionados'
    )
    st.plotly_chart(fig_correlacao,use_container_width=True)

def habilitar_comparar_indices():
    st.session_state.compara_indice = not st.session_state.compara_indice


def definicao_periodos_dinamicos():
    try:
        with st.sidebar:
            st.markdown(
                "<h3 style='color: #550899; font-family: \"Styrene A Regular\", sans-serif;'>1. Selecione os intervalos de datas:</h3>",
                unsafe_allow_html=True)

            if "periodos" not in st.session_state:
                st.session_state.periodos = [(datetime(2015, 1, 1), datetime(2025, 3, 1))]

            if st.button("Adicionar novo período"):
                st.session_state.periodos.append((datetime(2015, 1, 1), datetime(2025, 3, 1)))

            if st.button("Remover último período") and len(st.session_state.periodos) > 1:
                st.session_state.periodos.pop()

            novos_periodos = []
            for i, (inicio, fim) in enumerate(st.session_state.periodos):
                st.markdown(f"**Período {i + 1}**")
                data_inicial, data_final = st.date_input(
                    f"Selecione as datas do período {i + 1}",
                    value=(inicio, fim),
                    min_value=datetime(1995, 1, 1),
                    max_value=datetime(2025, 3, 1),
                    key=f"periodo_{i}"
                )
                if data_inicial > data_final:
                    st.warning(f"⚠️ Período {i + 1} inválido.")
                novos_periodos.append((data_inicial, data_final))
    except:
        st.warning(f"⚠️ Período inválido.")
    return novos_periodos


def escolha_indice_limitado(df):
    with st.sidebar:
        st.markdown(
            "<h3 style='color: #550899; font-family: \"Styrene A Regular\", sans-serif;'>"
            "2. Selecione os índices:</h3>",
            unsafe_allow_html=True)

        st.markdown("""
            <style>
            .stMultiSelect [data-baseweb="tag"] {
                background-color: #AC4DFF !important;
                color: white !important;
            }
            .stMultiSelect [data-baseweb="tag"] > div {
                color: white !important;
            }
            </style>
            """, unsafe_allow_html=True)

        opcoes = list(df.keys())
        escolha_indice = st.multiselect(
            'Escolha no máximo **2 índices** para análise:',
            options=opcoes,
            default=['IPCA'] if 'IPCA' in opcoes else None
        )

        if len(escolha_indice) > 2:
            st.warning("Por favor, selecione no máximo 2 índices.")
            escolha_indice = escolha_indice[:2]

    return escolha_indice


def comparar_indice(df, codigo_sap, escolha_periodos):
    dfs_periodos = []
    comparativo = []

    # Etapa 1: filtrar os períodos
    for data_inicial, data_final in escolha_periodos:
        data_inicial = pd.Timestamp(data_inicial)
        data_final = pd.Timestamp(data_final)

        df_filtrado = df[['Data'] + codigo_sap].copy()
        df_filtrado = df_filtrado[(df_filtrado['Data'] >= data_inicial) & (df_filtrado['Data'] <= data_final)]
        df_filtrado = df_filtrado.sort_values('Data').reset_index(drop=True)

        dfs_periodos.append(df_filtrado)

    # Etapa 2: calcular variações e montar quadro comparativo
    for idx, dfg in enumerate(dfs_periodos):
        try:
            linha = {
                "Período": f"{escolha_periodos[idx][0].strftime('%Y-%m-%d')} a {escolha_periodos[idx][1].strftime('%Y-%m-%d')}"
            }
            valores_finais = {}

            for coluna in codigo_sap:
                fator_acumulado = 1

                if coluna == 'INCC':
                    dfg[f'Variação % Mensal_{coluna}'] = dfg[coluna]
                    dfg = dfg.drop(columns=coluna)
                    dfg[f'Variação % acumulada_{coluna}'] = 0
                    inicio = dfg[f'Variação % Mensal_{coluna}'].first_valid_index()
                else:
                    dfg[f'Variação % Mensal_{coluna}'] = dfg[coluna].pct_change() * 100
                    dfg[f'Variação % acumulada_{coluna}'] = 0
                    inicio = dfg[f'Variação % Mensal_{coluna}'].first_valid_index()

                if inicio is not None:
                    for i in range(inicio, len(dfg)):
                        valor = dfg.loc[i, f'Variação % Mensal_{coluna}']
                        if pd.notna(valor):
                            fator_variacao = 1 + (valor / 100)
                            fator_acumulado *= fator_variacao
                            dfg.loc[i, f'Variação % acumulada_{coluna}'] = (fator_acumulado - 1) * 100

                # Pega último valor acumulado
                ultimo_valor = dfg[f'Variação % acumulada_{coluna}'].dropna().iloc[-1]
                valores_finais[coluna] = ultimo_valor
                linha[f'Acumulado final no período - índice: {coluna} (%)'] = round(ultimo_valor, 2)

            # Diferenças
            if len(codigo_sap) == 2:
                idx1, idx2 = codigo_sap
                val1 = valores_finais[idx1]
                val2 = valores_finais[idx2]
                diff_abs = val1 - val2
                diff_pct = abs((diff_abs / val2) * 100) if val2 != 0 else None

                linha[f'Diferença Absoluta ({idx1} - {idx2}) (%)'] = f"{round(diff_abs, 2)}%"
                linha[f'Diferença Absoluta ({idx1} - {idx2}) (%)'] = linha[f'Diferença Absoluta ({idx1} - {idx2}) (%)'].replace(".",",")
                linha[f'Diferença Relativa ({idx1} - {idx2}) (%)'] = f"{round(diff_pct, 2)}%" if diff_pct is not None else None
                linha[f'Diferença Relativa ({idx1} - {idx2}) (%)'] = linha[f'Diferença Relativa ({idx1} - {idx2}) (%)'].replace(".",",")

            comparativo.append(linha)
            dfs_periodos[idx] = dfg  # atualiza com as colunas calculadas

        except Exception as e:
            st.warning(f'⚠️ Não foi possível calcular para o período {idx + 1}: {e}')

    # Mostra o comparativo
    df_comparativo = pd.DataFrame(comparativo)
    st.markdown("### 🔎 Quadro Comparativo dos Índices por Período")
    st.dataframe(df_comparativo, use_container_width=True,hide_index=True)
    return df_comparativo






def plotar_indice(df,codigo_sap,data_inicial,data_final):

    if 'button' not in st.session_state:
        st.session_state.button = False
    with st.sidebar:
        st.button('Realizar correlção com Dólar', on_click=abilitar_correlação_dolar)
    if st.session_state.button:
        codigo_sap =codigo_sap +['Dólar']
        df = df[['Data'] + codigo_sap]
    else:
        df = df[['Data'] + codigo_sap]
    data_inicial = pd.Timestamp(data_inicial)
    data_final = pd.Timestamp(data_final)
    df =  df[['Data']+codigo_sap]
    try:
        df = df[(df['Data']>= data_inicial) & (df['Data']<= data_final)]
        df = df.sort_values('Data').reset_index()
        for coluna in codigo_sap:
            fator_acumulado = 1
            if coluna == 'INCC':
                df[f'Variação % Mensal_{coluna}'] = df[coluna]
                df = df.drop(columns=coluna)
                df[f'Variação % acumulada_{coluna}'] = 0
                inicio = df[f'Variação % Mensal_{coluna}'].first_valid_index()


            else:
                df[f'Variação % Mensal_{coluna}'] = df[coluna].pct_change() * 100

                df[f'Variação % acumulada_{coluna}'] = 0
                inicio = df[f'Variação % Mensal_{coluna}'].first_valid_index()

            if inicio is not None:
                for i in range(inicio, len(df)):
                    valor = df.loc[i, f'Variação % Mensal_{coluna}']
                    if pd.notna(valor):
                        fator_variacao = 1 + (valor / 100)
                        fator_acumulado *= fator_variacao
                        df.loc[i, f'Variação % acumulada_{coluna}'] = (fator_acumulado - 1) * 100



        fig_acumulada = go.Figure()

        for coluna in codigo_sap:
            fig_acumulada.add_trace(go.Scatter(
                x=df['Data'],
                y=df[f'Variação % acumulada_{coluna}'],
                mode='lines+markers',
                name=f'{coluna} - Acumulado'
            ))
        fig_acumulada.update_traces(texttemplate='%{text:.1%}')
        fig_acumulada.update_layout(
            #title='Variação Acumulada por Índice',
            xaxis_title='Data',
            yaxis_title='Variação % Acumulada (%)',
            legend_title='Índices',
            hovermode='x unified',
            yaxis=dict(
                ticksuffix='%',
                tickformat='.2f'


            )
        )
        df = df.drop(columns=['index'])
        with st.container():
            st.subheader("Gráfico de Variação Acumulada")
            st.plotly_chart(fig_acumulada, use_container_width=True)
            st.subheader('Tabela de índices')
            st.dataframe(df, hide_index=True, use_container_width=True)
            grafico_correlação(df)

    except:
        st.warning('⚠️ não existem dados suficientes para o período selecionado.')

def descritivo_especifico(caminho, codigo_aba, indice=0):
associa_aba_abreviação = {
        "IPCA": "IPCA",
        "INCC": "INCC",
        "INPC": "INPC",
        "IGP-M": "IGP-M",
        "IGP-DI": "IGP-DI",
        "787": "Met. Básica",
        "877": "Máqs. e Equip.",
        "855": "Equip. Elétricos",
        "757": "Tubos Plásticos",
        "756": "Conexões Plásticas",
        "803": "Tubos Fe/Aço",
        "805": "Conex. Fe/Aço",
        "878": "Mot./Bomb./Comp.",
        "643": "Madeira e Deriv.",
        "741": "Borracha/Plástico",
        "749": "Prod. Plásticos",
        "774": "Art. Cimento/Concreto",
        "815": "Peças Fe Fundido",
        "881": "Bombas Hidrául.",
        "882": "Valv./Torneiras./Reg.",
        "835": "Equip.Informática",
        "IPC-FIPE": "IPC-FIPE"


    }
    try:

        # Lê os DataFrames das abas selecionadas
        dfs = {
            aba: ler_excel(caminho, aba)
            .drop(columns=['Índice'])
            .rename(columns={'Última Atualização': "Periodicidade de Atualização"})
            .assign(**{"Periodicidade de Atualização": "Mensal"})
            for aba in codigo_aba
        }

        # Pega os nomes das colunas da primeira aba (assumindo todas iguais)
        colunas = dfs[codigo_aba[0]].columns[:12]  # pega no máximo 12

        # Cria a matriz 3x4 de containers
        rows = [st.columns(4) for _ in range(3)]
        flat_containers = [col for row in rows for col in row]

        for i, coluna in enumerate(colunas):
            with flat_containers[i]:
                with st.container(height=200):
                    st.markdown(f"**{coluna}**")  # título da coluna

                    # Mostra uma linha por aba selecionada com formatação HTML
                    for aba in codigo_aba:
                        valor = dfs[aba].at[indice, coluna]
                        if valor == '-':
                            st.markdown(
                                """
                                <div style="padding: 8px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 8px; text-align: center;">
                                    Não se Aplica
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            desc = associa_aba_abreviação[aba]
                            st.markdown(
                                f"""
                                <div style="padding: 8px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 8px;">
                                    <strong>{desc}:</strong> {valor}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
    except:
        st.warning("Selecione um índice")






