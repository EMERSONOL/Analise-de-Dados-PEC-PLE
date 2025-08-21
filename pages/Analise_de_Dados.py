import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ======================================================================
# (1) Função de Logout
# ======================================================================
def logout():
    st.session_state["logged_in"] = False
    st.rerun()

# ======================================================================
# (2) Verificação de Login
# ======================================================================
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Por favor, faça o login para acessar esta página.")
    st.switch_page("Home.py")
    st.stop()

# ======================================================================
# (3) Carregar Dados
# ======================================================================
@st.cache_data
def load_data():
    file_url = "https://docs.google.com/spreadsheets/d/1rRQmXlVAKQocCfJy0CIsZGMJUxdMvKdI/export?format=xlsx"
    try:
        df = pd.read_excel(file_url)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("🚨 Nenhum dado disponível. Verifique se o arquivo de dados está presente e corretamente formatado.")
    st.stop()

# ======================================================================
# (4) Logo e Correções de Países
# ======================================================================
try:
    logo_path = r"logo.png"
    imagem = Image.open(logo_path)
    st.logo(imagem)
except Exception:
    st.warning("⚠️ Logo não encontrada.")

correcoes_de_pais = {
    "EUA": "United States",
    "Brasil": "Brazil",
    "Cabo Verde": "Cape Verde",
    "Côte d'Ivoire": "Ivory Coast"
}
df["País de origem"] = df["País de origem"].replace(correcoes_de_pais)
df = df.dropna(subset=["País de origem"])
df["Ano de entrada PEC-PLE"] = df["Ano de entrada PEC-PLE"].astype(int)

# ======================================================================
# (5) Filtros na Barra Lateral
# ======================================================================
Filtro_ano = st.sidebar.multiselect("Selecione Ano de Entrada", df["Ano de entrada PEC-PLE"].unique())
Filtro_Pais = st.sidebar.multiselect("Selecione País(es) de Origem", df["País de origem"].unique())
filtro_universidade = st.sidebar.multiselect("Selecione Universidade PEC-G", df["IES PEC-G"].unique())
filtro_curso = st.sidebar.multiselect("Filtrar por Curso PEC-G", df["Curso PEC-G"].unique())
filtro_sexo = st.sidebar.multiselect("Filtrar por Sexo", df["Sexo"].unique())

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

if filtrado_df.empty:
    st.warning("⚠️ Nenhum dado corresponde aos filtros selecionados. Por favor, ajuste os filtros para visualizar os dados.")
    st.stop()

# ======================================================================
# (6) Dashboard - Dados Gerais
# ======================================================================
st.title("📊 Análise de Dados PEC-PLE")
st.subheader("📋 Dados Tratados")
st.dataframe(filtrado_df)

# ======================================================================
# (7) Métricas Resumidas
# ======================================================================
contagens_cursos = filtrado_df['Curso PEC-G'].value_counts()

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
st.markdown(custom_css, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    total_estudantes = filtrado_df.shape[0]
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Total de Alunos</div>
            <div class="metric-value">{total_estudantes}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if not contagens_cursos.empty:
        top_course = contagens_cursos.idxmax()
        top_course_count = contagens_cursos.max()
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Curso com Mais Alunos: {top_course}</div>
                <div class="metric-value">{top_course_count}</div>
            </div>
        """, unsafe_allow_html=True)

with col3:
    students_per_country = filtrado_df['País de origem'].value_counts()
    if not students_per_country.empty:
        most_students_country = students_per_country.idxmax()
        most_students_count = students_per_country.max()
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">País com Mais Alunos: {most_students_country}</div>
                <div class="metric-value">{most_students_count}</div>
            </div>
        """, unsafe_allow_html=True)

# ======================================================================
# (8) Evolução Temporal por País
# ======================================================================
if "Ano de entrada PEC-PLE" in filtrado_df.columns and "País de origem" in filtrado_df.columns:
    df_pecg = filtrado_df[["Ano de entrada PEC-PLE", "País de origem"]].dropna()
    if not df_pecg.empty:
        df_pecg["Ano de entrada PEC-PLE"] = df_pecg["Ano de entrada PEC-PLE"].astype(int)
        df_grouped = df_pecg.groupby(["Ano de entrada PEC-PLE", "País de origem"]).size().reset_index(name="Quantidade")

        if not df_grouped.empty:
            todos_anos = range(df_grouped["Ano de entrada PEC-PLE"].min(), df_grouped["Ano de entrada PEC-PLE"].max() + 1)
            todos_paises = df_grouped["País de origem"].unique()

            df_grid = pd.MultiIndex.from_product([todos_anos, todos_paises], names=["Ano de entrada PEC-PLE", "País de origem"]).to_frame(index=False)

            df_completo = pd.merge(df_grid, df_grouped, how="left", on=["Ano de entrada PEC-PLE", "País de origem"])
            df_completo["Quantidade"] = df_completo["Quantidade"].fillna(0)

            st.subheader("📊 Evolução do Número de Alunos PEC-G por País")
            fig = px.line(df_completo, x="Ano de entrada PEC-PLE", y="Quantidade", color="País de origem", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Não há dados agrupados para exibir o gráfico de evolução por país.")
    else:
        st.info("ℹ️ Nenhum dado disponível após aplicar os filtros.")
else:
    st.error("🚨 As colunas 'Ano de entrada PEC-PLE' e 'País de origem' não foram encontradas nos dados.")

# ======================================================================
# (9) Botão de Logout
# ======================================================================
st.sidebar.button("Sair", on_click=logout)
