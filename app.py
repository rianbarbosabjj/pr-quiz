import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random

# =====================================================
# PALETA DE CORES (baseada no site GFTeam IAPC de Irajá)
# =====================================================
COR_FUNDO = "#0e2d26"       # verde escuro do fundo
COR_PAINEL = "#0a211d"      # verde mais fechado
COR_TEXTO = "#FFFFFF"       # texto principal
COR_TEXTO_SUAVE = "#CCCCCC" # texto secundário
COR_DESTAQUE = "#FFD700"    # dourado dos títulos
COR_BOTAO = "#078B6C"       # verde GFTeam dos botões
COR_HOVER = "#FFD700"       # hover dourado
COR_ACERTO = "#4CAF50"      # verde de acerto
COR_ERRO = "#B22222"        # vermelho de erro

# =====================================================
# FUNÇÃO PARA ENCONTRAR IMAGEM
# =====================================================
def encontrar_imagem(base_path):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        caminho = base_path + ext
        if os.path.exists(caminho):
            return caminho
    return None

# =====================================================
# PERGUNTAS SEPARADAS POR TEMA
# =====================================================
perguntas = {
    "regras": [
        {"nivel": 1, "imagem": "imagens/inicio_luta", "pergunta": "Quando o árbitro estende o braço à frente e faz movimento vertical em direção ao solo, o que ele indica?", "opcoes": ["A) Parar a luta", "B) Início da luta", "C) Punição", "D) Declaração do vencedor"], "resposta": "B"},
        {"nivel": 1, "imagem": "imagens/parar_luta", "pergunta": "O que significa o gesto do árbitro?", "opcoes": ["A) Punição", "B) Parar a luta", "C) Ponto para ambos", "D) Desclassificação"], "resposta": "B"},
        {"nivel": 1, "imagem": "imagens/dois_pontos", "pergunta": "O árbitro ergue dois dedos (indicador e médio). O que significa?", "opcoes": ["A) Duas vantagens", "B) Dois pontos (queda, raspagem ou joelho na barriga)", "C) Punição dupla", "D) Pedido de médico"], "resposta": "B"},
        {"nivel": 2, "imagem": "imagens/topo", "pergunta": "Quantos pontos são concedidos pela passagem de guarda estabilizada?", "opcoes": ["A) 2 pontos", "B) 3 pontos", "C) 4 pontos", "D) Apenas vantagem"], "resposta": "B"},
        {"nivel": 2, "imagem": "imagens/cronometro", "pergunta": "O árbitro deve contar quantos segundos de estabilização para validar uma posição de pontuação?", "opcoes": ["A) 2 segundos", "B) 3 segundos", "C) 5 segundos", "D) 10 segundos"], "resposta": "B"},
        {"nivel": 3, "imagem": "imagens/Punicao", "pergunta": "Qual é a sequência de punições para faltas graves?", "opcoes": ["A) 1ª – vantagem; 2ª – pontos; 3ª – desclassificação", "B) 1ª – aviso; 2ª – vantagem ao oponente; 3ª – 2 pontos; 4ª – desclassificação", "C) 1ª – advertência; 2ª – reinício em pé; 3ª – expulsão", "D) 1ª – vantagem; 2ª – vantagem; 3ª – desclassificação"], "resposta": "B"}
    ],

    "graduacoes": [
        {"nivel": 1, "imagem": "imagens/faixas", "pergunta": "Qual é a ordem correta das faixas no jiu-jitsu adulto?", "opcoes": ["A) Branca, Azul, Roxa, Marrom, Preta", "B) Azul, Branca, Roxa, Marrom, Preta", "C) Branca, Roxa, Azul, Marrom, Preta", "D) Branca, Azul, Preta, Marrom"], "resposta": "A"},
        {"nivel": 2, "imagem": "imagens/faixa_preta", "pergunta": "Após quantos graus na faixa preta o atleta se torna faixa coral?", "opcoes": ["A) 4º grau", "B) 5º grau", "C) 6º grau", "D) 7º grau"], "resposta": "D"},
        {"nivel": 3, "imagem": "imagens/faixa_vermelha", "pergunta": "A faixa vermelha é atribuída a mestres com quantos anos de prática e contribuição?", "opcoes": ["A) 20 anos", "B) 30 anos", "C) 40 anos", "D) 50 anos"], "resposta": "C"}
    ],

    "historia": [
        {"nivel": 1, "imagem": "imagens/historia_jj", "pergunta": "Quem é considerado o precursor do jiu-jitsu brasileiro?", "opcoes": ["A) Rickson Gracie", "B) Mitsuyo Maeda (Conde Koma)", "C) Helio Gracie", "D) Carlos Gracie"], "resposta": "B"},
        {"nivel": 2, "imagem": "imagens/gracie_family", "pergunta": "Qual família popularizou o jiu-jitsu no Brasil?", "opcoes": ["A) Nogueira", "B) Gracie", "C) Machado", "D) Silva"], "resposta": "B"},
        {"nivel": 3, "imagem": "imagens/projeto_resgate", "pergunta": "O Projeto Resgate GFTeam IAPC de Irajá tem como missão:", "opcoes": ["A) Ensinar apenas competição", "B) Promover o jiu-jitsu como ferramenta de transformação social", "C) Formar atletas profissionais exclusivamente", "D) Focar em lutas internacionais"], "resposta": "B"}
    ]
}

