import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(page_title='Dashboard Pesquisa Pulse', page_icon=':bar_chart:', layout='wide')

# Carregar os dados
@st.cache_data  # Cache para melhorar o desempenho
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Função para limpar os nomes das colunas
def limpar_nome_coluna(nome):
    nome = nome.replace('Comunicação e Transparência: ', '')
    nome = nome.replace('Desenvolvimento e Feedback: ', '')
    nome = nome.replace('Justiça e Igualdade: ', '')
    nome = nome.replace('Ambiente e Relacionamento: ', '')
    nome = nome.replace('Satisfação Geral: ', '')
    return nome.strip()

# Carregar os DataFrames
df_pre_vendas = load_data("Pesquisa Pulse - Pré-vendas (respostas).xlsx")
df_vendas_alta_gama = load_data("Pesquisa Pulse - Vendas (Alta gama e cursos e feiras) (respostas).xlsx")
df_vendas_gestao = load_data("Pesquisa Pulse - Vendas (Gestão comercial) (respostas).xlsx")
df_vendas_inside = load_data("Pesquisa Pulse - Vendas (Inside sales e loja fisica) (respostas).xlsx")

# Widget de seleção do setor
option = st.sidebar.selectbox(
    'Selecione o Setor',
    ('Pré-vendas', 'Vendas (Alta gama e cursos e feiras)', 'Vendas (Gestão comercial)', 'Vendas (Inside sales e loja fisica)'))

# Mapear o DataFrame selecionado
if option == 'Pré-vendas':
    df_selecionado = df_pre_vendas
elif option == 'Vendas (Alta gama e cursos e feiras)':
    df_selecionado = df_vendas_alta_gama
elif option == 'Vendas (Gestão comercial)':
    df_selecionado = df_vendas_gestao
elif option == 'Vendas (Inside sales e loja fisica)':
    df_selecionado = df_vendas_inside

# Limpar os nomes das colunas do DataFrame
df_selecionado.columns = [limpar_nome_coluna(col) for col in df_selecionado.columns]

# Definir as colunas de avaliação (agora com os nomes limpos)
colunas_avaliacao = [
    'Meu gestor compartilha informações relevantes sobre o setor e a empresa.',
    'Sinto que posso me comunicar abertamente com minha liderança.',
    'Recebo feedbacks frequentes que me ajudam a melhorar.',
    'Meu gestor incentiva meu crescimento profissional.',
    'Todos são tratados de forma justa e com igualdade dentro do setor.',
    'As oportunidades são distribuídas de maneira justa.',
    'O clima organizacional dentro do setor é positivo e colaborativo.',
    'Minha liderança está aberta a ouvir sugestões e opiniões.',
]

# Função para calcular a média das respostas
def calcular_media(df, colunas):
    return df[colunas].mean().mean()

# Calcular a média geral
media_geral = calcular_media(df_selecionado, colunas_avaliacao)

# Layout do Dashboard
st.title('Dashboard de Pesquisa Pulse')

# KPIs em destaque
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Média Geral de Satisfação", value=f"{media_geral:.2f}")

# Gráfico de barras com a média de cada coluna
fig = px.bar(
    x=colunas_avaliacao,
    y=df_selecionado[colunas_avaliacao].mean().values,
    labels={'x': 'Critério', 'y': 'Média'},
    title='Média de Satisfação por Critério',
    color=colunas_avaliacao,
    color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(fig, use_container_width=True)

# Comentários Abertos
st.subheader("Comentários Abertos")
comentarios = df_selecionado['O que você acredita que sua liderança poderia melhorar para tornar seu ambiente de trabalho mais produtivo e motivador?'].dropna()
for comentario in comentarios:
    st.write(comentario)