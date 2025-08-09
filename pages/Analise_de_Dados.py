# -------------- Bibliotecas ----------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# --- FUNÇÃO DE LOGOUT ---
def logout():
    st.session_state["logged_in"] = False
    st.rerun()

# --- VERIFICAÇÃO DE LOGIN ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Por favor, faça o login para acessar esta página.")
    # Adiciona um botão para voltar ao login se o usuário não estiver logado
    if st.button("Ir para Login"):
        st.switch_page("Home.py")
    st.stop()

# -------------- Carregar os dados ---------------------
@st.cache_data
def load_data():
    
    # Link para a planilha - Google Sheets
    file_url = "https://docs.google.com/spreadsheets/d/1rRQmXlVAKQocCfJy0CIsZGMJUxdMvKdI/export?format=xlsx"
    try:
        df = pd.read_excel(file_url)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

df = load_data()

# Verificar se o DataFrame está vazio
if df.empty:
    st.error("🚨 Nenhum dado disponível. Verifique se o arquivo de dados está presente e corretamente formatado.")
    st.stop()  # Interrompe a execução do aplicativo
else:
    # ------------- Caminho da logo --------------
    logo_path = "logo.png"
    imagem = Image.open(logo_path)
    st.logo(imagem)

    # ------------ Corrigir nomes de países ------------
    correcoes_de_pais = {
        "EUA": "United States",
        "Brasil": "Brazil",
        "Cabo Verde": "Cape Verde",
        "Côte d'Ivoire": "Ivory Coast"
    }

    # Corrigir os nomes dos países
    df["País de origem"] = df["País de origem"].replace(correcoes_de_pais)

    # Remover linhas com dados faltantes
    df = df.dropna(subset=["País de origem"])

    # Converter a coluna "Ano de entrada PEC-PLE" para inteiro
    df["Ano de entrada PEC-PLE"] = df["Ano de entrada PEC-PLE"].astype(int)

    # -----------Barra lateral -----------
    # Filtros
    Filtro_ano = st.sidebar.multiselect("Selecione Ano de Entrada", df["Ano de entrada PEC-PLE"].unique())
    Filtro_Pais = st.sidebar.multiselect("Selecione País(es) de Origem", df["País de origem"].unique())
    filtro_universidade = st.sidebar.multiselect("Selecione Universidade PEC-G", df["IES PEC-G"].unique())
    filtro_curso = st.sidebar.multiselect("Filtrar por Curso PEC-G", df["Curso PEC-G"].unique())
    filtro_sexo = st.sidebar.multiselect("Filtrar por Sexo", df["Sexo"].unique())

    # Filtrar dados
    filtrado_df = df.copy()

    if Filtro_ano:
        filtrado_df = filtrado_df[filtrado_df["Ano de entrada PEC-PLE"].isin(Filtro_ano)]
    if Filtro_Pais:
        filtrado_df = filtrado_df[filtrado_df["País de origem"].isin(Filtro_Pais)]
    if filtro_universidade:
        filtrado_df = filtrado_df[filtrado_df["IES PEC-G"].isin(filtro_universidade)]
    if filtro_curso:
        filtrado_df = filtrado_df[filtrado_df["Curso PEC-G"].isin(filtro_curso)]
    if filtro_sexo:
        filtrado_df = filtrado_df[filtrado_df["Sexo"].isin(filtro_sexo)]

    # Verificar se o DataFrame filtrado está vazio
    if filtrado_df.empty:
        st.warning("⚠️ Nenhum dado corresponde aos filtros selecionados. Por favor, ajuste os filtros para visualizar os dados.")
    else:
        # -------Inicio do Dashboard---------
        # Título
        st.title("📊 Análise de Dados PEC-PLE")

        # Subtítulo
        st.subheader("📋 Dados Tratados")

        # Exibir os dados 
        st.dataframe(filtrado_df)

# ------- Inicio das Métricas ---------
# Calcular a contagem de alunos por curso
contagens_cursos = filtrado_df['Curso PEC-G'].value_counts()

# Borda direita em gradiente amarelo → azul, altura fixa, e alinhamento vertical

custom_css = """
<style>
.metric-container {
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 1rem;
    border-right: 6px solid;
    border-image: linear-gradient(to bottom, yellow, blue) 1;
    background-color: #f9f9f9;
    border-radius: 10px;
    margin: 0 5px;
    box-sizing: border-box;
}
.metric-label {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}
.metric-value {
    font-size: 24px;
    color: #111;
}
</style>
"""

# ------- Analise de Dados do PEC-PLE -------
st.markdown(custom_css, unsafe_allow_html=True)

# Criar colunas para múltiplas métricas
col1, col2, col3 = st.columns(3)

# Total de Alunos
with col1:
    total_estudantes = filtrado_df.shape[0]
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total de Alunos</div>
            <div class="metric-value">{total_estudantes}</div>
        </div>
    """, unsafe_allow_html=True)

# Curso com Mais Alunos
with col2:
    top_course = contagens_cursos.idxmax()
    top_course_count = contagens_cursos.max()
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Curso com Mais Alunos: {top_course}</div>
            <div class="metric-value">{top_course_count}</div>
        </div>
    """, unsafe_allow_html=True)

