# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from fpdf import FPDF
import qrcode
import time # Para simular o exponencial backoff no mock

# =========================================
# 1. MOCKS DE DEPENDÊNCIAS (Para tornar o código rodável)
# =========================================

# Mock para a conexão com o banco de dados (Firestore)
def get_db():
    class MockDB:
        def collection(self, name):
            # Simulando o objeto de coleção para fins de contagem
            class MockCollection:
                def count(self):
                    class MockCount:
                        def get(self):
                            # Retorna o mock de resultado de contagem: total = 41
                            return [[type('MockAggregation', (object,), {'value': 41})()]]
                    return MockCount()
            return MockCollection()
    return MockDB()

# =========================================
# 2. FUNÇÕES AUXILIARES
# =========================================

def gerar_codigo_verificacao():
    """Gera código no formato BJJDIGITAL-{ANO}-{SEQUENCIA}"""
    try:
        # Mock do banco de dados - usa get_db()
        db = get_db() 
        # Tenta simular a contagem (deve retornar 41 do mock)
        docs = db.collection('resultados').count().get()
        total = docs[0][0].value  
    except Exception as e:
        # Fallback: Gera um número aleatório se não conseguir conectar (cai aqui se o mock falhar)
        print(f"Alerta: Usando fallback de código aleatório devido ao erro: {e}")
        total = random.randint(1000, 9999)
    
    # Sequência será total + 1 (41 + 1 = 42)
    sequencia = total + 1
    ano_atual = datetime.now().year
    
    # Formato: BJJDIGITAL-2025-0042
    return f"BJJDIGITAL-{ano_atual}-{sequencia:04d}"

def gerar_qrcode(codigo):
    """Gera um QR Code para o código de verificação e salva temporariamente."""
    
    # Cria a pasta temporária 'temp' se não existir
    os.makedirs("temp", exist_ok=True)
    caminho_qr = f"temp/qr_{codigo}.png"
    
    # Evita gerar o QR code se ele já existir (para otimização)
    if os.path.exists(caminho_qr): return caminho_qr

    base_url = "https://bjjdigital.com.br/verificar"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"{base_url}?codigo={codigo}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Salva no caminho temporário
    img.save(caminho_qr) 
    return caminho_qr

