import streamlit as st
from PIL import Image

# 1. Configurando página inicial
st.set_page_config(page_title="Home", layout='wide')

# 2. Adicionando logo
image = Image.open('Techwave.png')
st.sidebar.image(image, width=250)

# 3. Adicionando criador
st.sidebar.markdown('#### Create by Anndre Juan')

st.write('# Techwave Company Dashboard')

st.markdown("""

## Visão de Produtos:
- Distribuição de Categorias de Produtos: Frequência de vendas para cada categoria de produto.
- Avaliações de Produtos: Média das avaliações dos clientes para cada categoria de produto.
## Visão da Empresa:
- Resumo de Vendas: Total de vendas por categoria de produto.
- Total de desconto aplicado: Resumo dos descontos aplicados aos produtos.
- Análise por região: Analisar regionalmente os valores de faturamento e distribuição dos valores.
         
#### Ask for Help - @AnndreJuan
""")