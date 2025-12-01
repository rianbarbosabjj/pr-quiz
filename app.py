import streamlit as st
from fpdf import FPDF
import os
import base64
from streamlit_pdf_viewer import pdf_viewer

# --- CONFIGURAÇÃO DA FONTE ---
# ATENÇÃO: Para usar a fonte 'Allura', você deve ter os arquivos da fonte (ex: Allura.ttf)
# e, idealmente, os arquivos de métrica gerados pelo utilitário FPDF na pasta 'assets/'.
# Se a fonte Allura não carregar, comente as linhas 'pdf.add_font' e use uma fonte padrão.
CUSTOM_FONT_NAME = 'Allura-Regular'
CUSTOM_FONT_FILE = 'assets/Allura-Regular.ttf' # Substitua pelo nome exato do seu arquivo .ttf

# --- 1. FUNÇÃO DE GERAÇÃO DE PDF ---
def gerar_pdf(usuario_nome, faixa, professor=None, cor_dourado_rgb=(184, 134, 11), largura_barra=25, margem_x_conteudo=15, tamanho_titulo=24, posicao_y_titulo=45, posicao_y_nome=70, posicao_y_faixa=120, posicao_x_assinatura=150, posicao_y_assinatura_nome=170, espacamento_titulo=20, incluir_logo=False):
    
    # Cores
    cor_preto = (25, 25, 25)
    cor_cinza = (100, 100, 100)
    cor_fundo = (252, 252, 250)
    cor_dourado = cor_dourado_rgb

    try:
        pdf = FPDF("L", "mm", "A4")
        pdf.set_auto_page_break(False)
        pdf.add_page()
        
        # 1. Carregar Fonte Customizada (Allura)
        # O argumento 'uni=True' é importante para fontes Unicode/TTF
        if os.path.exists(CUSTOM_FONT_FILE):
             # Tenta adicionar a fonte. Se houver erro de metrica, pode falhar.
             try:
                 pdf.add_font(CUSTOM_FONT_NAME, '', CUSTOM_FONT_FILE, uni=True)
             except Exception:
                 st.warning(f"Erro ao carregar a fonte customizada '{CUSTOM_FONT_NAME}'. Usando Helvetica.")
                 CUSTOM_FONT_NAME = 'Helvetica'
                 
        else:
             st.warning(f"Arquivo de fonte '{CUSTOM_FONT_FILE}' não encontrado. Usando Helvetica.")
             CUSTOM_FONT_NAME = 'Helvetica'

        # Fundo e Barra Lateral
        pdf.set_fill_color(*cor_fundo)
        pdf.rect(0, 0, 297, 210, "F")
        pdf.set_fill_color(*cor_preto)
        pdf.rect(0, 0, largura_barra, 210, "F")
        pdf.set_fill_color(*cor_dourado)
        pdf.rect(largura_barra, 0, 2, 210, "F")

        # Logo 
        if incluir_logo and os.path.exists("assets/logo.png"):
            pdf.image("assets/logo.png", x=5, y=20, w=largura_barra - 10) 
        
        # 2. Configuração da Área de Conteúdo (Margem X)
        x_inicio = largura_barra + margem_x_conteudo
        largura_util = 297 - x_inicio - 15 
        centro_x = x_inicio + (largura_util / 2)
        
        # 3. Título Principal (Posição Y ajustável)
        pdf.set_xy(x_inicio, posicao_y_titulo) 
        pdf.set_font("Helvetica", "B", tamanho_titulo)
        pdf.set_text_color(*cor_dourado)
        titulo = "CERTIFICADO DE EXAME TEÓRICO DE FAIXA"
        pdf.cell(largura_util, tamanho_titulo / 2, titulo, ln=1, align="C")
        
        pdf.set_y(pdf.get_y() + espacamento_titulo) # Avança o Y de acordo com o espaçamento
        
        # 4. Bloco de Nome/Texto Introdutório (Posição Y ajustável)
        pdf.set_xy(x_inicio, posicao_y_nome)
        
        # Texto Introdutório
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto)
        texto_intro = "Certificamos que o aluno(a)"
        pdf.cell(largura_util, 10, texto_intro, ln=1, align="C")

        # Nome do Aluno - Em destaque (centralizado dentro da largura útil)
        pdf.ln(8)
        nome_limpo = usuario_nome.upper().encode('latin-1', 'replace').decode('latin-1')
        tamanho_fonte_nome = 28
        pdf.set_font("Helvetica", "B", tamanho_fonte_nome)
        pdf.set_text_color(*cor_dourado)
        pdf.cell(largura_util, 14, nome_limpo, ln=1, align="C") 
        
        pdf.ln(20)

        # Continuação do texto
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto)
        texto_aprovacao = "foi APROVADO(A) no Exame teórico para a faixa"
        pdf.cell(largura_util, 10, texto_aprovacao, ln=1, align="C")
        
        pdf.ln(2)
        texto_apto = "estando apto(a) a ser provido(a) a faixa:"
        pdf.cell(largura_util, 10, texto_apto, ln=1, align="C")

        # 5. Faixa (Posição Y ajustável)
        pdf.set_xy(x_inicio, posicao_y_faixa)
        
        # Linha horizontal acima da Faixa
        largura_linha = 180
        x_linha = centro_x - (largura_linha / 2)
        pdf.set_draw_color(*cor_preto)
        pdf.set_line_width(0.5)
        pdf.line(x_linha, posicao_y_faixa, x_linha + largura_linha, posicao_y_faixa)

        pdf.set_y(posicao_y_faixa + 5) # Espaço de 5mm após a linha
        
        # Faixa - Em destaque
        pdf.set_font("Helvetica", "B", 32)
        pdf.set_text_color(*cor_preto)
        texto_faixa = f"{str(faixa).upper()}"
        pdf.cell(largura_util, 16, texto_faixa, ln=1, align="C")
        
        # --- BLOC DA ASSINATURA ---
        
        # 6. Assinatura do Professor (Nome em Allura) (Posição X e Y ajustável)
        if professor:
            professor_limpo = professor.encode('latin-1', 'replace').decode('latin-1')
            
            # Escreve o nome com a Fonte Allura
            pdf.set_xy(posicao_x_assinatura, posicao_y_assinatura_nome)
            pdf.set_font(CUSTOM_FONT_NAME, '', 20)
            pdf.set_text_color(*cor_preto)
            pdf.cell(0, 10, professor_limpo, ln=1, align="L") # Align L para usar X como ponto de início
            
            # Linha de assinatura
            y_assinatura = pdf.get_y() + 2 # Posição Y da linha logo abaixo do nome
            largura_linha_assinatura = 80
            
            # X da linha é relativo ao X do nome do professor
            x_linha_assinatura = posicao_x_assinatura
            
            pdf.set_draw_color(*cor_preto)
            pdf.set_line_width(0.3)
            pdf.line(x_linha_assinatura, y_assinatura, x_linha_assinatura + largura_linha_assinatura, y_assinatura)
            
            # "Professor Responsável"
            pdf.set_xy(x_linha_assinatura, y_assinatura + 2)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(*cor_cinza)
            pdf.cell(largura_linha_assinatura, 5, "Professor Responsável", align="C")
        
        # Nota: Pontuação/Total/Código foram removidos da função para simplificar e focar no design
        return pdf.output(dest='S').encode('latin-1'), f"Certificado_{usuario_nome.split()[0]}.pdf"
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")
        return None, None