# =========================================
# 3. PDF PREMIUM (DARK MODE / DOURADO) - CÓDIGO REPLICADO E AJUSTADO
# =========================================
# Removida a decoração @st.cache_data para evitar dependência do Streamlit
def gerar_pdf(usuario_nome, faixa, pontuacao, total, codigo, professor=None):
    """
    Gera o certificado PDF em modo paisagem (A4) replicando o layout da imagem.
    
    Ajustes de layout:
    - Uso de cor escura para a barra lateral (Dark Olive).
    - Inclusão de placeholders para o emblema e data de emissão na barra lateral.
    - Posicionamento e rotação do placeholder [LOGO_EQUIPE].
    - Ajuste fino da área de texto principal e centralização.
    - Posicionamento do QR Code e código de verificação no canto inferior direito.
    """
    try:
        # Configuração do Documento
        pdf = FPDF("L", "mm", "A4")
        pdf.set_auto_page_break(False)
        pdf.add_page()
        
        # Cores baseadas na imagem (Dark Mode / Dourado)
        cor_dourado = (184, 134, 11)  # Gold
        cor_preto_fundo = (20, 40, 30) # Dark Olive/Greenish Black para a barra
        cor_preto_texto = (25, 25, 25) # Preto para o texto principal
        cor_cinza = (100, 100, 100)
        cor_fundo = (252, 252, 250) # Fundo branco/quase branco

        # Fundo principal (branco/off-white)
        pdf.set_fill_color(*cor_fundo)
        pdf.rect(0, 0, 297, 210, "F")

        # Barra Lateral Esquerda (Dark Mode)
        largura_barra = 28 # Ajustado para encaixar os elementos
        pdf.set_fill_color(*cor_preto_fundo)
        pdf.rect(0, 0, largura_barra, 210, "F")
        
        # Linha separadora Dourada (2mm de largura)
        pdf.set_fill_color(*cor_dourado)
        pdf.rect(largura_barra, 0, 2, 210, "F")

        # Configuração da Área de Texto Principal
        # Início X na área principal (30mm da borda esquerda)
        x_inicio = largura_barra + 15  
        largura_util = 297 - x_inicio - 15  # Largura da área de texto
        centro_x_util = x_inicio + (largura_util / 2) # Ponto central da área de texto

        # ----------------------------------------------------
        # Elementos da Barra Esquerda
        # ----------------------------------------------------
        
        # Placeholder Logo Superior (usando a posição da imagem original)
        pdf.set_xy(5, 20)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(18, 5, "BJJ DIGITAL", 0, 0, "C")
        
        # Placeholder Emblema Inferior (Coin) - Centralizado na barra
        pdf.set_xy(0, 175)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*cor_dourado)
        pdf.cell(largura_barra, 5, "[EMBLEMA DOURADO]", 0, 0, "C")
        
        # Data de Emissão - Alinhado à esquerda na barra
        pdf.set_xy(5, 200) # x=5 para uma margem interna
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(200, 200, 200) # Cinza claro
        data_emissao = datetime.now().strftime("%d/%m/%Y")
        pdf.cell(largura_barra - 5, 5, f"Data de Emissão: {data_emissao}", 0, 0, "L")
        
        # ----------------------------------------------------
        # Elementos da Área Principal
        # ----------------------------------------------------
        
        # 1. Título Principal
        pdf.set_y(45) 
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(*cor_dourado)
        titulo = "CERTIFICADO DE EXAME TEÓRICO DE FAIXA"
        
        pdf.set_x(x_inicio) 
        pdf.cell(largura_util, 12, titulo, 0, 1, "C") # Centralizado
        
        pdf.ln(20) # Espaço grande após o título
        
        # 2. Placeholder LOGO_EQUIPE (Rotacionado)
        y_logo_equipe = pdf.get_y() - 10 
        x_logo_equipe = centro_x_util + 40 # Posição no quadrante superior direito

        pdf.set_xy(x_logo_equipe, y_logo_equipe)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(255, 0, 0) # Cor vermelha para o placeholder
        
        # Rotaciona 30 graus no ponto (x_logo_equipe, y_logo_equipe)
        pdf.rotate(30, x_logo_equipe, y_logo_equipe) 
        pdf.cell(50, 5, "[LOGO_EQUIPE]", 0, 0, "C")
        pdf.rotate(0) # Volta a rotação
        
        # 3. Textos e Nome
        pdf.set_y(y_logo_equipe + 30) # Posição após a área do logo rotacionado
        
        # Texto Introdutório - "Certificamos que o aluno(a)"
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto_texto)
        pdf.set_x(x_inicio)
        pdf.cell(largura_util, 10, "Certificamos que o aluno(a)", 0, 1, "C")

        # Nome do Aluno - Em negrito e destaque
        pdf.ln(8)
        try:  
            nome_limpo = usuario_nome.upper().encode('latin-1', 'replace').decode('latin-1')
        except:  
            nome_limpo = usuario_nome.upper()

        # Ajuste de tamanho para o nome (mantido do seu código original)
        tamanho_fonte = 28
        largura_maxima_nome = largura_util - 40
        while True:
            pdf.set_font("Helvetica", "B", tamanho_fonte)
            largura_texto = pdf.get_string_width(nome_limpo)
            if largura_texto <= largura_maxima_nome or tamanho_fonte <= 16:
                break
            tamanho_fonte -= 1

        pdf.set_text_color(*cor_dourado)
        pdf.set_x(x_inicio)
        pdf.cell(largura_util, 14, nome_limpo, 0, 1, "C")

        pdf.ln(10) 
        
        # Texto de Aprovação - Linha combinada da imagem
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto_texto)
        texto_aprovacao = "foi APROVADO(A) no Exame teórico para a faixa estando apto(a) a ser provido(a) a faixa:"
        pdf.set_x(x_inicio)
        # MultiCell para quebrar a linha automaticamente se for muito longa
        pdf.multi_cell(largura_util, 8, texto_aprovacao, 0, "C") 
        
        pdf.ln(15)

        # Faixa - Em destaque
        pdf.set_font("Helvetica", "B", 32)
        pdf.set_text_color(*cor_preto_texto)
        texto_faixa = f"{str(faixa).upper()}" # Usando o valor da variável 'faixa'
        
        pdf.set_x(x_inicio)
        pdf.cell(largura_util, 16, texto_faixa, 0, 1, "C")

        # 4. Rodapé com assinatura
        y_rodape_linha = 175 # Posição da linha de assinatura
        
        pdf.set_y(y_rodape_linha)
        
        # Centralização da linha e texto
        largura_linha_assinatura = 80
        x_assinatura = centro_x_util - (largura_linha_assinatura / 2) 
        
        # Linha da assinatura
        pdf.set_draw_color(*cor_preto_texto)
        pdf.set_line_width(0.3)
        pdf.line(x_assinatura, y_rodape_linha, x_assinatura + largura_linha_assinatura, y_rodape_linha)
        
        # Nome do professor (ou placeholder) - Acima da linha na imagem
        pdf.set_xy(x_assinatura, y_rodape_linha - 12)
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(*cor_preto_texto)
        pdf.cell(largura_linha_assinatura, 5, professor or "{nome_do_professor}", align="C")
        
        # Texto "Professor Responsável" - Abaixo da linha na imagem
        pdf.set_xy(x_assinatura, y_rodape_linha + 2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*cor_cinza)
        pdf.cell(largura_linha_assinatura, 5, "Professor Responsável", align="C")

        # 5. QR Code e Código de Verificação (Bottom Right)
        
        qr_size = 25 # Tamanho do quadrado do QR
        qr_margin_bottom = 10 
        qr_margin_right = 10
        x_qr = 297 - qr_size - qr_margin_right 
        y_qr = 210 - qr_size - qr_margin_bottom 
        
        caminho_qr = gerar_qrcode(codigo)
        
        # Adiciona a imagem do QR Code
        if os.path.exists(caminho_qr):
            pdf.image(caminho_qr, x=x_qr, y=y_qr, w=qr_size)

        # Texto do Código de Verificação (abaixo do QR)
        pdf.set_xy(x_qr, y_qr + qr_size + 2)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*cor_cinza)
        pdf.cell(qr_size, 4, codigo, align="R") # Alinha à direita

        # Retorna o PDF como bytes
        return pdf.output(dest='S').encode('latin-1'), f"Certificado_{usuario_nome.split()[0]}.pdf"
    except Exception as e:
        # Aumentei o print para ver o erro em mais detalhes
        print(f"Erro ao gerar PDF: {e}")
        return None, None

