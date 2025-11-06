# ============================================================
# TESTE DE CONHECIMENTOS - PROJETO RESGATE | GFTEAM IAPC IRAJÁ
# Versão protótipo responsiva (PC + celular) - Streamlit
# ============================================================

import streamlit as st
import random

# ------------------ CONFIGURAÇÕES GERAIS ---------------------
st.set_page_config(
    page_title="Teste de Conhecimentos - Projeto Resgate | GFTeam IAPC de Irajá",
    page_icon="🥋",
    layout="centered"
)

# Paleta de cores
COR_FUNDO = "#0e2d26"       # verde escuro do fundo
COR_DESTAQUE = "#FFD700"    # dourado dos títulos
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#078B6C"

# ------------------ ESTILO CSS PERSONALIZADO -----------------
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {COR_FUNDO};
        }}
        h1, h2, h3, h4, h5, h6, p, li {{
            color: {COR_TEXTO};
        }}
        .titulo {{
            text-align: center;
            color: {COR_DESTAQUE};
            font-weight: bold;
        }}
        .pergunta {{
            font-size: 1.2rem;
            margin-top: 20px;
        }}
        .stButton>button {{
            background-color: {COR_BOTAO};
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            width: 100%;
            height: 3em;
        }}
        .stButton>button:hover {{
            background-color: {COR_DESTAQUE};
            color: {COR_FUNDO};
        }}
    </style>
