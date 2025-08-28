import streamlit as st
import pandas as pd
import os
import datetime

# Caminho fixo do Excel
ARQUIVO_EXCEL = "SISTEMA DE GERENCIAMENTO DE DADOS.xlsx"

# Colunas esperadas
CAMPOS_ALUNO = [
    "Ano de entrada PEC-PLE", "Nome", "País de origem", "Sexo", "Data de nascimento",
    "Sigla_IES_PEC_PLE", "IES PEC-PLE", "Cidade PEC-PLE", "Email", "Telefone",
    "Sigla IES PEC-G", "IES PEC-G", "Curso PEC-G", "Habilitação", "Cidade", "Semestre de ingresso PEC-G"
]

# Função para carregar dados existentes ou criar planilha
def carregar_dados():
    if os.path.exists(ARQUIVO_EXCEL):
        df = pd.read_excel(ARQUIVO_EXCEL)
        # Garante que todas as colunas existam
        for col in CAMPOS_ALUNO:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        df = pd.DataFrame(columns=CAMPOS_ALUNO)
        df.to_excel(ARQUIVO_EXCEL, index=False)
        return df

# Função para salvar os dados
def salvar_dados(df):
    df.to_excel(ARQUIVO_EXCEL, index=False)

# Layout da interface
st.set_page_config(page_title="Cadastro PEC-PLE & PEC-G", layout="wide")

tab1, tab2, tab3 = st.tabs(["🏫 Cadastrar aluno", "📝 Cadastrar avaliação", "📈 Visualizar dados"])

# === Cadastrar aluno ===
with tab1:
    st.subheader("📌 Cadastro de Aluno Estrangeiro")

    with st.form("form_aluno"):
        col1, col2 = st.columns(2)
        with col1:
            ano_entrada = st.text_input("Ano de entrada PEC-PLE")
            nome = st.text_input("Nome")
            pais = st.text_input("País de origem")
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            nascimento = st.date_input(
    "Data de nascimento",
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")

        with col2:
            sigla_ple = st.text_input("Sigla_IES_PEC_PLE")
            ies_ple = st.text_input("IES PEC-PLE")
            cidade_ple = st.text_input("Cidade PEC-PLE")
            sigla_pecg = st.text_input("Sigla IES PEC-G")
            ies_pecg = st.text_input("IES PEC-G")
            curso = st.text_input("Curso PEC-G")
            habilitacao = st.text_input("Habilitação")
            cidade = st.text_input("Cidade")
            semestre_ingresso = st.text_input("Semestre de ingresso PEC-G")

        enviado = st.form_submit_button("💾 Salvar")

        if enviado:
            df = carregar_dados()

            # Evita cadastro duplicado (mesmo nome e email, por exemplo)
            if ((df["Nome"] == nome) & (df["Email"] == email)).any():
                st.warning(f"⚠️ O aluno '{nome}' já está cadastrado!")
            else:
                novo = pd.DataFrame([[
                    ano_entrada, nome, pais, sexo, str(nascimento), sigla_ple, ies_ple,
                    cidade_ple, email, telefone, sigla_pecg, ies_pecg,
                    curso, habilitacao, cidade, semestre_ingresso
                ]], columns=CAMPOS_ALUNO)

                df = pd.concat([df, novo], ignore_index=True)
                salvar_dados(df)
                st.success(f"✅ Aluno '{nome}' cadastrado com sucesso!")

# === Cadastrar avaliação ===
with tab2:
    st.subheader("📝 Cadastro de Avaliação do Aluno")
    st.info("Aqui você pode vincular a avaliação Celpe-Bras ao aluno já cadastrado.")

    df = carregar_dados()
    if df.empty:
        st.warning("Nenhum aluno cadastrado ainda.")
    else:
        aluno = st.selectbox("Selecione o aluno", df["Nome"])
        col1, col2 = st.columns(2)

        with col1:
            tentativa1 = st.text_input("Ano e semestre - 1ª tentativa")
            resultado1 = st.selectbox("Resultado 1ª tentativa", ["Aprovado", "Reprovado", "Não se Aplica"])
            nivel1 = st.selectbox("Nível certificação 1ª tentativa", ["Nível Avançado Superior", "Nível Avançado", "Nível Intermediario Superior", "Nível Intermediario", "Não se Aplica"])

        with col2:
            tentativa2 = st.text_input("Ano e semestre - 2ª tentativa")
            resultado2 = st.selectbox("Resultado 2ª tentativa", ["Aprovado", "Reprovado", "Não se Aplica"])
            nivel2 = st.selectbox("Nível certificação 2ª tentativa", ["Nível Avançado Superior", "Nível Avançado", "Nível Intermediario Superior", "Nível Intermediario", "Não se Aplica"])

        if st.button("💾 Salvar Avaliação"):
            idx = df[df["Nome"] == aluno].index[0]
            df.loc[idx, "Ano/Semestre 1ª tentativa"] = tentativa1
            df.loc[idx, "Resultado 1ª tentativa"] = resultado1
            df.loc[idx, "Nível 1ª tentativa"] = nivel1
            df.loc[idx, "Ano/Semestre 2ª tentativa"] = tentativa2
            df.loc[idx, "Resultado 2ª tentativa"] = resultado2
            df.loc[idx, "Nível 2ª tentativa"] = nivel2
            salvar_dados(df)
            st.success(f"✅ Avaliação do aluno '{aluno}' cadastrada com sucesso!")

# === Visualizar dados ===
with tab3:
    st.subheader("📊 Dados Cadastrados")
    df = carregar_dados()
    if df.empty:
        st.warning("Nenhum dado cadastrado ainda.")
    else:
        # Campo de busca por Nome ou Email
        busca = st.text_input("🔎 Buscar aluno por nome ou email")

        if busca:
            df_filtrado = df[df["Nome"].str.contains(busca, case=False, na=False) | 
                             df["Email"].str.contains(busca, case=False, na=False)]
        else:
            df_filtrado = df

        st.dataframe(df_filtrado, use_container_width=True)

        # Excluir aluno (se busca retornar alguém)
        if not df_filtrado.empty and busca:
            aluno_selecionado = st.selectbox("Selecione o aluno para excluir", df_filtrado["Nome"] + " | " + df_filtrado["Email"])

            if st.button("🗑️ Excluir aluno"):
                # Quebra Nome | Email para identificar único
                nome_sel, email_sel = aluno_selecionado.split(" | ")

                # Remove do DataFrame original
                df = df[~((df["Nome"] == nome_sel) & (df["Email"] == email_sel))]

                salvar_dados(df)
                st.success(f"✅ Aluno '{nome_sel}' excluído com sucesso!")

        # Exporta os dados filtrados
        st.download_button(
            "📥 Baixar Excel",
            data=df_filtrado.to_csv(index=False).encode("utf-8"),
            file_name="alunos.csv",
            mime="text/csv"
        )