# --- 2. INTERFACE STREAMLIT ---

st.set_page_config(layout="wide", page_title="Editor de Certificado")

st.title("📄 Editor de Certificado FPDF (Streamlit)")

col_config, col_preview = st.columns([1, 2])

with col_config:
    st.header("🛠️ Configurações do Certificado")
    
    st.subheader("Dados Principais")
    # Campos de texto
    nome_aluno = st.text_input("Nome do Aluno:", "Carlos Alberto da Silva Rocha")
    faixa_alvo = st.text_input("Faixa a ser conferida:", "Faixa Roxa")
    professor_nome = st.text_input("Nome para Assinatura:", "M. Kawashima")
    
    st.subheader("Ajustes de Design e Coordenadas")
    
    # Color Picker
    cor_dourado_hex = st.color_picker("Cor de Destaque (Dourado):", "#B8860B")
    h = cor_dourado_hex.lstrip('#')
    cor_dourado_rgb_tuple = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    # Sliders de Layout Geral
    largura_barra_ajuste = st.slider("Largura da Barra Lateral (mm):", 5, 50, 25)
    margem_x_conteudo_ajuste = st.slider("Margem X do Conteúdo (mm):", 5, 50, 15, help="Controla o X de início do bloco de texto após a barra lateral.")
    incluir_logo_check = st.checkbox("Incluir Logo (Requer 'assets/logo.png')", value=False)
    
    st.markdown("---")
    st.subheader("Posicionamento Vertical (Y)")
    
    # Y-Coordinates
    posicao_y_titulo_ajuste = st.slider("Y do Título (mm):", 10, 80, 45)
    posicao_y_nome_ajuste = st.slider("Y do Bloco 'Nome' (mm):", 50, 100, 70, help="Define o Y inicial para o texto introdutório.")
    posicao_y_faixa_ajuste = st.slider("Y do Bloco 'Faixa' (mm):", 100, 160, 120, help="Define o Y da linha horizontal acima da Faixa.")
    
    st.markdown("---")
    st.subheader("Posicionamento da Assinatura")
    
    # X/Y Assinatura
    # Nota: A página A4 Landscape tem 297mm de largura
    posicao_x_assinatura_ajuste = st.slider("X da Assinatura (mm):", 50, 250, 150, help="Define a posição horizontal (X) do nome do professor e da linha.")
    posicao_y_assinatura_nome_ajuste = st.slider("Y do Nome da Assinatura (mm):", 150, 200, 170, help="Define a posição vertical (Y) do nome do professor.")
    
    st.markdown("---")
    st.subheader("Outros Ajustes")
    
    # Outros Sliders
    tamanho_titulo_ajuste = st.slider("Tamanho da Fonte do Título:", 18, 40, 24)
    espacamento_ajuste = st.slider("Espaçamento Vertical (ln) após Título:", 10, 50, 20)

    
