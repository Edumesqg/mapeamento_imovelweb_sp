# Aplicativo Avaliação de Dados Imóveis São Paulo

## 📊 Descrição
O **Aplicativo Avaliação de Dados Imóveis São Paulo** é uma ferramenta interativa desenvolvida com **Streamlit** para análise e visualização de dados de apartamentos disponíveis para aluguel na região central de São Paulo. Utilizando técnicas de web scraping na plataforma **ImovelWeb**, o aplicativo permite aos usuários explorar a distribuição de preços, correlações entre variáveis e a localização geográfica dos imóveis através de mapas interativos.

## 🛠️ Funcionalidades
- **Visualização de Dados**: Exibição de amostras dos dados, informações gerais, estatísticas descritivas e verificação de valores nulos.
- **Análise Exploratória**: Histograma da distribuição de preços, boxplots por bairro e mapa de calor das correlações entre variáveis.
- **Mapas Interativos**: Mapa com marcadores e mapa de calor utilizando **Folium** para visualizar a localização e preços dos imóveis.
- **Filtros Interativos**: Barra lateral com sliders para filtrar imóveis por área, número de quartos, banheiros, vagas e preço do aluguel.
- **Atualizações em Tempo Real**: O mapa e as visualizações são atualizados conforme os filtros são ajustados.
- **Interface Intuitiva**: Design responsivo e amigável, facilitando a navegação e a interpretação dos dados.

## 📁 Estrutura do Projeto
```
analise-imoveis-sao-paulo/
├── app.py
├── data_mapa.csv
├── requirements.txt
├── README.md
└── screenshots/
    ├── dashboard.png
    └── mapa_interativo.png
```
- **app.py**: Script principal do aplicativo Streamlit.
- **data_mapa.csv**: Arquivo CSV contendo os dados dos imóveis.
- **requirements.txt**: Lista de dependências necessárias para executar o aplicativo.
- **README.md**: Este arquivo de documentação.
- **screenshots/**: Pasta contendo capturas de tela do aplicativo.

## 🚀 Como Usar

### 1. Clone o Repositório
```bash
git clone https://github.com/Edumesqg/analise-imoveis-sao-paulo.git
cd analise-imoveis-sao-paulo
```

### 2. Instale as Dependências
Certifique-se de ter o **Python** instalado. Recomenda-se utilizar um ambiente virtual.

```bash
pip install -r requirements.txt
```

### 3. Execute o Aplicativo
```bash
streamlit run app.py
```
O aplicativo será iniciado localmente e acessível no seu navegador, geralmente em [http://localhost:8501](http://localhost:8501).

## ☁️ Implantção Online
O aplicativo foi implantado utilizando o **Streamlit Cloud**, tornando-o acessível a qualquer pessoa com o link de acesso.

**Acesse o Aplicativo Online**: Aplicativo Avaliação de Dados Imóveis São Paulo

## 🔧 Desenvolvimento

### Tecnologias Utilizadas
- **Python**: Linguagem de programação principal.
- **Streamlit**: Framework para criação de aplicativos web interativos.
- **Pandas**: Manipulação e análise de dados.
- **Matplotlib & Seaborn**: Visualização de dados.
- **Geopandas & Shapely**: Manipulação de dados geoespaciais.
- **Folium**: Criação de mapas interativos.
- **Streamlit-Folium**: Integração de mapas Folium com Streamlit.

### Etapas do Projeto

#### Desenvolvimento do Scraper:
- Captura de dados de imóveis disponíveis no centro de São Paulo na plataforma **ImovelWeb**.
- Simulação de comportamento humano com atrasos e configurações manuais de CAPTCHA.
- Armazenamento dos dados em arquivos CSV.

#### Tratamento dos Dados:
- Remoção de duplicatas.
- Conversão de tipos de dados para inteiros.
- Integração com a API do Google Maps para captura de latitudes e longitudes.

#### Desenvolvimento do Relatório:
- Criação de visualizações interativas.
- Implementação de filtros para refinar a busca.
- Integração de mapas interativos para localização dos imóveis.

## 📫 Contato
**Eduardo Mesquita Gomes**
- **Telefone**: (21) 98319-9660
- **Email**: eduardo_mesq@outlook.com
- **LinkedIn**: [linkedin.com/in/engeduardomesquita](https://www.linkedin.com/in/engeduardomesquita)

## 📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

