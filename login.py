import streamlit as st
import hashlib

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Login")

# --- FUNÇÕES DE HASH (sem alterações) ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# --- BANCO DE DADOS DE USUÁRIOS (exemplo) ---
# Em um ambiente de produção, use um banco de dados seguro.
users_db = {
    "Emerson": "dadaecdbec200e1141248153336698233ceb388b52859be85c54e98236507888",
    "Admin": "c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f",
    "Patricia": "465bca39e0786f2e2146ddc717e62fc5e5ed3467575e93f822e2bc97607d9441",
}

# --- ESTILO CSS CUSTOMIZADO ---
# Inspirado na imagem fornecida pelo usuário.
st.markdown("""
<style>
    /* Remove o padding padrão do container principal do Streamlit */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Container principal para o layout de duas colunas */
    .main-layout {
        display: flex;
        width: 100vw;
        height: 100vh;
        margin: 0;
    }

    /* Coluna da esquerda (ilustração) */
    .left-column {
        flex: 1.2;
        background-color: #0099FF; /* Cor azul da imagem */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        padding: 2rem;
    }
    
    .left-column h1 {
        font-size: 2.5rem;
        font-weight: bold;
    }

    /* Coluna da direita (formulário) */
    .right-column {
        flex: 1.5;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #FFFFFF;
        padding: 3rem;
    }
    
    .login-form-container {
        width: 100%;
        max-width: 450px;
    }

    .login-form-container h2 {
        font-size: 2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
        text-align: left;
    }

    /* Estiliza os campos de texto */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 5px;
        border: 1px solid #E0E0E0;
        padding: 12px;
        background-color: #FAFAFA;
    }
    
    /* Checkbox "Remember me" */
    .stCheckbox {
        color: #555;
    }

    /* Links e texto secundário */
    .form-links {
        display: flex;
        justify-content: space-between;
        margin-top: -15px;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    
    .form-links a {
        color: #0099FF;
        text-decoration: none;
    }
    
    /* Botão Entrar */
    div[data-testid="stButton"] > button {
        width: 100%;
        border-radius: 5px;
        background-color: #0099FF;
        color: white;
        font-weight: bold;
        padding: 12px 0;
        border: none;
        margin: 1rem 0;
    }

    div[data-testid="stButton"] > button:hover {
        background-color: #007ACC;
    }
    
    /* Seção "Logar Com" */
    .social-login {
        text-align: center;
        margin-top: 2rem;
        color: #888;
    }
    
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 1rem;
        font-size: 2rem; /* Tamanho dos ícones */
    }

    .social-icons a {
        color: #333;
        text-decoration: none;
    }
    
    .signup-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #555;
    }
    
    .signup-link a {
        color: #0099FF;
        font-weight: bold;
        text-decoration: none;
    }

</style>
""", unsafe_allow_html=True)

# --- Carregar ícones do Font Awesome ---
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)

def login_page():
    # --- LAYOUT PRINCIPAL ---
    st.markdown('<div class="main-layout">', unsafe_allow_html=True)

    # --- COLUNA DA ESQUERDA ---
    st.markdown("""
        <div class="left-column">
            <h1>Sua Plataforma</h1>
            <p>Bem-vindo(a)! Faça login para continuar.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- COLUNA DA DIREITA ---
    col1, col2 = st.columns([1.2, 1.5]) # Apenas para estrutura, o CSS controla o layout

    with col2:
        st.markdown('<div class="right-column">', unsafe_allow_html=True)
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        
        st.markdown("<h2>LOGIN</h2>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="@mail.com", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        # Links abaixo dos campos
        st.markdown("""
            <div class="form-links">
                <label class="stCheckbox"><input type="checkbox"> Remember me</label>
                <a href="#">Esqueceu a senha?</a>
            </div>
        """, unsafe_allow_html=True)
        
        # Botão de login
        if st.button("Entrar"):
            if username in users_db and check_hashes(password, users_db[username]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
        
        # Link de inscrição
        st.markdown('<p class="signup-link">Não Tem Uma Conta? <a href="#">Inscrever-se</a></p>', unsafe_allow_html=True)
        
        # Seção de login social
        st.markdown('<div class="social-login">Logar Com</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="social-icons">
                <a href="#"><i class="fab fa-facebook-f"></i></a>
                <a href="#"><i class="fab fa-google"></i></a>
                <a href="#"><i class="fab fa-apple"></i></a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Fim do login-form-container
        st.markdown('</div>', unsafe_allow_html=True) # Fim do right-column

    st.markdown('</div>', unsafe_allow_html=True) # Fim do main-layout


def main_app():
    st.title(f"Bem-vindo, {st.session_state['username']}!")
    st.write("Você está na página principal da aplicação.")
    if st.button("Sair"):
        st.session_state['logged_in'] = False
        del st.session_state['username']
        st.rerun()

# --- CONTROLE DE FLUXO ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_page()