# --- Geração e Visualização do PDF ---
pdf_bytes, nome_arquivo = gerar_pdf(
    usuario_nome=nome_aluno, 
    faixa=faixa_alvo, 
    professor=professor_nome,
    cor_dourado_rgb=cor_dourado_rgb_tuple,
    largura_barra=largura_barra_ajuste,
    margem_x_conteudo=margem_x_conteudo_ajuste,
    tamanho_titulo=tamanho_titulo_ajuste,
    posicao_y_titulo=posicao_y_titulo_ajuste,
    posicao_y_nome=posicao_y_nome_ajuste,
    posicao_y_faixa=posicao_y_faixa_ajuste,
    posicao_x_assinatura=posicao_x_assinatura_ajuste,
    posicao_y_assinatura_nome=posicao_y_assinatura_nome_ajuste,
    espacamento_titulo=espacamento_ajuste,
    incluir_logo=incluir_logo_check
)

with col_preview:
    st.header("✨ Pré-visualização")
    
    if pdf_bytes:
        # Usa o componente pdf_viewer para contornar o bloqueio do Chrome
        pdf_viewer(
            input=pdf_bytes,
            width=700,
            height=600
        )
        
        # Botão de download
        st.download_button(
            label="Baixar PDF Gerado",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf"
        )
    else:
        st.warning("Não foi possível gerar o PDF. Verifique os logs de erro.")


