import streamlit as st
import pandas as pd
import os
from PIL import Image
import pycountry

# --- FUNÇÃO DE LOGOUT ---
def logout():
    st.session_state["logged_in"] = False
    st.rerun()

# --- VERIFICAÇÃO DE LOGIN ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔒 Por favor, faça o login para acessar esta página.")
    if st.button("Ir para Login"):
        st.switch_page("Home.py")
    st.stop()

# ---------- Funções auxiliares ----------
@st.cache_data
def load_data():
    #file_url = "https://docs.google.com/spreadsheets/d/1rRQmXlVAKQocCfJy0CIsZGMJUxdMvKdI/export?format=xlsx"
    # Caminho da planilha USB
    file_url = "E:/atual - PECPLE\PEC-PLE/SISTEMA DE GERENCIAMENTO DE DADOS.xlsx"
    df = pd.read_excel(file_url, engine='openpyxl')  
    return df
# ------- Função para carregar a bandeira -------------
def get_country_code(country_name):
    # Dicionário de códigos de países por nome
    country_codes = {'Afghanistan': 'af','Albania': 'al',
 'Algeria': 'dz',
 'American Samoa': 'as',
 'Andorra': 'ad',
 'Angola': 'ao',
 'Anguilla': 'ai',
 'Antarctica': 'aq',
 'Antigua and Barbuda': 'ag',
 'Argentina': 'ar',
 'Armenia': 'am',
 'Aruba': 'aw',
 'Australia': 'au',
 'Austria': 'at',
 'Azerbaijan': 'az',
 'Bahamas': 'bs',
 'Bahrain': 'bh',
 'Bangladesh': 'bd',
 'Barbados': 'bb',
 'Belarus': 'by',
 'Belgium': 'be',
 'Belize': 'bz',
 'Benin': 'bj',
 'Bermuda': 'bm',
 'Bhutan': 'bt',
 'Bolivia, Plurinational State of': 'bo',
 'Bonaire, Sint Eustatius and Saba': 'bq',
 'Bosnia and Herzegovina': 'ba',
 'Botswana': 'bw',
 'Bouvet Island': 'bv',
 'Brazil': 'br',
 'British Indian Ocean Territory': 'io',
 'Brunei Darussalam': 'bn',
 'Bulgaria': 'bg',
 'Burkina Faso': 'bf',
 'Burundi': 'bi',
 'Cabo Verde': 'cv',
 'Cambodia': 'kh',
 'Cameroon': 'cm',
 'Canada': 'ca',
 'Cayman Islands': 'ky',
 'Central African Republic': 'cf',
 'Chad': 'td',
 'Chile': 'cl',
 'China': 'cn',
 'Christmas Island': 'cx',
 'Cocos (Keeling) Islands': 'cc',
 'Colombia': 'co',
 'Comoros': 'km',
 'Congo': 'cg',
 'Congo, The Democratic Republic of the': 'cd',
 'Cook Islands': 'ck',
 'Costa Rica': 'cr',
 'Croatia': 'hr',
 'Cuba': 'cu',
 'Curaçao': 'cw',
 'Cyprus': 'cy',
 'Czechia': 'cz',
 "Côte d'Ivoire": 'ci',
 'Denmark': 'dk',
 'Djibouti': 'dj',
 'Dominica': 'dm',
 'Dominican Republic': 'do',
 'Ecuador': 'ec',
 'Egypt': 'eg',
 'El Salvador': 'sv',
 'Equatorial Guinea': 'gq',
 'Eritrea': 'er',
 'Estonia': 'ee',
 'Eswatini': 'sz',
 'Ethiopia': 'et',
 'Falkland Islands (Malvinas)': 'fk',
 'Faroe Islands': 'fo',
 'Fiji': 'fj',
 'Finland': 'fi',
 'France': 'fr',
 'French Guiana': 'gf',
 'French Polynesia': 'pf',
 'French Southern Territories': 'tf',
 'Gabon': 'ga',
 'Gambia': 'gm',
 'Georgia': 'ge',
 'Germany': 'de',
 'Ghana': 'gh',
 'Gibraltar': 'gi',
 'Greece': 'gr',
 'Greenland': 'gl',
 'Grenada': 'gd',
 'Guadeloupe': 'gp',
 'Guam': 'gu',
 'Guatemala': 'gt',
 'Guernsey': 'gg',
 'Guinea': 'gn',
 'Guinea-Bissau': 'gw',
 'Guyana': 'gy',
 'Haiti': 'ht',
 'Heard Island and McDonald Islands': 'hm',
 'Holy See (Vatican City State)': 'va',
 'Honduras': 'hn',
 'Hong Kong': 'hk',
 'Hungary': 'hu',
 'Iceland': 'is',
 'India': 'in',
 'Indonesia': 'id',
 'Iran, Islamic Republic of': '🇮🇷',
 'Iraq': 'iq',
 'Ireland': 'ie',
 'Isle of Man': 'im',
 'Israel': 'il',
 'Italy': 'it',
 'Jamaica': 'jm',
 'Japan': 'jp',
 'Jersey': 'je',
 'Jordan': 'jo',
 'Kazakhstan': 'kz',
 'Kenya': 'ke',
 'Kiribati': 'ki',
 "Korea, Democratic People's Republic of": 'kp',
 'Korea, Republic of': 'kr',
 'Kuwait': 'kw',
 'Kyrgyzstan': 'kg',
 "Lao People's Democratic Republic": 'la',
 'Latvia': 'lv',
 'Lebanon': 'lb',
 'Lesotho': 'ls',
 'Liberia': 'lr',
 'Libya': 'ly',
 'Liechtenstein': 'li',
 'Lithuania': 'lt',
 'Luxembourg': 'lu',
 'Macao': 'mo',
 'Madagascar': 'mg',
 'Malawi': 'mw',
 'Malaysia': 'my',
 'Maldives': 'mv',
 'Mali': 'ml',
 'Malta': 'mt',
 'Marshall Islands': 'mh',
 'Martinique': 'mq',
 'Mauritania': 'mr',
 'Mauritius': 'mu',
 'Mayotte': 'yt',
 'Mexico': 'mx',
 'Micronesia, Federated States of': 'fm',
 'Moldova, Republic of': 'md',
 'Monaco': 'mc',
 'Mongolia': 'mn',
 'Montenegro': 'me',
 'Montserrat': 'ms',
 'Morocco': 'ma',
 'Mozambique': 'mz',
 'Myanmar': 'mm',
 'Namibia': 'na',
 'Nauru': 'nr',
 'Nepal': 'np',
 'Netherlands': 'nl',
 'New Caledonia': 'nc',
 'New Zealand': 'nz',
 'Nicaragua': 'ni',
 'Niger': 'ne',
 'Nigeria': 'ng',
 'Niue': 'nu',
 'Norfolk Island': 'nf',
 'North Macedonia': 'mk',
 'Northern Mariana Islands': 'mp',
 'Norway': 'no',
 'Oman': 'om',
 'Pakistan': 'pk',
 'Palau': 'pw',
 'Palestine, State of': 'ps',
 'Panama': 'pa',
 'Papua New Guinea': 'pg',
 'Paraguay': 'py',
 'Peru': 'pe',
 'Philippines': 'ph',
 'Pitcairn': 'pn',
 'Poland': 'pl',
 'Portugal': 'pt',
 'Puerto Rico': 'pr',
 'Qatar': 'qa',
 'Romania': 'ro',
 'Russian Federation': 'ru',
 'Rwanda': 'rw',
 'Réunion': 're',
 'Saint Barthélemy': 'bl',
 'Saint Helena, Ascension and Tristan da Cunha': 'sh',
 'Saint Kitts and Nevis': 'kn',
 'Saint Lucia': 'lc',
 'Saint Martin (French part)': 'mf',
 'Saint Pierre and Miquelon': 'pm',
 'Saint Vincent and the Grenadines': 'vc',
 'Samoa': 'ws',
 'San Marino': 'sm',
 'Sao Tome and Principe': 'st',
 'Saudi Arabia': 'sa',
 'Senegal': 'sn',
 'Serbia': 'rs',
 'Seychelles': 'sc',
 'Sierra Leone': 'sl',
 'Singapore': 'sg',
 'Sint Maarten (Dutch part)': 'sx',
 'Slovakia': 'sk',
 'Slovenia': 'si',
 'Solomon Islands': 'sb',
 'Somalia': 'so',
 'South Africa': 'za',
 'South Georgia and the South Sandwich Islands': 'gs',
 'South Sudan': 'ss',
 'Spain': 'es',
 'Sri Lanka': 'lk',
 'Sudan': 'sd',
 'Suriname': 'sr',
 'Svalbard and Jan Mayen': 'sj',
 'Sweden': 'se',
 'Switzerland': 'ch',
 'Syrian Arab Republic': 'sy',
 'Taiwan, Province of China': 'tw',
 'Tajikistan': 'tj',
 'Tanzania, United Republic of': 'tz',
 'Thailand': 'th',
 'Timor-Leste': 'tl',
 'Togo': 'tg',
 'Tokelau': 'tk',
 'Tonga': 'to',
 'Trinidad and Tobago': 'tt',
 'Tunisia': 'tn',
 'Turkey': 'tr',
 'Turkmenistan': 'tm',
 'Turks and Caicos Islands': 'tc',
 'Tuvalu': 'tv',
 'Uganda': 'ug',
 'Ukraine': 'ua',
 'United Arab Emirates': 'ae',
 'United Kingdom': 'gb',
 'United States': 'us',
 'United States Minor Outlying Islands': 'um',
 'Uruguay': 'uy',
 'Uzbekistan': 'uz',
 'Vanuatu': 'vu',
 'Venezuela, Bolivarian Republic of': 've',
 'Viet Nam': 'vn',
 'Virgin Islands, British': 'vg',
 'Virgin Islands, U.S.': 'vi',
 'Wallis and Futuna': 'wf',
 'Western Sahara': 'eh',
 'Yemen': 'ye',
 'Zambia': 'zm',
 'Zimbabwe': 'zw',
 'Åland Islands': 'ax'}
    
    return country_codes.get(country_name, None)