# =====================================================
# CLASSE PRINCIPAL DO JOGO
# =====================================================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🥋 Quiz do Projeto Resgate GFTeam IAPC de Irajá")

        largura = self.root.winfo_screenwidth()
        altura = self.root.winfo_screenheight()
        self.root.geometry(f"{int(largura*0.9)}x{int(altura*0.9)}")
        self.root.configure(bg=COR_FUNDO)
        self.root.resizable(True, True)

        self.tema_atual = None
        self.score = 0
        self.q_index = 0
        self.nivel_atual = 1

        self.tela_inicial()

    # =====================================================
    # TELA INICIAL
    # =====================================================
    def tela_inicial(self):
        self.tela_inicial = tk.Frame(self.root, bg=COR_FUNDO)
        self.tela_inicial.pack(fill="both", expand=True)

        titulo = tk.Label(self.tela_inicial, text="🥋 Quiz do Projeto Resgate",
                          font=("Poppins", 32, "bold"), fg=COR_DESTAQUE, bg=COR_FUNDO)
        titulo.pack(pady=40)

        subtitulo = tk.Label(self.tela_inicial,
                             text="Escolha o tema e mostre seus conhecimentos sobre o Jiu-Jitsu!",
                             font=("Poppins", 16), fg=COR_TEXTO, bg=COR_FUNDO)
        subtitulo.pack(pady=10)

        caminho_logo = encontrar_imagem("imagens/logo_projeto_resgate") or encontrar_imagem("imagens/topo")
        if caminho_logo:
            largura_tela = self.root.winfo_screenwidth()
            altura_tela = self.root.winfo_screenheight()
            largura_img = int(largura_tela * 0.4)
            altura_img = int(altura_tela * 0.4)
            logo = Image.open(caminho_logo).resize((largura_img, altura_img), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo)
            tk.Label(self.tela_inicial, image=self.logo_tk, bg=COR_FUNDO).pack(pady=20)

        tk.Button(self.tela_inicial, text="🏁 Escolher Tema",
                  font=("Poppins", 18, "bold"), bg=COR_BOTAO, fg=COR_TEXTO,
                  activebackground=COR_HOVER, activeforeground=COR_FUNDO,
                  padx=40, pady=15, borderwidth=0, relief="ridge",
                  command=self.tela_tema).pack(pady=40)

    # =====================================================
    # TELA DE SELEÇÃO DE TEMA
    # =====================================================
    def tela_tema(self):
        self.tela_inicial.destroy()
        self.tela_tema = tk.Frame(self.root, bg=COR_FUNDO)
        self.tela_tema.pack(fill="both", expand=True)

        tk.Label(self.tela_tema, text="🥋 Escolha seu Desafio",
                 font=("Poppins", 28, "bold"), fg=COR_DESTAQUE, bg=COR_FUNDO).pack(pady=40)

        temas = {
            "Regras e Arbitragem": "regras",
            "Graduações e Faixas": "graduacoes",
            "História e Projeto Resgate": "historia"
        }

        for texto, chave in temas.items():
            tk.Button(self.tela_tema, text=texto,
                      font=("Poppins", 16, "bold"),
                      bg=COR_BOTAO, fg=COR_TEXTO,
                      activebackground=COR_HOVER, activeforeground=COR_FUNDO,
                      padx=40, pady=15, borderwidth=0, relief="ridge",
                      command=lambda c=chave: self.iniciar_quiz(c)).pack(pady=20)

    # =====================================================
    # INICIAR QUIZ
    # =====================================================
    def iniciar_quiz(self, tema):
        self.tema_atual = tema
        self.tela_tema.destroy()
        self.score = 0
        self.q_index = 0
        self.nivel_atual = 1
        self.carregar_perguntas()

    # =====================================================
    # CARREGAR PERGUNTAS E INTERFACE
    # =====================================================
    def carregar_perguntas(self):
        self.perguntas_nivel = [p for p in perguntas[self.tema_atual] if p["nivel"] == self.nivel_atual]
        random.shuffle(self.perguntas_nivel)

        for widget in self.root.winfo_children():
            widget.destroy()

        self.img_label = tk.Label(self.root, bg=COR_FUNDO)
        self.img_label.pack(pady=20)

        self.titulo_label = tk.Label(self.root,
                                     text=f"Tema: {self.tema_atual.capitalize()} | Nível {self.nivel_atual} de 3",
                                     font=("Poppins", 18, "bold"), fg=COR_DESTAQUE, bg=COR_FUNDO)
        self.titulo_label.pack()

        self.pergunta_label = tk.Label(self.root, text="", font=("Poppins", 14),
                                       wraplength=900, justify="center", fg=COR_TEXTO, bg=COR_FUNDO)
        self.pergunta_label.pack(pady=20)

        self.botoes = []
        for i in range(4):
            btn = tk.Button(self.root, text="", width=60, height=2,
                            font=("Poppins", 12),
                            bg=COR_BOTAO, fg=COR_TEXTO,
                            activebackground=COR_HOVER, activeforeground=COR_FUNDO,
                            borderwidth=0, relief="ridge",
                            command=lambda i=i: self.verificar_resposta(i))
            btn.pack(pady=5)
            self.botoes.append(btn)

        self.status_label = tk.Label(self.root, text="", font=("Poppins", 12),
                                     fg=COR_TEXTO_SUAVE, bg=COR_FUNDO)
        self.status_label.pack(pady=10)

        self.carregar_pergunta()

    def carregar_pergunta(self):
        if self.q_index >= len(self.perguntas_nivel):
            if self.nivel_atual < 3:
                self.mostrar_tela_transicao()
            else:
                self.fim_do_jogo()
            return

        q = self.perguntas_nivel[self.q_index]
        caminho_img = encontrar_imagem(q["imagem"])

        if caminho_img:
            img = Image.open(caminho_img).resize((420, 260))
            self.photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.photo)
            self.img_label.image = self.photo
        else:
            self.img_label.config(image="", text="(Imagem não encontrada)")

        self.pergunta_label.config(text=q["pergunta"])
        for i, opcao in enumerate(q["opcoes"]):
            self.botoes[i].config(text=opcao)

        self.status_label.config(
            text=f"Nível {self.nivel_atual} | Pergunta {self.q_index + 1} de {len(self.perguntas_nivel)} | Pontos: {self.score}"
        )

    # =====================================================
    # TELA DE TRANSIÇÃO ENTRE NÍVEIS
    # =====================================================
    def mostrar_tela_transicao(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tela = tk.Frame(self.root, bg=COR_FUNDO)
        tela.pack(fill="both", expand=True)

        msg = tk.Label(
            tela,
            text=f"🎉 Parabéns!\nVocê completou o Nível {self.nivel_atual}!",
            font=("Poppins", 26, "bold"), fg=COR_DESTAQUE, bg=COR_FUNDO
        )
        msg.pack(pady=40)

        caminho_img = encontrar_imagem(f"imagens/nivel_{self.nivel_atual}_concluido") or encontrar_imagem("imagens/parabens")
        if caminho_img:
            largura_tela = self.root.winfo_screenwidth()
            altura_tela = self.root.winfo_screenheight()
            largura_img = int(largura_tela * 0.3)
            altura_img = int(altura_tela * 0.3)

            img = Image.open(caminho_img).resize((largura_img, altura_img), Image.Resampling.LANCZOS)
            self.transicao_img = ImageTk.PhotoImage(img)
            tk.Label(tela, image=self.transicao_img, bg=COR_FUNDO).pack(pady=20)

        tk.Button(
            tela, text="👉 Continuar para o próximo nível",
            font=("Poppins", 16, "bold"), bg=COR_BOTAO, fg=COR_TEXTO,
            activebackground=COR_HOVER, activeforeground=COR_FUNDO,
            padx=30, pady=12, borderwidth=0, relief="ridge",
            command=lambda: self.avancar_nivel(tela)
        ).pack(pady=40)

    def avancar_nivel(self, tela):
        tela.destroy()
        self.nivel_atual += 1
        self.q_index = 0
        self.carregar_perguntas()

    # =====================================================
    # VERIFICAR RESPOSTAS
    # =====================================================
    def verificar_resposta(self, i):
        q = self.perguntas_nivel[self.q_index]
        resposta_escolhida = q["opcoes"][i][0]
        if resposta_escolhida == q["resposta"]:
            self.score += 1
            messagebox.showinfo("✅ Correto!", "Boa! Você acertou.")
        else:
            messagebox.showwarning("❌ Errado!", f"A resposta certa era {q['resposta']}.")
        self.q_index += 1
        self.carregar_pergunta()

    # =====================================================
    # TELA FINAL
    # =====================================================
    def fim_do_jogo(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        resultado = tk.Label(self.root,
                             text=f"🏁 Fim de jogo!\nVocê acertou {self.score} de {len(perguntas[self.tema_atual])} perguntas.",
                             font=("Poppins", 18, "bold"),
                             fg=COR_DESTAQUE, bg=COR_FUNDO)
        resultado.pack(pady=50)

        faixa = (
            "Faixa Branca 🥋" if self.score <= 4 else
            "Faixa Azul 💙" if self.score <= 7 else
            "Faixa Roxa 💜" if self.score <= 9 else
            "Faixa Marrom 🤎" if self.score <= 11 else
            "Faixa Preta 🖤"
        )

        tk.Label(self.root, text=faixa,
                 font=("Poppins", 20, "bold"),
                 fg=COR_TEXTO, bg=COR_FUNDO).pack()

        tk.Button(self.root, text="🔁 Jogar novamente",
                  font=("Poppins", 14, "bold"),
                  bg=COR_BOTAO, fg=COR_TEXTO,
                  activebackground=COR_HOVER, activeforeground=COR_FUNDO,
                  padx=20, pady=10, borderwidth=0, relief="ridge",
                  command=self.reiniciar).pack(pady=30)

    def reiniciar(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)

# =====================================================
# EXECUÇÃO
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
