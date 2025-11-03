import pandas as pd
import streamlit as st
import plotly.express as px
import os

# --- Configuração da Página ---
# Usamos 'wide' para que o dashboard ocupe a tela inteira
st.set_page_config(layout="wide")

# --- Título do Dashboard ---
st.title("Dashboard de Performance de Marketing Digital 📈")

# --- Carregamento dos Dados ---
# O streamlit "enxerga" a partir de onde ele foi executado (a pasta projeto_marketing_etl/)
DATA_FILE = os.path.join('data_clean', 'marketing_consolidado.csv')

# Usamos uma função com @st.cache_data para o Streamlit não recarregar
# o CSV toda vez que mexermos em um filtro.
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv(DATA_FILE)
        # Convertemos a coluna 'data' para datetime (IMPORTANTE)
        df['data'] = pd.to_datetime(df['data'])
        return df
    except FileNotFoundError:
        st.error(f"Arquivo de dados não encontrado em '{DATA_FILE}'.")
        st.info("Por favor, execute o script 'scripts/etl_pipeline.py' primeiro para gerar os dados limpos.")
        return None

df = carregar_dados()

# Se os dados não foram carregados, interrompe a execução
if df is None:
    st.stop()

# --- Barra Lateral de Filtros (Sidebar) ---
st.sidebar.header("Filtros Interativos")

# Filtro 1: Seleção de Plataforma (Multiselect)
# Pegamos as plataformas únicas do dataframe
plataformas_disponiveis = df['plataforma'].unique()
plataformas_selecionadas = st.sidebar.multiselect(
    "Selecione as Plataformas:",
    options=plataformas_disponiveis,
    default=plataformas_disponiveis # Começa com todas selecionadas
)

# Filtro 2: Filtro de Data (Date Range)
data_min = df['data'].min()
data_max = df['data'].max()

filtro_data = st.sidebar.date_input(
    "Selecione o Período:",
    value=(data_min, data_max), # Começa com o período completo
    min_value=data_min,
    max_value=data_max
)

# --- Filtrando o DataFrame ---
# O 'df_filtrado' será usado para todos os nossos gráficos e métricas
# É assim que o dashboard se torna interativo

# 1. Tratamento do filtro de data (para evitar erro se for tupla de 1 elemento)
if len(filtro_data) == 2:
    start_date, end_date = filtro_data
else:
    start_date, end_date = filtro_data[0], filtro_data[0] # Caso de data única

# 2. Aplicando os filtros
df_filtrado = df[
    (df['plataforma'].isin(plataformas_selecionadas)) &
    (df['data'] >= pd.to_datetime(start_date)) &
    (df['data'] <= pd.to_datetime(end_date))
]

# --- Exibição de Métricas (KPIs) ---
st.header("Visão Geral dos KPIs")

# Calculando os KPIs com base no dataframe filtrado
custo_total = df_filtrado['custo'].sum()
cliques_totais = df_filtrado['cliques'].sum()
impressoes_totais = df_filtrado['impressoes'].sum()

# Cálculos de média (com cuidado para evitar divisão por zero)
cpc_medio = (custo_total / cliques_totais) if cliques_totais > 0 else 0
cpm_medio = (custo_total / impressoes_totais) * 1000 if impressoes_totais > 0 else 0

# Exibindo os KPIs em colunas
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Custo Total", f"R$ {custo_total:,.2f}")
col2.metric("Cliques Totais", f"{cliques_totais:,}")
col3.metric("Impressões Totais", f"{impressoes_totais:,}")
col4.metric("CPC Médio", f"R$ {cpc_medio:,.2f}")
col5.metric("CPM Médio", f"R$ {cpm_medio:,.2f}")

st.markdown("---") # Linha divisória

# --- Gráficos Interativos (com Plotly) ---
st.header("Análises Visuais")

# Dividir a área de gráficos em duas colunas
col_graf1, col_graf2 = st.columns(2)

# Gráfico 1: Custo ao Longo do Tempo (por plataforma)
with col_graf1:
    st.subheader("Custo ao Longo do Tempo")
    # Agrupamos por data e plataforma para a série temporal
    df_temporal = df_filtrado.groupby(['data', 'plataforma'])['custo'].sum().reset_index()
    
    fig_temporal = px.line(
        df_temporal,
        x='data',
        y='custo',
        color='plataforma', # Uma linha para cada plataforma
        title="Evolução do Custo Diário"
    )
    st.plotly_chart(fig_temporal, use_container_width=True)

# Gráfico 2: Custo Total por Plataforma
with col_graf2:
    st.subheader("Distribuição de Custo")
    df_custo_plataforma = df_filtrado.groupby('plataforma')['custo'].sum().reset_index()
    
    fig_pie_custo = px.pie(
        df_custo_plataforma,
        names='plataforma',
        values='custo',
        title="Custo Total por Plataforma (%)",
        hole=.3 # Gráfico de "donut"
    )
    st.plotly_chart(fig_pie_custo, use_container_width=True)

# Gráfico 3: Análise de CPC vs CPM
st.subheader("Análise de Eficiência (CPC vs CPM)")
# Usamos 'hover_data' para mostrar mais infos ao passar o mouse
fig_scatter = px.scatter(
    df_filtrado,
    x='cpc',
    y='cpm',
    color='plataforma',
    size='custo', # O tamanho da bola representa o custo
    title="Eficiência de Custo por Plataforma",
    hover_data=['data', 'cliques', 'impressoes']
)
st.plotly_chart(fig_scatter, use_container_width=True)


# --- Tabela de Dados Brutos (Filtrados) ---
st.header("Explore os Dados Detalhados")
st.dataframe(df_filtrado)