def get_flag_url(country_name):
    code = get_country_code(country_name)
    if code:
        return f"https://flagcdn.com/w80/{code}.png"  # 80px de largura
    return None

# ---------- Logo ----------
# Caminho da logo
logo_path = "e:/PEC-PLE/logo.png"

# Caminho da logo
#logo_path = "C:/Users/EMERSON/OneDrive/Área de Trabalho/PEC-PLE/logo.png"
imagem = Image.open(logo_path)
st.logo(imagem)

# ---------- Carregar dados ----------
try:
    data = load_data()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

if data.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

# ---------- Barra lateral (filtros) ----------
st.sidebar.title("🔎 Filtros")

# Selecionar Ano de Entrada
anos = sorted(data["Ano de entrada PEC-PLE"].dropna().unique(), reverse=True)

selected_year = st.sidebar.selectbox("Selecione o ano de entrada PEC-PLE", anos)

# Filtrar alunos pelo ano selecionado
students_by_year = data[data["Ano de entrada PEC-PLE"] == selected_year]["Nome"].dropna().unique()
students_by_year = sorted(students_by_year)


# Seletor de aluno
selected_name = st.sidebar.selectbox("Selecione o aluno", students_by_year)

# ---------- Dados do aluno selecionado ----------
student_data = data[data["Nome"] == selected_name]

