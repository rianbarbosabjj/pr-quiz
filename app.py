import streamlit as st
from PIL import Image
import random
import os

# =====================================================
# CONFIGURAÇÕES DE ESTILO E TEMA
# =====================================================
st.set_page_config(
    page_title="Quiz do Projeto Resgate 🥋",
    layout="centered",
    page_icon="🥋"
)

COR_FUNDO = "#0e2d26"
COR_TEXTO = "#FFFFFF"
COR_DESTAQUE = "#FFD700"
COR_BOTAO = "#078B6C"

st.markdown(
    f"""
    <style>
        body {{
            background-color: {COR_FUNDO};
            color: {COR_TEXTO};
        }}
        .stButton>button {{
            background-color: {COR_BOTAO};
            color: white;
            border-radius: 10px;
            padding: 10px 25px;
            border: none;
            font-weight: bold;
            font-size: 18px;
        }}
        .stButton>button:hover {{
            background-color: {COR_DESTAQUE};
            color: black;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# PERGUNTAS POR TEMA
# =====================================================
perguntas = {
    "regras": [
        {"imagem": "imagens/inicio_luta.png", "pergunta": "Quando o árbitro estende o braço à frente e faz movimento vertical em direção ao solo, o que ele indica?",
         "opcoes": ["Parar a luta", "Início da luta", "Punição", "Declaração do vencedor"], "resposta": "Início da luta"},
        {"imagem": "imagens/parar_luta.png", "pergunta": "O que significa o gesto do árbitro?",
         "opcoes": ["Punição", "Parar a luta", "Ponto para ambos", "Desclassificação"], "resposta": "Parar a luta"},
        {"imagem": "imagens/dois_pontos.png", "pergunta": "O árbitro ergue dois dedos (indicador e médio). O que significa?",
         "opcoes": ["Duas vantagens", "Dois pontos (queda, raspagem ou joelho na barriga)", "Punição dupla", "Pedido de médico"], "resposta": "Dois pontos (queda, raspagem ou joelho na barriga)"}
    ],
    "graduacoes": [
        {"imagem": "imagens/faixas.png", "pergunta": "Qual é a ordem correta das faixas no jiu-jitsu adulto?",
         "opcoes": ["Branca, Azul, Roxa, Marrom, Preta", "Azul, Branca, Roxa, Marrom, Preta", "Branca, Roxa, Azul, Marrom, Preta", "Branca, Azul, Preta, Marrom"], "resposta": "Branca, Azul, Roxa, Marrom, Preta"}
    ],
    "historia": [
        {"imagem": "imagens/historia_jj.png", "pergunta": "Quem é considerado o precursor do jiu-jitsu brasileiro?",
         "opcoes": ["Rickson Gracie", "Mitsuyo Maeda (Conde Koma)", "Helio Gracie", "Carlos Gracie"], "resposta": "Mitsuyo Maeda (Conde Koma)"}
    ]
}

# =====================================================
# LÓGICA PRINCIPAL
# =====================================================

if "tema" not in st.session_state:
    st.session_state.tema = None
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# =====================================================
# TELA INICIAL
# =====================================================
st.title("🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá")

if not st.session_state.tema:
    st.subheader("Escolha o tema do seu desafio:")
    if st.button("Regras e Arbitragem ⚖️"):
        st.session_state.tema = "regras"
    if st.button("Graduações e Faixas 🎖️"):
        st.session_state.tema = "graduacoes"
    if st.button("História e Projeto Resgate 📜"):
        st.session_state.tema = "historia"
    st.stop()

# =====================================================
# INÍCIO DO QUIZ
# =====================================================
tema = st.session_state.tema
lista = perguntas[tema]
total = len(lista)
pergunta_atual = lista[st.session_state.indice]

st.markdown(f"### Tema: {tema.capitalize()}")
st.markdown(f"**Pergunta {st.session_state.indice + 1} de {total}**")

# Exibe imagem se existir
if os.path.exists(pergunta_atual["imagem"]):
    img = Image.open(pergunta_atual["imagem"])
    st.image(img, width=400)

# Pergunta e opções
st.write(f"**{pergunta_atual['pergunta']}**")

opcao = st.radio("Escolha sua resposta:", pergunta_atual["opcoes"], index=None)

if st.button("Responder"):
    if opcao == pergunta_atual["resposta"]:
        st.success("✅ Correto!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Errado! A resposta certa era: **{pergunta_atual['resposta']}**")

    st.session_state.indice += 1
    if st.session_state.indice >= total:
        st.balloons()
        st.success(f"🏁 Fim do Quiz! Você acertou {st.session_state.score} de {total} perguntas.")
        if st.button("🔁 Jogar novamente"):
            st.session_state.tema = None
            st.session_state.indice = 0
            st.session_state.score = 0
        st.stop()
    else:
        st.rerun()