# País com Mais Alunos
with col3:
    students_per_country = filtrado_df['País de origem'].value_counts()
    most_students_country = students_per_country.idxmax()
    most_students_count = students_per_country.max()
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">País com Mais Alunos: {most_students_country}</div>
            <div class="metric-value">{most_students_count}</div>
        </div>
    """, unsafe_allow_html=True)
    
    
# ------- Número de Alunos por Ano + Polígono de Frequência -------

# Garantir que os anos estejam como strings ordenáveis
filtrado_df["Ano de entrada PEC-PLE"] = filtrado_df["Ano de entrada PEC-PLE"].astype(str)

# Contagem de alunos por ano
ano_counts = filtrado_df["Ano de entrada PEC-PLE"].value_counts().sort_index()

# Criar DataFrame
df_ano = pd.DataFrame({
    "Ano": ano_counts.index,
    "Quantidade de Alunos": ano_counts.values
})

# Criar a figura combinando barra + linha
fig = go.Figure()

# Histograma (colunas)
fig.add_trace(go.Bar(
    x=df_ano["Ano"],
    y=df_ano["Quantidade de Alunos"],
    name="Frequência",
    marker_color="lightskyblue"
))

# Polígono de frequência (linha)
fig.add_trace(go.Scatter(
    x=df_ano["Ano"],
    y=df_ano["Quantidade de Alunos"],
    name="Polígono de Frequência",
    mode="lines+markers",
    line=dict(color="royalblue", width=3),
    marker=dict(size=8)
))

# Layout do gráfico
fig.update_layout(
    xaxis_title="Ano de Entrada",
    yaxis_title="Número de Alunos",
    xaxis=dict(type='category'),
    bargap=0.2
)

# Exibir no Streamlit
st.subheader("")
st.subheader("📊 Número de Alunos por Ano + Polígono de Frequência")
st.plotly_chart(fig, use_container_width=True)

# Garantir que o ano esteja no tipo string (ou inteiro ordenável)
filtrado_df["Ano de entrada PEC-PLE"] = filtrado_df["Ano de entrada PEC-PLE"].astype(str)

# Agrupar os dados por ano
ano_counts = filtrado_df["Ano de entrada PEC-PLE"].value_counts().sort_index()

# Criar DataFrame auxiliar
df_ano = pd.DataFrame({
    "Ano": ano_counts.index,
    "Quantidade de Alunos": ano_counts.values
})


# ---- Histograma - Distribuição do Curso PEC-G ----

st.subheader("🎓 Distribuição dos Cursos PEC-G")
st.write("Este gráfico exibe a quantidade de alunos por curso no programa PEC-G.")

# Agrupamento
curso_counts = filtrado_df["Curso PEC-G"].value_counts().reset_index()
curso_counts.columns = ["Curso PEC-G", "Quantidade"]

# Gráfico

top10 = curso_counts.nlargest(10, "Quantidade")

fig_top = px.bar(
    top10.sort_values("Quantidade"),
    x="Quantidade",
    y="Curso PEC-G",
    orientation="h",
    title="Top 10 Cursos com mais Alunos",
    labels={"Quantidade": "Número de Alunos", "Curso PEC-G": "Curso"},
    color_discrete_sequence=["#87CEFA"]
)

st.plotly_chart(fig_top, use_container_width=True)


# Definir uma paleta de cores fixa baseada nos países de origem
cores_paises = px.colors.qualitative.Set3  

# Criar um mapeamento fixo de cores para cada país
unique_countries = filtrado_df["País de origem"].unique()
color_map = {country: color for country, color in zip(unique_countries, cores_paises)}

# --------- Gráfico de Barras - Distribuição da Habilitação -------------
st.subheader("📊 Distribuição da Habilitação")
st.write("Este gráfico de barras mostra a quantidade de alunos em cada habilitação, facilitando a análise da distribuição entre diferentes áreas de estudo.")

# Contar o número de alunos por habilitação
habilitacao_counts = filtrado_df['Habilitação'].value_counts().reset_index()
habilitacao_counts.columns = ['Habilitação', 'Quantidade']

# Criar o gráfico de barras
fig_hab_bar = px.bar(habilitacao_counts, x='Habilitação', y='Quantidade', color='Habilitação')
st.plotly_chart(fig_hab_bar, use_container_width=True)

                                                 
# ------- Análise do Sexo dos Alunos ---------

st.markdown(custom_css, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    total_masc = filtrado_df[filtrado_df['Sexo'] == 'Masculino'].shape[0]
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total de Alunos Masculinos</div>
            <div class="metric-value">{total_masc}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    total_fem = filtrado_df[filtrado_df['Sexo'] == 'Feminino'].shape[0]
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total de Alunas Femininas</div>
            <div class="metric-value">{total_fem}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    total_na = filtrado_df[filtrado_df['Sexo'].isna()].shape[0]
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total de Alunos Outros</div>
            <div class="metric-value">{total_na}</div>
        </div>
    """, unsafe_allow_html=True)

