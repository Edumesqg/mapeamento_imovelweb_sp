import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

# Configurações gerais do Streamlit
st.set_page_config(
    page_title="Análise de Imóveis - São Paulo",
    layout="wide",
)

# Carregar a base de dados
data = pd.read_csv('data_mapa.csv')

# ---------------------------
# EXPLORAÇÃO INICIAL DOS DADOS
# ---------------------------
st.title("Análise Interativa de Imóveis na Região Central de São Paulo")
st.markdown("""
Este é um relatório interativo criado em [Streamlit](https://streamlit.io/) para explorar dados de apartamentos disponíveis no centro de São Paulo, obtidos via web scraping (ImovelWeb).  
O objetivo é visualizar a distribuição de preços, correlacionar variáveis, mapear a localização e criar filtros interativos para que o usuário possa refinar sua busca.
""")

st.markdown("""
Na estruturação do relatório, desenvolvemos um projeto com 3 etapas, sendo elas:
- Desenvolvimento de um Scraper para captura de dados de imóveis disponíveis no centro de São Paulo na plataforma ImovelWeb, código para edição disponível em: [Edumesqg Scraper-Imovelweb-](https://github.com/Edumesqg/Scraper-Imovelweb-)
- Tratamento dos dados capturados, removendo duplicatas e convertendo os tipos de dados para inteiros, e utilizando a integração com a API do Google Maps para captura das latitudes e longitudes de cada imóvel. Código disponível em: [https://github.com/Edumesqg/geo-mapeamento-imovelweb]
- Criação e desenvolvimento deste relatório.

Esse relatório tem como objetivo mostrar o poder da avaliação de dados no nosso dia a dia.
""")

st.subheader("Visão Geral dos Dados")

# Mostrar algumas linhas iniciais
st.write("**Amostra dos Dados:**")
st.dataframe(data.head())

# Informações gerais
st.write("**Informações do DataFrame:**")
buffer_info = []
buffer_info.append("Número de linhas: {}".format(data.shape[0]))
buffer_info.append("Número de colunas: {}".format(data.shape[1]))
st.write("\n".join(buffer_info))

# Descrever dados numéricos
st.write("**Estatísticas Descritivas:**")
st.write(data.describe())

st.markdown("""
A partir da visualização geral da base de dados, conseguimos trabalhar no desenvolvimento de um relatório que nos permitirá entender melhor como são distribuídos os aluguéis de imóveis no centro de São Paulo.
""")

# Remover duplicatas
data = data.drop_duplicates()

# ---------------------------
# ANÁLISE EXPLORATÓRIA INICIAL
# ---------------------------

st.subheader("Distribuição de Preços dos Imóveis")

# Verificar colunas necessárias
if 'aluguel_num' not in data.columns:
    st.error("A coluna 'aluguel_num' não existe no DataFrame.")
    st.stop()
if 'bairro' not in data.columns:
    st.error("A coluna 'bairro' não existe no DataFrame.")
    st.stop()

# Histograma de preços
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data['aluguel_num'], bins=30, kde=True, ax=ax)
ax.set_title('Distribuição dos Preços dos Imóveis')
ax.set_xlabel('Preço')
ax.set_ylabel('Frequência')
st.pyplot(fig)

# Boxplot dos preços por bairro
st.subheader("Boxplot de Preços por Bairro")

# Ordenar os bairros pela mediana dos preços
bairros_ordenados = data.groupby(
    'bairro')['aluguel_num'].median().sort_values().index

# Criar o boxplot com melhorias visuais
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.boxplot(
    x='aluguel_num',
    y='bairro',
    data=data,
    order=bairros_ordenados,
    palette="coolwarm",
    ax=ax2
)

ax2.set_title('Distribuição de Preços de Aluguel por Bairro', fontsize=16)
ax2.set_xlabel('Preço', fontsize=14)
ax2.set_ylabel('Bairro', fontsize=14)
ax2.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()
st.pyplot(fig2)

# Mapa de calor das correlações
st.subheader("Mapa de Calor das Correlações")
numeric_data = data.select_dtypes(include=[float, int])

fig3, ax3 = plt.subplots(figsize=(10, 8))
sns.heatmap(numeric_data.corr(), annot=True,
            cmap='coolwarm', linewidths=0.5, ax=ax3)
