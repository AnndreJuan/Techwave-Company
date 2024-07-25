#========================================================
# VISÃO - ENTREGADORES
#========================================================

#========================================================
# Bibliotecas necessárias
#========================================================
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

#========================================================
# Importando dataframe
#========================================================
df1 = pd.read_csv(r'dataset/techwave.csv', sep=',')
df = df1.copy()

#========================================================
# Função para limpar dataframe
#========================================================
def clear_data(df):
    df = df.astype(str)  # Transformando dataframe em string
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Removendo espaços de todo o dataframe

    # Convertendo colunas para int
    df['Nota'] = df['Nota'].astype(int)
    df['Quantidade'] = df['Quantidade'].astype(int)

    # Convertendo colunas para float
    df['Preco'] = df['Preco'].astype(float)
    df['Desconto'] = df['Desconto'].astype(float)

    # Converter a coluna de data para datetime, especificando o formato
    df['DataCompra'] = pd.to_datetime(df['DataCompra'], format='%d/%m/%Y')

    return df

#========================================================
# Limpando dataframe
#========================================================
df = clear_data(df)

#========================================================
# Funções de análises de dados
#========================================================

# METRICAS
# 1. Maior e Menor idade
def Idade(df):
    maiorIdade = df['Idade'].max()
    menorIdade = df['Idade'].min()
    col1.metric('Maior Idade', maiorIdade)
    col2.metric('Menor Idade', menorIdade)
    
# 2. Maior e Menor nota
def Nota(df):
    maiorNota = df['Nota'].max()
    menorNota = df['Nota'].min()
    col3.metric('Maior Nota', maiorNota)
    col4.metric('Menor Nota', menorNota)
    
# 3. Quantidade de Produtos → grafico de coluna
def QauntidadeProdColumn(df):
    a = df['Produto'].value_counts().reset_index()
    a.rename(columns={'count':'Quantidade'}, inplace=True)
    fig = px.bar(data_frame=a, x='Produto', y='Quantidade')
    col1.plotly_chart(fig)

# 3. Produtos por cidade
def produtosPorCidade(df):
    a = df.groupby(['Categoria', 'Regiao']).size().reset_index(name='Count')
    fig = px.sunburst(a, path=['Categoria', 'Regiao'], values='Count',
                      title='Distribuição de Subcategorias de Produtos por Cidade',
                      color_continuous_scale=px.colors.qualitative.Plotly)

    col2.plotly_chart(fig)

#======================================================================================================================
# Configuração da barra lateral
#======================================================================================================================

# 4. Adicionando logo
image = Image.open('Techwave.png')
st.sidebar.image(image, width=250)

# 5. Filtro de região
regiao = st.sidebar.multiselect('Filtro de Região', ['Norte','Nordeste','Sul','Sudeste','Centro-Oeste'], default=['Norte','Nordeste','Sul','Sudeste','Centro-Oeste'])
linhas_selecionadas = df['Regiao'].isin(regiao)
df = df.loc[linhas_selecionadas, :]

# 6. Filtro de categoria
categoria = st.sidebar.multiselect('Filtro de Categoria', ['Redes','Eletrônicos','Segurança','Automação','Informática','Robótica'], default=['Redes','Eletrônicos','Segurança','Automação','Informática','Robótica'])
linhas_selecionadas = df['Categoria'].isin(categoria)
df = df.loc[linhas_selecionadas, :]

# 6. Período de compra
data_inicio = df['DataCompra'].min()
data_fim = df['DataCompra'].max()

# Configurar o slider para selecionar a data de compra
data_compra = st.sidebar.slider(
    'Selecione o período de Data de Compra',
    min_value=data_inicio.date(),
    max_value=data_fim.date(),
    value=(data_inicio.date(), data_fim.date()),
    format='DD-MM-YYYY'
)

# Converter as datas do slider para datetime
data_compra = (pd.to_datetime(data_compra[0]), pd.to_datetime(data_compra[1]))

# Filtrar o dataframe com base no intervalo de datas selecionado
df = df[(df['DataCompra'] >= data_compra[0]) & (df['DataCompra'] <= data_compra[1])]

# 7. Adicionando criador
st.sidebar.markdown('#### Create by Anndre Juan')

#======================================================================================================================
# Layout Streamlit
#======================================================================================================================
st.markdown('### PRODUTOS')
st.markdown("---")
st.markdown('### Métricas')

with st.container():
    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1, col2:
        Idade(df)
    
    with col3, col4:
        Nota(df)

    st.markdown("---")
    st.markdown("### Avaliações")

    with st.container():
        col1, col2  = st.columns(2, gap='large')

        with col1:
            QauntidadeProdColumn(df)

        with col2:
            produtosPorCidade(df)