if student_data.empty:
    st.warning("Nenhum dado encontrado para o aluno selecionado.")
    st.stop()

student_data = student_data.iloc[0]

# Caminhos de imagens USB
photo_folder = r"e:\\PEC-PLE\\Foto dos Alunos"
# Caminhos de imagens
#photo_folder = r"C:\\Users\\EMERSON\\OneDrive\\Área de Trabalho\\PEC-PLE\\Foto dos Alunos"
photo_path = os.path.join(photo_folder, f"{selected_name}.png")
country_name = student_data.get("País de origem", "Não disponível")
flag_url = get_flag_url(country_name)

# ---------- Corpo principal ----------
st.subheader("🎓 Ficha de Perfil do Aluno")

col1, col2 = st.columns([1, 2])

with col1:
    if os.path.exists(photo_path):
        st.image(photo_path, width=200)
    else:
        st.warning("📸 Foto não encontrada.")
    
    if flag_url:
        
        st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="{flag_url}" width="30" style="margin-right: 10px;">
            <span style="font-weight: bold; font-size: 18px;">{country_name}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    else:
        st.markdown(
            f"**{country_name}** (bandeira indisponível)"
    )

    

with col2:
    st.markdown(f"### {student_data.get('Nome', 'Nome não disponível')}")
    st.write(f"**Ano de entrada PEC-PLE:** {student_data.get('Ano de entrada PEC-PLE', 'Não disponível')}")
    st.write(f"**Sexo:** {student_data.get('Sexo', 'Não disponível')}")
    st.write(f"**Data de nascimento:** {student_data.get('Data de nascimento', 'Não disponível')}")
    st.write(f"**Email:** {student_data.get('Email', 'Não disponível')}")
    st.write(f"**Telefone:** {student_data.get('Telefone', 'Não disponível')}")

st.divider()

st.subheader("🏛️ Informações Acadêmicas")
st.write(f"**Sigla IES PEC-PLE:** {student_data.get('Sigla_IES_PEC_PLE', 'Não disponível')}")
st.write(f"**IES PEC-PLE:** {student_data.get('IES PEC-PLE', 'Não disponível')}")
st.write(f"**Cidade PEC-PLE:** {student_data.get('CidadePEC-PLE', 'Não disponível')}")

st.write(f"**Sigla IES PEC-G:** {student_data.get('Sigla IES PEC-G', 'Não disponível')}")
st.write(f"**IES PEC-G:** {student_data.get('IES PEC-G', 'Não disponível')}")
st.write(f"**Curso PEC-G:** {student_data.get('Curso PEC-G', 'Não disponível')}")
st.write(f"**Habilitação:** {student_data.get('Habilitação', 'Não disponível')}")
st.write(f"**Cidade:** {student_data.get('Cidade', 'Não disponível')}")
st.write(f"**Semestre de ingresso PEC-G:** {student_data.get('Semestre de ingresso PEC-G', 'Não disponível')}")

st.divider()

st.subheader("📝 Informações Celpe-Bras")
st.write(f"**1ª tentativa:** {student_data.get('Ano e semestre de realização do Celpe-Bras - primeira tentativa', 'Não disponível')}")
st.write(f"**Nível de certificação:** {student_data.get('Nível de certificação', 'Não disponível')}")
st.write(f"**2ª tentativa:** {student_data.get('Ano e semestre de realização do Celpe-Bras - segunda tentativa', 'Não disponível')}")
st.write(f"**Nível de certificação (segunda tentativa):** {student_data.get('Nível de certificação - segunda tentativa', 'Não disponível')}")

# botão de sair
st.sidebar.button("Sair", on_click=logout)