ax3.set_title('Mapa de Calor das Correlações')
st.pyplot(fig3)

# ---------------------------
# CRIAÇÃO DO MAPA INTERATIVO
# ---------------------------

# Criar um GeoDataFrame
gdf = gpd.GeoDataFrame(
    data, geometry=[Point(xy)
                    for xy in zip(data['longitude'], data['latitude'])]
)
gdf.set_crs(epsg=4326, inplace=True)


def criar_mapa(df):
    # Criar um mapa centralizado no centro de São Paulo
    m = folium.Map(location=[-23.550559, -46.633347], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        popup_content = f"""
        <b>Área:</b> {row['area']} m²<br>
        <b>Quartos:</b> {row['quartos']}<br>
        <b>Banheiros:</b> {row['banheiros']}<br>
        <b>Vaga:</b> {row['vaga']}<br>
        <b>Aluguel:</b> R$ {row['aluguel']}<br>
        <b>Condomínio:</b> R$ {row['condominio']}
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_content
        ).add_to(marker_cluster)

    # Adicionar mapa de calor baseado no preço do aluguel
    heat_data = df[['latitude', 'longitude', 'aluguel_num']].values.tolist()
    HeatMap(heat_data, radius=15, gradient={
            0.4: 'blue', 0.65: 'lime', 1: 'red'}, name="Mapa de Calor").add_to(m)

    return m

# ---------------------------
# FILTROS INTERATIVOS
# ---------------------------


st.subheader("Filtragem Interativa")
st.markdown("Use os controles na **barra lateral** para filtrar os imóveis e visualizar apenas as opções de interesse no mapa.")

st.sidebar.header("Parâmetros de Filtro:")

# Definir valores máximos para os sliders com base nos dados
max_area = int(data['area'].max()) if 'area' in data.columns else 1000
max_quartos = int(data['quartos'].max()) if 'quartos' in data.columns else 10
max_banheiros = int(data['banheiros'].max()
                    ) if 'banheiros' in data.columns else 10
max_vaga = int(data['vaga'].max()) if 'vaga' in data.columns else 10
max_aluguel = int(data['aluguel_num'].max()
                  ) if 'aluguel_num' in data.columns else 10000

area_min, area_max = st.sidebar.slider(
    "Área (m²):", 0, max_area, (0, max_area))
quartos_min, quartos_max = st.sidebar.slider(
    "Quartos:", 0, max_quartos, (0, max_quartos))
banheiros_min, banheiros_max = st.sidebar.slider(
    "Banheiros:", 0, max_banheiros, (0, max_banheiros))
vaga_min, vaga_max = st.sidebar.slider("Vagas:", 0, max_vaga, (0, max_vaga))
aluguel_min, aluguel_max = st.sidebar.slider(
    "Aluguel (R$):", 0, max_aluguel, (0, max_aluguel), step=100)

# Aplicar filtros
filtered_data = data[
    (data['area'] >= area_min) & (data['area'] <= area_max) &
    (data['quartos'] >= quartos_min) & (data['quartos'] <= quartos_max) &
    (data['banheiros'] >= banheiros_min) & (data['banheiros'] <= banheiros_max) &
    (data['vaga'] >= vaga_min) & (data['vaga'] <= vaga_max) &
    (data['aluguel_num'] >= aluguel_min) & (data['aluguel_num'] <= aluguel_max)
]

st.write(f"Foram encontrados {len(filtered_data)
                              } imóveis com os critérios selecionados.")

m = criar_mapa(filtered_data)
st_folium(m, width=1000, height=600)

st.markdown("""
Com essa avaliação, conseguimos entender um pouco mais sobre a distribuição dos imóveis.  
Aproveite que os dados são reais e estão atualizados em Dezembro de 2024.  
Um ponto interessante é que podemos usar este estudo para mapear o crescimento de imóveis na região central de São Paulo e a mudança dos preços ao longo do tempo, futuramente.
""")

# Rodapé formatado
st.markdown("""
---
**Desenvolvido por:** [Eduardo Mesquita Gomes](https://www.linkedin.com/in/engeduardomesquita/)  
**Contato:** (21) 98319-9660 | eduardo_mesq@outlook.com
""")
