import streamlit as st
from fpdf import FPDF
import os
import base64

# --- 1. FUNÇÃO ORIGINAL (COM PARÂMETROS DE COORDENADAS) ---
def gerar_pdf(usuario_nome, faixa, pontuacao, total, codigo, professor=None, cor_dourado_rgb=(184, 134, 11), largura_barra=25, tamanho_titulo=24, posicao_y_titulo=45, espacamento_titulo=20, incluir_logo=True):
    # Cores baseadas no PDF
    cor_preto = (25, 25, 25)
    cor_cinza = (100, 100, 100)
    cor_fundo = (252, 252, 250)
    
    # Decodifica a tupla RGB do Streamlit
    cor_dourado = cor_dourado_rgb

    try:
        pdf = FPDF("L", "mm", "A4")
        pdf.set_auto_page_break(False)
        pdf.add_page()
        
        # Fundo
        pdf.set_fill_color(*cor_fundo)
        pdf.rect(0, 0, 297, 210, "F")

        # Barra Lateral (largura ajustável)
        pdf.set_fill_color(*cor_preto)
        pdf.rect(0, 0, largura_barra, 210, "F")
        pdf.set_fill_color(*cor_dourado)
        pdf.rect(largura_barra, 0, 2, 210, "F")

        # Logo 
        if incluir_logo and os.path.exists("assets/logo.png"):
            try: 
                pdf.image("assets/logo.png", x=5, y=20, w=largura_barra - 10) 
            except Exception as e:
                pass
        
        # Configuração da Área de Texto
        x_inicio = largura_barra + 15  # Margem maior após a barra
        largura_util = 297 - x_inicio - 15 
        # centro_x não precisa ser alterado, pois depende da largura da área de texto
        
        # Título Principal - Posição Y ajustável
        pdf.set_y(posicao_y_titulo) 
        pdf.set_font("Helvetica", "B", tamanho_titulo)
        pdf.set_text_color(*cor_dourado)
        titulo = "CERTIFICADO DE EXAME TEÓRICO DE FAIXA"
        pdf.cell(largura_util, tamanho_titulo / 2, titulo, ln=1, align="C")
        
        pdf.ln(espacamento_titulo)  # Espaço ajustável
        
        # --- O RESTO DO CÓDIGO PERMANECE O MESMO, MAS ADAPTA-SE À NOVA POSIÇÃO INICIAL DO TÍTULO ---
        
        # Texto Introdutório - Primeira linha
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto)
        texto_intro = "Certificamos que o aluno(a)"
        pdf.cell(largura_util, 10, texto_intro, ln=1, align="C")

        # Nome do Aluno - Em destaque
        pdf.ln(8)
        nome_limpo = usuario_nome.upper().encode('latin-1', 'replace').decode('latin-1')
        
        tamanho_fonte = 28
        largura_maxima_nome = largura_util - 40
        centro_x = x_inicio + (largura_util / 2)
        
        while True:
            pdf.set_font("Helvetica", "B", tamanho_fonte)
            largura_texto = pdf.get_string_width(nome_limpo)
            if largura_texto <= largura_maxima_nome or tamanho_fonte <= 16:
                break
            tamanho_fonte -= 1

        pdf.set_text_color(*cor_dourado)
        x_nome = centro_x - (largura_texto / 2)
        pdf.set_xy(x_nome, pdf.get_y())
        pdf.cell(largura_texto, 14, nome_limpo, align='L')
        
        pdf.ln(20)

        # Continuação do texto
        pdf.set_font("Helvetica", "", 16)
        pdf.set_text_color(*cor_preto)
        texto_aprovacao = "foi APROVADO(A) no Exame teórico para a faixa"
        pdf.cell(largura_util, 10, texto_aprovacao, ln=1, align="C")
        
        pdf.ln(2)
        texto_apto = "estando apto(a) a ser provido(a) a faixa:"
        pdf.cell(largura_util, 10, texto_apto, ln=1, align="C")

        # Linha horizontal
        pdf.ln(15)
        y_linha = pdf.get_y()
        largura_linha = 180
        x_linha = centro_x - (largura_linha / 2)
        pdf.set_draw_color(*cor_preto)
        pdf.set_line_width(0.5)
        pdf.line(x_linha, y_linha, x_linha + largura_linha, y_linha)

        pdf.ln(20)

        # Faixa - Em destaque
        pdf.set_font("Helvetica", "B", 32)
        pdf.set_text_color(*cor_preto)
        texto_faixa = f"{str(faixa).upper()}"
        pdf.cell(largura_util, 16, texto_faixa, ln=1, align="C")

        # Rodapé com assinatura
        y_rodape = 160
        
        if professor:
            pdf.set_y(y_rodape)
            pdf.set_font("Helvetica", "I", 12)
            pdf.set_text_color(*cor_preto)
            pdf.cell(largura_util, 8, professor, ln=1, align="C")
        
        # Linha de assinatura e texto "Professor Responsável"
        pdf.ln(15)
        y_assinatura = pdf.get_y()
        
        largura_linha_assinatura = 80
        x_assinatura = centro_x - (largura_linha_assinatura / 2)
        pdf.set_draw_color(*cor_preto)
        pdf.set_line_width(0.3)
        pdf.line(x_assinatura, y_assinatura, x_assinatura + largura_linha_assinatura, y_assinatura)
        
        pdf.set_xy(x_assinatura, y_assinatura + 2)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*cor_cinza)
        pdf.cell(largura_linha_assinatura, 5, "Professor Responsável", align="C")

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
    professor_nome = st.text_input("Nome do Professor Responsável:", "Sensei Mestre Kawashima")
    
    st.subheader("Ajustes de Design e Coordenadas")
    
    # Color Picker
    cor_dourado_hex = st.color_picker("Cor de Destaque (Dourado):", "#B8860B")
    h = cor_dourado_hex.lstrip('#')
    cor_dourado_rgb_tuple = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    # Sliders de Coordenadas e Tamanho
    largura_barra_ajuste = st.slider("Largura da Barra Lateral (mm):", 5, 50, 25)
    
    # NOVO: Controle de Posição Y do Título
    posicao_y_titulo_ajuste = st.slider("Posição Y (Vertical) do Título:", 10, 80, 45, help="Controla o pdf.set_y(Y) antes do título principal.")
    
    tamanho_titulo_ajuste = st.slider("Tamanho da Fonte do Título:", 18, 40, 24)
    espacamento_ajuste = st.slider("Espaçamento Vertical (ln) após Título:", 10, 50, 20)
    
    # Checkbox
    incluir_logo_check = st.checkbox("Incluir Logo (Requer 'assets/logo.png')", value=False)
    
    st.subheader("Dados Não Visíveis (Fixo para o Streamlit)")
    st.text_input("Pontuação (Pontuacao)", 90, disabled=True)
    st.text_input("Total de Pontos (Total)", 100, disabled=True)
    st.text_input("Código de Validação (Codigo)", "XYZ123ABC", disabled=True)
    
# --- Geração e Visualização do PDF ---
pdf_bytes, nome_arquivo = gerar_pdf(
    nome_aluno, 
    faixa_alvo, 
    90, 
    100, 
    "XYZ123ABC", 
    professor=professor_nome,
    cor_dourado_rgb=cor_dourado_rgb_tuple,
    largura_barra=largura_barra_ajuste,
    tamanho_titulo=tamanho_titulo_ajuste,
    posicao_y_titulo=posicao_y_titulo_ajuste, # NOVO PARÂMETRO
    espacamento_titulo=espacamento_ajuste,
    incluir_logo=incluir_logo_check
)

with col_preview:
    st.header("✨ Pré-visualização")
    
    if pdf_bytes:
        # Usa base64 para embedar o PDF no Streamlit
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Botão de download
        st.download_button(
            label="Baixar PDF Gerado",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf"
        )
    else:
        st.warning("Não foi possível gerar o PDF. Verifique os logs de erro.")
