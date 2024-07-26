#========================================================
# VISÃO - EMPRESA
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

# 1. Total de vendas (quantidade) 
def totalDeVendas(df):
    totalVendas = df['Quantidade'].sum()
    col2.metric('Total de Vendas (Quantidade)', totalVendas)

# 2. total Vendas (preco)
def totalDeVendasPreco(df):
    totalVendas = df['Preco'].sum()
    totalVendasFormatado = f"{totalVendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    col1.metric('Total de vendas por valor', f'R$ {totalVendasFormatado}')

# 3. Metricas de faturamento
def faturamentoPorCategoriaRegiao(df):
    a = df.groupby(['Categoria','Regiao']).agg({'Preco':'sum'}).reset_index()
    fig = px.bar(a, x='Categoria', y='Preco', color='Regiao',
                 pattern_shape='Regiao')
    
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='black',
        # paper_bgcolor='black',
        font=dict(color='white'),  # Ajustar a cor da fonte para melhor contraste
        title={
            'text': "Preço por Categoria x Região",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    col2.plotly_chart(fig)

# 4. Faturamento por categoria
def fatuCategoria(df):
    fig = px.bar(data_frame=df, x='Categoria', y='Preco')
    
    # Atualizar o layout para remover as linhas de grade e ajustar a visualização
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # plot_bgcolor='black',
        # paper_bgcolor='black',
        font=dict(color='white'),  # Ajustar a cor da fonte para melhor contraste
        title={
            'text': "Preço por Categoria",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    col1.plotly_chart(fig)

# 5. Tipos de pagamento mais utilizado
def pagamentosPorTipo(df):
    contagem_tipos = df['FormaPagamento'].value_counts().reset_index()
    contagem_tipos.columns = ['FormaPagamento', 'Contagem']
    
    fig = px.pie(contagem_tipos, names='FormaPagamento', values='Contagem', title='Tipos de Forma de Pagamento')

    col6.plotly_chart(fig)

# 6. Contagem de tipo de pagemento pelo tempo
def pagamentoPeloTempo(df):

    contagem_cumulativa = df.groupby(['DataCompra', 'FormaPagamento']).size().groupby(level=1).cumsum().reset_index(name='Contagem')

    # Criar o gráfico de linha com Plotly Express
    fig = px.line(contagem_cumulativa, x='DataCompra', y='Contagem', color='FormaPagamento', title='Tipos de Forma de Pagamento ao Longo do Tempo',
                labels={'DataCompra': 'Data de Compra', 'Contagem': 'Número de Vendas', 'FormaPagamento': 'Forma de Pagamento'})

    col7.plotly_chart(fig)

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
st.markdown('### EMPRESA')
st.markdown("---")
st.markdown("METRICAS")

with st.container():
    col1, col2, col3 = st.columns(3, gap='large')

    with col1:
        totalDeVendasPreco(df)

    with col2:
        totalDeVendas(df)
    
    with st.container():
        col1, col2 = st.columns(2, gap='large')

        with col1:
            faturamentoPorCategoriaRegiao(df)
        
        with col2:
            fatuCategoria(df)

    with st.container():
        st.markdown("---")
        col6, col7 = st.columns(2, gap='large')

        with col6:
            pagamentosPorTipo(df)

        with col7:
            pagamentoPeloTempo(df)
