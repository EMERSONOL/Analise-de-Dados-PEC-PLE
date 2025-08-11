import streamlit as st
import hashlib
import base64
from pathlib import Path

# --- FUNÇÕES DE HASH (sem alterações) ---
def make_hashes(password):
    """Gera o hash SHA256 da senha."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_hashes(hashed_password, user_password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return make_hashes(user_password) == hashed_password

# --- BANCO DE DADOS DE USUÁRIOS (exemplo) ---
USERS = {
    "Emerson": "dadaecdbec200e1141248153336698233ceb388b52859be85c54e98236507888",
    "Patricia": "465bca39e0786f2e2146ddc717e62fc5e5ed3467575e93f822e2bc97607d9441",
    "Admin": "c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f"
}

# --- FUNÇÃO PARA CONVERTER IMAGEM LOCAL PARA BASE64 ---
def get_image_as_base64(path_str):
    """Converte uma imagem local para uma string base64."""
    path = Path(path_str)
    if not path.is_file():
        return None
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/{path.suffix.lstrip('.')};base64,{encoded_string}"

# --- FORMULÁRIO DE LOGIN COM DESIGN MODERNO ---
def login_form():
    """Renderiza o formulário de login com um design centralizado e moderno."""
    
    # --- CONFIGURAÇÕES DA PÁGINA ---
    st.set_page_config(layout="wide", page_title="Login")

    # --- CAMINHO DA IMAGEM ---
    # !!! IMPORTANTE: Substitua pelo caminho correto da sua imagem !!!
    image_path = "E:/atual - PECPLE/PEC-PLE/login_capa.jpg"
    image_base64 = get_image_as_base64(image_path)
    
    background_image_css = ""
    if image_base64:
        background_image_css = f"""
            background-image: url("{image_base64}");
            background-size: cover;
            background-position: center;
        """

    # --- ESTILO CSS CUSTOMIZADO ---
    CUSTOM_CSS = f"""
    <style>
        /* Remove o padding padrão do Streamlit */
        .block-container {{
            padding: 0 !important;
        }}
        
        /* Contêiner principal para centralizar o conteúdo */
        .main-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            {background_image_css}
        }}
        
        /* Card de login */
        .login-card {{
            background-color: rgba(255, 255, 255, 0.9); /* Fundo branco semitransparente */
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 450px;
        }}
        
        h2 {{
            text-align: center;
            margin-bottom: 2rem;
            color: #333;
        }}

        /* Estilo dos campos de texto */
        div[data-testid="stTextInput"] > div > div > input {{
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }}
        
        /* Estilo do botão de login */
        div[data-testid="stButton"] > button {{
            width: 100%;
            border-radius: 5px;
            background-color: #E87A5D; /* Cor de destaque */
            color: white;
            font-weight: 600;
            border: none;
            padding: 10px 0;
            margin-top: 1rem;
        }}

        div[data-testid="stButton"] > button:hover {{
            background-color: #D36A4F; /* Cor mais escura no hover */
        }}

        /* Mensagens de erro e sucesso */
        div[data-testid="stAlert"] {{
            border-radius: 5px;
        }}

    </style>
    """
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # --- ESTRUTURA DO LAYOUT ---
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h2>Bem-vindo(a) de volta!</h2>", unsafe_allow_html=True)

        with st.form('sign_in_form', clear_on_submit=False):
            username = st.text_input('Usuário', placeholder="Digite seu nome de usuário")
            password = st.text_input('Senha', placeholder="Digite sua senha", type='password')
            remember_me = st.checkbox("Lembrar-me")
            submit_btn = st.form_submit_button(label="Entrar")
            
            if submit_btn:
                if not username or not password:
                    st.error("❗ Por favor, preencha todos os campos.")
                elif username in USERS and check_hashes(USERS[username], password):
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = username
                    st.rerun() # Recarrega a página para refletir o estado de login
                else:
                    st.error("❌ Usuário ou senha incorretos.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- PONTO DE ENTRADA DA APLICAÇÃO ---
def main_app():
    """Renderiza a página principal após o login."""
    st.set_page_config(layout="centered", page_title="App Principal")
    
    st.title(f"Bem-vindo(a) à sua Aplicação, {st.session_state['current_user']}!")
    st.success("Você está logado com sucesso.")
    st.write("Aqui você pode adicionar o conteúdo principal da sua aplicação.")
    
    if st.button("Sair"):
        st.session_state["logged_in"] = False
        st.session_state.pop("current_user", None)
        st.rerun()

# --- LÓGICA DE EXECUÇÃO ---
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_form()
    else:
        main_app()
