import streamlit as st
from PIL import Image
import random
import os
import time

# =====================================================
# PALETA DE CORES (GFTeam IAPC de Irajá)
# =====================================================
COR_FUNDO = "#0e2d26"
COR_TEXTO = "#FFFFFF"
COR_TEXTO_SUAVE = "#CCCCCC"
COR_DESTAQUE = "#FFD700"

# =====================================================
# CONFIGURAÇÃO DO APP
# =====================================================
st.set_page_config(
    page_title="🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá",
    layout="centered",
    page_icon="🥋"
)

# =====================================================
# TIPOGRAFIA E ESTILO MODERNO
# =====================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(180deg, #0e2d26 0%, #143d35 100%);
        color: {COR_TEXTO};
        font-family: 'Inter', sans-serif;
    }}

    h1 {{
        font-family: 'Montserrat', sans-serif;
        color: {COR_DESTAQUE};
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        text-shadow: 0px 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 5px;
        background: linear-gradient(90deg, #eac645, #fff6c5, #eac645);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shine 5s linear infinite;
    }}

    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}

    h2 {{
        text-align: center;
        color: {COR_TEXTO};
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        margin-top: -5px;
        margin-bottom: 40px;
    }}

    /* Botões premium */
    .stButton>button {{
        background: linear-gradient(135deg, #0fa37f 0%, #0b5c48 100%);
        color: {COR_TEXTO};
        border: none;
        border-radius: 14px;
        padding: 14px 36px;
        font-size: 17px;
        font-weight: 700;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 0.6px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.25);
        transition: all 0.25s ease-in-out;
    }}

    .stButton>button:hover {{
        transform: translateY(-3px) scale(1.03);
        background: linear-gradient(135deg, #eac645 0%, #d1a700 100%);
        color: #0e2d26;
        box-shadow: 0px 8px 20px rgba(255, 215, 0, 0.3);
    }}

    .stButton>button:active {{
        transform: scale(0.98);
        box-shadow: 0px 3px 6px rgba(0,0,0,0.3);
    }}

    /* Perguntas */
    .question {{
        font-size: 22px;
        text-align: center;
        font-weight: 500;
        color: {COR_TEXTO};
        font-family: 'Inter', sans-serif;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 0 8px rgba(255,215,0,0.15);
    }}

    .stRadio > div {{
        background-color: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 15px;
        font-family: 'Inter', sans-serif;
    }}

    img {{
        display: block;
        margin: auto;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0,0,0,0.4);
    }}

    img[src*="topo.webp"] {{
        box-shadow: none !important;
        border-radius: 0 !important;
    }}

    .divider {{
        width: 80%;
        height: 3px;
        background: linear-gradient(90deg, transparent, {COR_DESTAQUE}, transparent);
        margin: 25px auto;
        border-radius: 5px;
    }}

    .fade {{
        animation: fadeIn 1s ease-in-out;
    }}

    @keyframes fadeIn {{
        0% {{opacity: 0; transform: translateY(10px);}}
        100% {{opacity: 1; transform: translateY(0);}}
    }}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÃO PARA EXIBIR IMAGEM
# =====================================================
def mostrar_imagem(caminho, max_largura=700):
    if os.path.exists(caminho):
        img = Image.open(caminho)
        largura, altura = img.size
        if largura > max_largura:
            proporcao = max_largura / largura
            nova_altura = int(altura * proporcao)
            img = img.resize((max_largura, nova_altura))
        st.image(img, use_column_width=False)

# =====================================================
# PERGUNTAS (resumo funcional)
# =====================================================
perguntas = {
    "regras": [
        {"nivel": 1, "imagem": "imagens/inicio_luta.png",
         "pergunta": "Quando o árbitro estende o braço à frente e faz movimento vertical em direção ao solo, o que ele indica?",
         "opcoes": ["A) Parar a luta", "B) Início da luta", "C) Punição", "D) Declaração do vencedor"],
         "resposta": "B"},
        {"nivel": 1, "imagem": "imagens/dois_pontos.png",
         "pergunta": "O árbitro ergue dois dedos (indicador e médio). O que significa?",
         "opcoes": ["A) Duas vantagens", "B) Dois pontos (queda, raspagem ou joelho na barriga)",
                    "C) Punição dupla", "D) Pedido de médico"],
         "resposta": "B"},
    ]
}

# =====================================================
# ESTADOS DO JOGO
# =====================================================
if "tema" not in st.session_state:
    st.session_state.tema = None
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# =====================================================
# INTERFACE INICIAL
# =====================================================
st.markdown('<div class="fade">', unsafe_allow_html=True)
st.title("🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá")
mostrar_imagem("imagens/topo.webp", max_largura=700)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if not st.session_state.tema:
    st.subheader("Escolha o tema do seu desafio:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚖️ Regras e Arbitragem"):
            st.session_state.tema = "regras"
    with col2:
        if st.button("🎖️ Graduações e Faixas"):
            st.session_state.tema = "graduacoes"
    with col3:
        if st.button("📜 História e Projeto Resgate"):
            st.session_state.tema = "historia"
    st.stop()

# =====================================================
# QUIZ (exemplo funcional)
# =====================================================
tema = st.session_state.tema
lista_perguntas = perguntas.get(tema, [])
if lista_perguntas:
    p = lista_perguntas[st.session_state.indice % len(lista_perguntas)]
    st.markdown(f"<div class='question'>{p['pergunta']}</div>", unsafe_allow_html=True)
    mostrar_imagem(p["imagem"], max_largura=500)

    opcao = st.radio("Escolha sua resposta:", p["opcoes"], index=None, label_visibility="collapsed")
    if st.button("Responder"):
        if not opcao:
            st.warning("Escolha uma opção antes de continuar!")
        elif opcao[0] == p["resposta"]:
            st.success("✅ Correto!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Errado! A resposta certa era {p['resposta']}.")
        time.sleep(0.8)
        st.session_state.indice += 1
        st.rerun()