# =========================================
# 4. EXEMPLO DE EXECUÇÃO
# =========================================

if __name__ == "__main__":
    # Dados de Exemplo
    NOME_ALUNO = "João Pedro da Silva"
    FAIXA_ATUAL = "Faixa Azul"
    PONTUACAO_EXAME = 95
    TOTAL_PONTOS = 100
    NOME_PROFESSOR = "Mestre Carlos Gracie Jr."
    
    # Gera o código e o QR Code
    CODIGO_VERIFICACAO = gerar_codigo_verificacao()
    print(f"Código de Verificação Gerado: {CODIGO_VERIFICACAO}")
    
    # Gera o PDF
    pdf_bytes, filename = gerar_pdf(
        usuario_nome=NOME_ALUNO, 
        faixa=FAIXA_ATUAL, 
        pontuacao=PONTUACAO_EXAME, 
        total=TOTAL_PONTOS, 
        codigo=CODIGO_VERIFICACAO, 
        professor=NOME_PROFESSOR
    )
    
    # Salva o arquivo localmente para visualização (opcional)
    if pdf_bytes:
        with open(filename, "wb") as f:
            f.write(pdf_bytes)
        print(f"Certificado gerado com sucesso: {filename}")
    
    # Limpa o QR Code temporário
    try:
        qr_path = f"temp/qr_{CODIGO_VERIFICACAO}.png"
        if os.path.exists(qr_path):
            os.remove(qr_path)
    except Exception as e:
        print(f"Não foi possível remover o arquivo QR temporário: {e}")
