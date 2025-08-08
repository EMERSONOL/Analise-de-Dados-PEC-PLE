# -------------- Bibliotecas ----------------------

import streamlit as st
from PIL import Image
import os

# -------------- pagina de inicio ---------------------
# Configura a largura da página
st.set_page_config(page_title="Análise de Dados do PEC-PLE", layout="wide")

# Agora importa o login
from login import login_form

# Verifica se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- EXIBE APENAS O LOGIN QUANDO NÃO ESTIVER AUTENTICADO ---
if not st.session_state["logged_in"]:
    # Esconde a sidebar com CSS
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Exibe o formulário de login
    login_form()

# --- INTERFACE PRINCIPAL DO DASHBOARD (SÓ APARECE APÓS LOGIN) ---
else:
    # Exibe o logo no topo
    logo_path = "logo.png"  # Altere para o seu caminho se necessário
    imagem = Image.open(logo_path)
    st.logo(imagem)

    # CSS para texto justificado
    st.markdown("""
        <style>
        .justificado {
            text-align: justify;
        }
        </style>
    """, unsafe_allow_html=True)

    # Título da página
    st.markdown("<h1 style='text-align: center;'>Análise de Dados do PEC-PLE e PEC-G</h1>", unsafe_allow_html=True)

    # Função para carregar imagens da galeria
    def load_images(image_folder, target_width=800):
        images = []
        target_height = int(target_width * 9 / 16)
        for filename in os.listdir(image_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(os.path.join(image_folder, filename))
                if img.width > img.height:
                    img = img.resize((target_width, target_height), Image.LANCZOS)
                images.append(img)
        return images

    # Pasta de imagens
    image_folder = r'e:\PEC-PLE\Folder'
    images = load_images(image_folder)

    if 'current_image' not in st.session_state:
        st.session_state.current_image = 0

    # Exibe imagem atual
    st.image(images[st.session_state.current_image], use_container_width=True)

    # Botões de navegação
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        btn_prev, btn_next = st.columns(2)
        with btn_prev:
            if st.button("←", key='prev'):
                if st.session_state.current_image > 0:
                    st.session_state.current_image -= 1
        with btn_next:
            if st.button("→", key='next'):
                if st.session_state.current_image < len(images) - 1:
                    st.session_state.current_image += 1

    # Texto explicativo
    st.markdown("""
        <div class="justificado">
        <b>O Programa de Estudantes-Convênio de Graduação (PEC-G)</b> desempenha um papel fundamental na cooperação educacional internacional, oferecendo a estudantes estrangeiros a oportunidade de realizar sua graduação no Brasil. Implementado em parceria entre o <b>Ministério das Relações Exteriores (MRE)</b> e o <b>Ministério da Educação (MEC)</b>, o programa fortalece laços acadêmicos e culturais com países em desenvolvimento.

        A análise de dados aplicada ao PEC-G permite um entendimento mais profundo sobre o perfil dos alunos, a distribuição geográfica, a evolução do programa ao longo dos anos e o impacto nas instituições de ensino superior brasileiras. Através da coleta e processamento preciso das informações, é possível identificar padrões, otimizar processos seletivos e aprimorar estratégias para melhor atender às demandas dos estudantes e universidades participantes.

        Além disso, a análise criteriosa dos dados garante maior transparência e eficiência na gestão do programa, permitindo que tomadores de decisão embasem políticas educacionais de forma mais assertiva. O monitoramento contínuo também contribui para avaliar o retorno dos alunos aos seus países de origem, verificando os impactos da formação acadêmica em suas comunidades e promovendo melhorias na cooperação internacional.

        Este <b>dashboard interativo</b> foi desenvolvido para proporcionar uma visão clara e detalhada dos dados do PEC-G, facilitando a exploração das informações e auxiliando na tomada de decisões estratégicas. 🚀📈
        </div>
    """, unsafe_allow_html=True)

    # Botão de logout

    st.sidebar.button("Sair", on_click=lambda: st.session_state.update(logged_in=False, current_page="Home"), key="logout_button")