# ----------- Gráfico de Sexo por Ano -----------
# Filtrar e preparar dados
df_sexo = filtrado_df[["Ano de entrada PEC-PLE", "Sexo"]].dropna()
df_sexo["Ano de entrada PEC-PLE"] = df_sexo["Ano de entrada PEC-PLE"].astype(int)

# Contar frequência por ano e sexo
df_contagem = df_sexo.groupby(["Ano de entrada PEC-PLE", "Sexo"]).size().reset_index(name="Contagem")

# Pivotar dados
df_pivot = df_contagem.pivot(index="Ano de entrada PEC-PLE", columns="Sexo", values="Contagem").fillna(0)
anos = df_pivot.index.tolist()

# Criar gráfico
fig = go.Figure()

# Adicionar barras empilhadas
for sexo in df_pivot.columns:
    fig.add_trace(go.Bar(
        x=anos,
        y=df_pivot[sexo],
        name=sexo,
        marker=dict(line=dict(width=0)),
    ))

# Adicionar linhas (polígono de frequência)
for sexo in df_pivot.columns:
    fig.add_trace(go.Scatter(
        x=anos,
        y=df_pivot[sexo],
        mode='lines+markers',
        name=f"{sexo} (linha)",
        line=dict(width=2, dash='dot')
    ))
st.subheader("")
st.subheader("📊 Distribuição de Sexo por Ano com Polígono de Frequência")
st.write("Este gráfico de barras exibe a quantidade de alunos masculinos e femininos por Ano de origem, permitindo uma análise da diversidade de gênero entre os participantes do programa. Criando um gráfico com linhas de polígono de frequência para melhor visualização.")
# Layout com fundo branco
fig.update_layout(
    barmode='stack',
    xaxis_title="Ano de Entrada no PEC-G",
    yaxis_title="Número de Alunos",
    plot_bgcolor="white",     # fundo do gráfico
    paper_bgcolor="white",    # fundo da área geral
    font=dict(color="black"), # cor da fonte para contraste
    legend_title="Sexo",
    xaxis=dict(tickmode='linear', dtick=1)
)

# Exibir no Streamlit
st.plotly_chart(fig, use_container_width=True)


# ------- Gráfico de Sexo por País ----------
st.subheader("📈️ Distribuição de Sexo por País")
st.write("Este gráfico de barras exibe a quantidade de alunos masculinos e femininos por país de origem, permitindo uma análise da diversidade de gênero entre os participantes do programa.")
sexo_pais_counts = filtrado_df.groupby(['País de origem', 'Sexo']).size().reset_index(name='Quantidade')
fig_sexo_pais = px.bar(sexo_pais_counts, x='País de origem', y='Quantidade', color='Sexo', barmode='group')
st.plotly_chart(fig_sexo_pais, use_container_width=True)


# --------- Gráfico de Pizza estilo Rosca ---------
st.subheader("🗺️Distribuição de Alunos por País")
st.write("Este gráfico de pizza exibe a proporção de alunos de cada país dentro do programa PEC-PLE, facilitando a análise de diversidade geográfica.")

country_counts = filtrado_df["País de origem"].value_counts().reset_index()
country_counts.columns = ["País de origem", "Quantidade"]


# Definir uma paleta de cores fixa baseada nos países de origem
fig_pizza = px.pie(country_counts, values="Quantidade", names="País de origem", hole=0.4, color="País de origem", color_discrete_map = color_map)

st.plotly_chart(fig_pizza, use_container_width=True)


# -------- Mapa Interativo -----------
st.subheader("🌍 Mapa 3D dos Países de Origem")
st.write("Este mapa interativo representa a distribuição geográfica dos alunos pelo mundo, destacando os países com maior participação no programa PEC-PLE.")

# Criar um mapa interativo
if "País de origem" in filtrado_df.columns:
    country_counts = filtrado_df.groupby("País de origem").size().reset_index(name="Quantidade")
    
    # Criar o gráfico
    fig_globe = go.Figure()

    # Adicionar dados ao mapa
    fig_globe.add_trace(go.Choropleth(
        locations=country_counts["País de origem"],
        locationmode="country names",
        z=country_counts["Quantidade"],
        colorscale="Plasma",
        marker_line_color="black",
        colorbar_title="Quantidade",
    ))

    # Personalizar o layout
    fig_globe.update_layout(
        geo=dict(
            showland=True,
            landcolor="rgb(144,238,144)",  # Verde claro para a terra
            showocean=True,
            oceancolor="rgb(17, 216, 230)",  # Azul claro para o oceano
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgb(255, 255, 255)",
            projection_type="orthographic"
        ),
        height=400,  # Aumente conforme necessário
        margin=dict(l=0, r=0, t=0, b=0),  # Remover margens para ocupar toda a área
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Exibir o Map ocupando toda a largura
    st.plotly_chart(fig_globe, use_container_width=True)

# botão de sair da sessão logada e ir para a pagina home

st.sidebar.button("Sair", on_click=logout)

