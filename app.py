import streamlit as st
from PIL import Image
import random
import os

# =====================================================
# PALETA DE CORES (GFTeam IAPC de Irajá)
# =====================================================
COR_FUNDO = "#0e2d26"       # verde escuro do fundo
COR_TEXTO = "#FFFFFF"       # texto principal
COR_TEXTO_SUAVE = "#CCCCCC" # texto secundário
COR_DESTAQUE = "#FFD700"    # dourado dos títulos
COR_BOTAO = "#078B6C"       # verde dos botões
COR_HOVER = "#FFD700"       # dourado hover

# =====================================================
# CONFIGURAÇÕES DO APP
# =====================================================
st.set_page_config(
    page_title="🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá",
    layout="centered",
    page_icon="🥋"
)

# =====================================================
# ESTILO PERSONALIZADO
# =====================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {COR_FUNDO};
            color: {COR_TEXTO};
        }}
        h1, h2, h3, h4 {{
            color: {COR_DESTAQUE};
            text-align: center;
            font-weight: bold;
        }}
        .stButton>button {{
            background-color: {COR_BOTAO};
            color: {COR_TEXTO};
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0px 0px 10px rgba(255, 215, 0, 0.3);
        }}
        .stButton>button:hover {{
            background-color: {COR_HOVER};
            color: {COR_FUNDO};
        }}
        .question {{
            font-size: 20px;
            text-align: center;
            color: {COR_TEXTO};
            margin-top: 20px;
            margin-bottom: 15px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# FUNÇÃO PARA MOSTRAR IMAGEM AJUSTADA
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
# PERGUNTAS POR TEMA
# =====================================================
perguntas = {
    "regras": [
        {"nivel": 1, "imagem": "imagens/inicio_luta.png",
         "pergunta": "Quando o árbitro estende o braço à frente e faz movimento vertical em direção ao solo, o que ele indica?",
         "opcoes": ["A) Parar a luta", "B) Início da luta", "C) Punição", "D) Declaração do vencedor"],
         "resposta": "B"},
        {"nivel": 1, "imagem": "imagens/parar_luta.png",
         "pergunta": "O que significa o gesto do árbitro?",
         "opcoes": ["A) Punição", "B) Parar a luta", "C) Ponto para ambos", "D) Desclassificação"],
         "resposta": "B"},
        {"nivel": 1, "imagem": "imagens/dois_pontos.png",
         "pergunta": "O árbitro ergue dois dedos (indicador e médio). O que significa?",
         "opcoes": ["A) Duas vantagens", "B) Dois pontos (queda, raspagem ou joelho na barriga)",
                    "C) Punição dupla", "D) Pedido de médico"],
         "resposta": "B"}
    ],
    "graduacoes": [
        {"nivel": 1, "imagem": "imagens/faixas.png",
         "pergunta": "Qual é a ordem correta das faixas no jiu-jitsu adulto?",
         "opcoes": ["A) Branca, Azul, Roxa, Marrom, Preta",
                    "B) Azul, Branca, Roxa, Marrom, Preta",
                    "C) Branca, Roxa, Azul, Marrom, Preta",
                    "D) Branca, Azul, Preta, Marrom"],
         "resposta": "A"},
        {"nivel": 2, "imagem": "imagens/faixa_preta.png",
         "pergunta": "Após quantos graus na faixa preta o atleta se torna faixa coral?",
         "opcoes": ["A) 4º grau", "B) 5º grau", "C) 6º grau", "D) 7º grau"],
         "resposta": "D"},
        {"nivel": 3, "imagem": "imagens/faixa_vermelha.png",
         "pergunta": "A faixa vermelha é atribuída a mestres com quantos anos de prática e contribuição?",
         "opcoes": ["A) 20 anos", "B) 30 anos", "C) 40 anos", "D) 50 anos"],
         "resposta": "C"}
    ],
    "historia": [
        {"nivel": 1, "imagem": "imagens/historia_jj.png",
         "pergunta": "Quem é considerado o introdutor do jiu-jitsu no Brasil?",
         "opcoes": ["A) Jigoro Kano", "B) Mitsuyo Maeda", "C) Hélio Gracie", "D) Carlos Gracie"],
         "resposta": "B"},
        {"nivel": 2, "imagem": "imagens/gracie_family.png",
         "pergunta": "Qual membro da família Gracie é reconhecido por adaptar o jiu-jitsu para pessoas mais leves?",
         "opcoes": ["A) Hélio Gracie", "B) Rorion Gracie", "C) Rickson Gracie", "D) Royce Gracie"],
         "resposta": "A"},
        {"nivel": 3, "imagem": "imagens/projeto_resgate.png",
         "pergunta": "O Projeto Resgate GFTeam IAPC de Irajá tem como missão:",
         "opcoes": ["A) Ensinar apenas competição",
                    "B) Promover o jiu-jitsu como ferramenta de transformação social",
                    "C) Formar atletas profissionais exclusivamente",
                    "D) Focar em lutas internacionais"],
         "resposta": "B"}
    ]
}

# =====================================================
# ESTADO DO JOGO
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
# TELA INICIAL
# =====================================================
st.title("🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá")
mostrar_imagem("imagens/topo.webp", max_largura=700)

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
# QUIZ
# =====================================================
tema = st.session_state.tema
lista_perguntas = [p for p in perguntas[tema] if p["nivel"] == st.session_state.nivel]
total = len(lista_perguntas)

# Fim de um nível
if st.session_state.indice >= total:
    if st.session_state.nivel < 3:
        st.success(f"🎉 Parabéns! Você completou o Nível {st.session_state.nivel}.")
        mostrar_imagem("imagens/parabens.png", max_largura=500)
        if st.button("👉 Avançar para o próximo nível"):
            st.session_state.nivel += 1
            st.session_state.indice = 0
        st.stop()
    else:
        st.balloons()
        st.markdown(f"<h2>🏁 Fim do jogo!</h2><h3>Você acertou {st.session_state.score} perguntas!</h3>", unsafe_allow_html=True)
        mostrar_imagem("imagens/logo_projeto_resgate.png", max_largura=400)
        if st.button("🔁 Jogar novamente"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
        st.stop()

# Pergunta atual
pergunta_atual = lista_perguntas[st.session_state.indice]

st.markdown(f"### Tema: {tema.capitalize()} | Nível {st.session_state.nivel}")
st.markdown(f"<div class='question'>{pergunta_atual['pergunta']}</div>", unsafe_allow_html=True)
mostrar_imagem(pergunta_atual["imagem"], max_largura=500)

opcao = st.radio("Escolha sua resposta:", pergunta_atual["opcoes"], index=None, label_visibility="collapsed")

if st.button("Responder"):
    if not opcao:
        st.warning("Escolha uma opção antes de continuar!")
    elif opcao[0] == pergunta_atual["resposta"]:
        st.success("✅ Correto!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Errado! A resposta certa era {pergunta_atual['resposta']}.")
    st.session_state.indice += 1
    st.rerun()
