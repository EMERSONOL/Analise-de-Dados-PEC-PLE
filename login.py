import streamlit as st
import hashlib
import base64
import json
from pathlib import Path

# --- FUNÇÕES DE HASH ---
def make_hashes(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashes(hashed_password, user_password):
    return make_hashes(user_password) == hashed_password

USERS = {"Emerson": "dadaecdbec200e1141248153336698233ceb388b52859be85c54e98236507888",
  "Patricia": "465bca39e0786f2e2146ddc717e62fc5e5ed3467575e93f822e2bc97607d9441",
  "Admin": "c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f"}

# --- FUNÇÃO PARA CONVERTER IMAGEM LOCAL PARA BASE64 ---
def get_image_as_base64(path_str):
    path = Path(path_str)
    if not path.is_file():
        return None
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/{path.suffix.lstrip('.')};base64,{encoded_string}"

# --- FORMULÁRIO DE LOGIN ---
def login_form():
    image_path = "E:/atual - PECPLE/PEC-PLE/login_capa.jpg"
    image_base64 = get_image_as_base64(image_path)

    CUSTOM_CSS = f"""
    <style>
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }}
        .background-column {{
            background-image: url("{image_base64}");
            background-size: cover;
            background-position: center;
            height: 70vh;
            border-radius: 10px;
        }}
        div[data-testid="column"]:first-child {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        div[data-testid="stButton"] > button {{
            width: 100%;
            border-radius: 5px;
            background-color: #E87A5D;
            color: white;
            font-weight: 600;
            border: none;
        }}
        h2 {{
            text-align: center;
            margin-bottom: 1.5rem;
        }}
    </style>
    """
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1.5], gap="large")
    with col1:
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)
        with st.form('sign_in_form', clear_on_submit=False):
            username = st.text_input('Usuário', placeholder="Digite seu nome de usuário")
            password = st.text_input('Senha', placeholder="Digite sua senha", type='password')
            remember_me = st.checkbox("Lembrar-me")
            submit_btn = st.form_submit_button(label="Entrar")

    with col2:
        if image_base64:
            st.markdown('<div class="background-column"></div>', unsafe_allow_html=True)
        else:
            st.warning("Imagem não encontrada. Verifique o caminho do arquivo.")

    if submit_btn:
        if not username or not password:
            st.error("❗ Por favor, preencha todos os campos.")
        elif username in USERS and check_hashes(USERS[username], password):
            st.success(f"✅ Login realizado com sucesso! Bem-vindo(a), {username}.")
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos.")

# --- PONTO DE ENTRADA ---
if __name__ == "__main__":
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_form()
    else:
        user = st.session_state.get("current_user", "Usuário")
        st.success(f"Você está logado como {user}!")
        st.write(f"Bem-vindo à sua aplicação, {user}!")
        if st.button("Sair"):
            st.session_state["logged_in"] = False
            st.rerun()