""", unsafe_allow_html=True)

# ------------------ BANCO DE PERGUNTAS -----------------------
perguntas = {
    "História": [
        {"nivel": 1, "pergunta": "O jiu-jitsu tem origem em qual país?",
         "opcoes": ["Japão", "China", "Brasil", "Índia"], "resposta": "Japão"},
        {"nivel": 1, "pergunta": "Quem é considerado o introdutor do jiu-jitsu no Brasil?",
         "opcoes": ["Jigoro Kano", "Mitsuyo Maeda", "Hélio Gracie", "Carlos Gracie"], "resposta": "Mitsuyo Maeda"},
        {"nivel": 2, "pergunta": "Qual membro da família Gracie adaptou o jiu-jitsu para pessoas mais leves e fracas?",
         "opcoes": ["Hélio Gracie", "Rorion Gracie", "Rickson Gracie", "Royce Gracie"], "resposta": "Hélio Gracie"},
        {"nivel": 3, "pergunta": "Em qual cidade Mitsuyo Maeda começou a ensinar jiu-jitsu no Brasil?",
         "opcoes": ["São Paulo", "Belém do Pará", "Rio de Janeiro", "Manaus"], "resposta": "Belém do Pará"}
    ],
    "Regras": [
        {"nivel": 1, "pergunta": "Quantos pontos valem uma raspagem bem executada?",
         "opcoes": ["2 pontos", "3 pontos", "4 pontos", "Apenas vantagem"], "resposta": "2 pontos"},
        {"nivel": 2, "pergunta": "Quantos segundos o atleta deve estabilizar uma posição para marcar pontos?",
         "opcoes": ["2 segundos", "3 segundos", "5 segundos", "10 segundos"], "resposta": "3 segundos"},
        {"nivel": 3, "pergunta": "Qual é a sequência de punições para faltas graves?",
         "opcoes": ["Aviso → Vantagem → 2 pontos → Desclassificação", "Punição direta", "Três avisos e expulsão", "Nenhuma das anteriores"],
         "resposta": "Aviso → Vantagem → 2 pontos → Desclassificação"}
    ],
    "Graduações": [
        {"nivel": 1, "pergunta": "Qual é a sequência correta das faixas no jiu-jitsu adulto?",
         "opcoes": ["Branca, Azul, Roxa, Marrom, Preta", "Azul, Roxa, Marrom, Preta, Coral", "Branca, Roxa, Azul, Marrom, Preta", "Branca, Azul, Preta, Marrom"], "resposta": "Branca, Azul, Roxa, Marrom, Preta"},
        {"nivel": 2, "pergunta": "Após quantos graus na faixa preta o atleta se torna faixa coral?",
         "opcoes": ["4º grau", "5º grau", "6º grau", "7º grau"], "resposta": "7º grau"},
        {"nivel": 3, "pergunta": "A faixa vermelha é atribuída a mestres com quantos anos de prática?",
         "opcoes": ["20 anos", "30 anos", "40 anos", "50 anos"], "resposta": "40 anos"}
    ]
}

# ------------------ INÍCIO DO APP ----------------------------
st.markdown("<h1 class='titulo'>🥋 Teste de Conhecimentos<br>Projeto Resgate | GFTeam IAPC de Irajá</h1>", unsafe_allow_html=True)
st.markdown("---")

if "fase" not in st.session_state:
    st.session_state.fase = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "tema" not in st.session_state:
    st.session_state.tema = None
if "pontuacao" not in st.session_state:
    st.session_state.pontuacao = 0

# ------------------ TELA DE LOGIN SIMULADO -------------------
if st.session_state.fase == "login":
    nome = st.text_input("Digite seu nome para começar:")
    if st.button("Entrar no Quiz"):
        if nome.strip():
            st.session_state.usuario = nome.strip().title()
            st.session_state.fase = "menu"
            st.rerun()
        else:
            st.warning("Por favor, digite um nome válido.")

# ------------------ MENU PRINCIPAL ---------------------------
elif st.session_state.fase == "menu":
    st.markdown(f"👋 Olá, **{st.session_state.usuario}**! Escolha um tema para começar o desafio.")
    tema = st.selectbox("Selecione o tema:", list(perguntas.keys()))
    if st.button("Iniciar Jogo"):
        st.session_state.tema = tema
        st.session_state.pontuacao = 0
        st.session_state.perguntas_tema = random.sample(perguntas[tema], len(perguntas[tema]))
        st.session_state.q_index = 0
        st.session_state.fase = "quiz"
        st.rerun()

# ------------------ TELA DO QUIZ -----------------------------
elif st.session_state.fase == "quiz":
    tema_atual = st.session_state.tema
    questoes = st.session_state.perguntas_tema
    q_index = st.session_state.q_index

    if q_index < len(questoes):
        q = questoes[q_index]
        st.markdown(f"### Pergunta {q_index + 1} de {len(questoes)} (Nível {q['nivel']})")
        st.markdown(f"<div class='pergunta'>{q['pergunta']}</div>", unsafe_allow_html=True)
        resposta = st.radio("Escolha uma opção:", q["opcoes"], key=f"resp_{q_index}")

        if st.button("Responder"):
            if resposta == q["resposta"]:
                st.success("✅ Resposta correta!")
                st.session_state.pontuacao += 1
            else:
                st.error(f"❌ Resposta incorreta. A correta era: **{q['resposta']}**")
            st.session_state.q_index += 1
            st.rerun()
    else:
        st.session_state.fase = "resultado"
        st.rerun()

# ------------------ RESULTADO FINAL --------------------------
elif st.session_state.fase == "resultado":
    st.markdown("## 🏁 Fim do Teste!")
    st.markdown(f"**{st.session_state.usuario}**, você acertou **{st.session_state.pontuacao}** de **{len(st.session_state.perguntas_tema)}** perguntas.")
    
    faixa = (
        "Faixa Branca 🥋" if st.session_state.pontuacao <= 2 else
        "Faixa Azul 💙" if st.session_state.pontuacao <= 4 else
        "Faixa Roxa 💜" if st.session_state.pontuacao <= 6 else
        "Faixa Marrom 🤎" if st.session_state.pontuacao <= 8 else
        "Faixa Preta 🖤"
    )
    st.markdown(f"### Seu nível atual: **{faixa}**")

    if st.button("🔁 Jogar Novamente"):
        st.session_state.fase = "menu"
        st.rerun()
