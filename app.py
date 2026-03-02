import streamlit as st
import base64
import urllib.parse
from datetime import datetime
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nick Hull Emerson Engineering | Portal", page_icon="🏗️", layout="centered")

# --- FUNÇÃO PARA TRATAMENTO DE IMAGEM ---
def get_base64_logo(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

bin_str = get_base64_logo("logo.png")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .header-container { text-align: center; padding: 10px 0px; }
    .header-text { font-size: clamp(30px, 5vw, 38px) !important; font-weight: 600; color: #ffffff; width: 100%; display: block; }
    .subheader-text { font-size: 18px !important; color: #2e7bcf; margin-top:-5px; font-weight: 500; }
    .welcome-box { background-color: #1a1c24; padding: 25px; border-radius: 10px; border: 1px solid #2e7bcf; text-align: justify; margin-bottom: 25px;}
    .doc-list { font-size: 14px; color: #aeb9cc; background: #161b22; padding: 15px; border-radius: 5px; border: 1px dashed #2e7bcf; line-height: 1.6; }
    .protocol-box { background-color: #1c2e2e; padding: 15px; border: 1px solid #25D366; border-radius: 5px; margin-top: 20px; margin-bottom: 20px; text-align: left; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #2e7bcf; color: white; font-weight: bold; height: 3.5em; border: none; }
    .stButton>button:hover { background-color: #3b8ee0; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    if bin_str:
        st.markdown(f'<img src="data:image/png;base64,{bin_str}" width="100%">', unsafe_allow_html=True)
    st.markdown("### 💬 Suporte Direto")
    st.write("Dúvidas sobre os dados ou documentos?")
    link_sup = "https://wa.me/5511998511552?text=Olá Emerson, preciso de ajuda no Portal."
    st.markdown(f'<a href="{link_sup}" target="_blank" style="text-decoration:none;"><div style="padding:10px; border:1px solid #25D366; color:#25D366; border-radius:5px; text-align:center; font-weight:bold;">Falar com o Engenheiro</div></a>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Nick Hull Emerson Engineering | Low-Friction Systems")

# --- CABEÇALHO ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if bin_str:
    st.markdown(f'<img src="data:image/png;base64,{bin_str}" width="180" style="display: block; margin: 0 auto;">', unsafe_allow_html=True)
else:
    st.markdown('<p class="header-text">🏗️ Nick Hull Emerson Engineering</p>', unsafe_allow_html=True)

st.markdown('<p class="header-text">Portal de Diagnóstico Estratégico</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">Precisão e Estratégia | Low-Friction Systems</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOAS-VINDAS ---
st.markdown(f"""
<div class="welcome-box">
    <b>Bem-vindo(a)!</b><br><br>
    Agradecemos a confiança na <b>Nick Hull Emerson Engineering</b>. Realizamos uma triagem técnica detalhada para garantir a 
    segurança jurídica e estrutural do seu patrimônio de forma ágil e eficiente.<br><br>
    <i>"A engenharia de excelência começa nos detalhes da informação."</i>
</div>
""", unsafe_allow_html=True)

# --- FORMULÁRIO ---
nome_resp = st.text_input("Nome Completo do Responsável *", key="n_resp")
finalidade = st.selectbox("Finalidade do Trabalho *", [
    "Selecione uma opção...", 
    "Usucapião (Documentação)", 
    "Retificação de Área", 
    "CND de Obra", 
    "Reforço Estrutural", 
    "Contenção | Muro de Arrimo", 
    "Projeto Estrutural", 
    "Avaliação de Imóveis",
    "Projeto de Fundação",
    "Projetos de Instalações",
    "Projeto Arquitetônico"
])

if finalidade != "Selecione uma opção...":
    # Mensagens de Importância
    mensagens = {
        "Usucapião": "Valoriza o imóvel em até 40% e garante a propriedade real.",
        "Retificação": "Ajuste físico-jurídico essencial para vendas e financiamentos.",
        "CND": "Regularidade fiscal perante a Receita Federal e averbação da obra.",
        "Reforço": "Intervenção para sanar patologias e riscos de desmoronamento.",
        "Contenção": "Estabilidade máxima para terrenos com desnível.",
        "Projeto Estrutural": "Otimização de custos e segurança máxima para sua estrutura.",
        "Avaliação": "Determinação técnica do valor real de mercado para transações seguras.",
        "Projeto de Fundação": "Garantia de estabilidade desde a base, evitando recalques futuros.",
        "Projetos de Instalações": "Eficiência e conformidade técnica para sistemas elétricos e hidráulicos.",
        "Projeto Arquitetônico": "Harmonia entre estética, funcionalidade e aproveitamento de espaço."
    }
    
    for k, v in mensagens.items():
        if k in finalidade: 
            st.info(f"**Importância:** {v}")

    if "Usucapião" in finalidade:
        anos = st.number_input("Há quantos anos você possui a posse do imóvel? *", min_value=0, step=1)

    st.write("### 📍 Localização e Triagem Fiscal")
    col1, col2 = st.columns([3, 1])
    with col1: ender = st.text_input("Logradouro (Rua/Av) *")
    with col2: num = st.text_input("Nº *")
    
    c1, c2, c3 = st.columns(3)
    with c1: cep = st.text_input("CEP *")
    with c2: bairro = st.text_input("Bairro *")
    with c3: cidade = st.text_input("Cidade *")

    iptu = st.text_input("Número do IPTU (Contribuinte) *")
    area = st.number_input("Área Aproximada (m²) *", min_value=0.0)
    
    st.write("Tipo de documentação de posse disponível:")
    col_doc1, col_doc2 = st.columns(2)
    with col_doc1: c_mat = st.checkbox("Possuo Matrícula")
    with col_doc2: c_cont = st.checkbox("Possuo Contrato de Compra e Venda")

    st.write("---")
    proprietario = st.text_input("Nome do Proprietário (conforme Matrícula/Contrato) *")
    
    if nome_resp and proprietario and nome_resp.strip().lower() != proprietario.strip().lower():
        st.error("⚠️ Divergência: O nome do responsável difere do proprietário registrado.")

    st.write("### 📂 Documentação e Evidências")
    
    # Lógica de Exibição SSD
    servicos_documentais = ["Usucapião", "Retificação", "CND", "Avaliação"]
    
    if any(s in finalidade for s in servicos_documentais):
        req_text = ""
        if "Usucapião" in finalidade:
            req_text = "• Matrícula ou Contrato<br>• Documento de Identidade<br>• Carnê IPTU<br>• Projeto existente (se houver)"
        elif "Retificação" in finalidade:
            req_text = "• Matrícula ou Transcrição<br>• Documento de Identidade<br>• Carnê IPTU<br>• Levantamento anterior"
        elif "CND" in finalidade:
            req_text = "• Alvará/Projeto Aprovado<br>• Documento de Identidade<br>• Capa do IPTU<br>• Notas Fiscais"
        elif "Avaliação" in finalidade:
            req_text = "• Matrícula atualizada<br>• Capa do IPTU<br>• Documento de Identidade<br>• Projeto arquitetônico"
        
        st.markdown(f'<div class="doc-list"><b>📄 Separe para enviar no WhatsApp:</b><br>{req_text}</div><br>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="doc-list">
            <b>📸 Guia de Fotos (Para enviar no WhatsApp):</b><br>
            • <b>IPTU:</b> Foto legível da capa.<br>
            • <b>Patologias/Reforço:</b> Fotos de longe (contexto) e de perto (detalhe).<br>
            • <b>Terrenos:</b> Fotos dos 4 cantos e desnível.<br>
            • <b>Reformas:</b> Fotos panorâmicas dos ambientes.
        </div><br>
        """, unsafe_allow_html=True)

    # --- INVENTÁRIO DE ARQUIVOS ---
    st.info("ℹ️ Selecione os arquivos abaixo para registro no protocolo. O envio real ocorrerá no WhatsApp.")
    files = st.file_uploader("Pré-Seleção de Arquivos (Inventário)", accept_multiple_files=True, type=['pdf','png','jpg','jpeg'])

    # --- LGPD E TERMOS ---
    st.write("---")
    st.write("### 🔒 Privacidade e Protocolo")
    lgpd_check = st.checkbox("Concordo com o tratamento dos meus dados pessoais para fins de orçamento e análise técnica de engenharia, em conformidade com a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).")

    if st.button("GERAR PROTOCOLO E FINALIZAR"):
        # Validação Rígida
        campos_obrigatorios = {
            "Nome do Responsável": nome_resp.strip(),
            "Logradouro": ender.strip(),
            "Bairro": bairro.strip(),
            "Cidade": cidade.strip(),
            "IPTU": iptu.strip(),
            "Área": area > 0,
            "Documento de Posse": (c_mat or c_cont),
            "Aceite LGPD": lgpd_check
        }
        
        erros = []
        for campo, preenchido in campos_obrigatorios.items():
            if not preenchido:
                erros.append(f"O campo '{campo}' é obrigatório.")

        if len(nome_resp.strip()) < 10:
            erros.append("O nome deve ser completo para identificação.")
        
        if erros:
            for e in erros: st.error(e)
        else:
            # Geração de ID Único
            protocolo_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            # --- PROCESSAMENTO DO INVENTÁRIO DE ARQUIVOS (FORENSE) ---
            qtd_arquivos = len(files) if files else 0
            if qtd_arquivos > 0:
                lista_arquivos = [f.name for f in files]
                texto_arquivos = "\n".join([f"- {nome}" for nome in lista_arquivos])
                msg_arquivos = f"{qtd_arquivos} arquivos pré-listados:\n{texto_arquivos}"
            else:
                msg_arquivos = "Nenhum arquivo listado na pré-conferência."

            # --- ÁREA DE SUCESSO E INSTRUÇÕES ---
            st.markdown(f"""
            <div class="protocol-box">
                <h3 style="color:#25D366; margin:0;">✅ Diagnóstico Iniciado: {protocolo_id}</h3><br>
                <b>Inventário de Entrega:</b><br>
                Foram registrados {qtd_arquivos} documentos/fotos neste protocolo. <br>
                <i>Certifique-se de anexá-los na conversa do WhatsApp.</i><br><br>
                <b>Próximos Passos Obrigatórios:</b><br>
                1. Clique no botão verde abaixo para abrir o WhatsApp.<br>
                2. <b>ANEXE AS FOTOS E DOCUMENTOS</b> listados.<br>
                3. Nossa engenharia fará a triagem técnica.<br><br>
                🕒 <b>SLA (Prazo de Resposta):</b> Orçamento/Parecer preliminar em 24h a 48h úteis após o recebimento das imagens.
            </div>
            """, unsafe_allow_html=True)
            
            # --- CONSTRUÇÃO DO LINK WHATSAPP COM INVENTÁRIO ---
            msg_whatsapp = f"""*NOVO DIAGNÓSTICO - NICK HULL EMERSON*
---------------------------------------
🆔 *Protocolo:* {protocolo_id}
👤 *Cliente:* {nome_resp}
🏗️ *Serviço:* {finalidade}

📍 *Localização:*
{ender}, {num} - {bairro}, {cidade}
CEP: {cep}

📐 *Dados Técnicos:*
IPTU: {iptu}
Área: {area} m²
Proprietário: {proprietario}

📂 *INVENTÁRIO DE DOCUMENTOS:*
{msg_arquivos}

🔐 *LGPD:* Aceite confirmado em {datetime.now().strftime('%d/%m/%Y')}

⚠️ *AÇÃO:* Estou enviando os arquivos listados acima agora:
"""
            msg_encoded = urllib.parse.quote(msg_whatsapp)
            link_wa = f"https://wa.me/5511998511552?text={msg_encoded}"
            
            st.markdown(f'''
                <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:5px; cursor:pointer; font-weight:bold; font-size:18px;">
                        📲 CONFIRMAR ENVIO NO WHATSAPP
                    </button>
                </a>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'<div style="text-align:center; font-size:12px; color:#888; margin-top:10px;">ℹ️ Ao clicar, os dados serão transferidos. Anexe as mídias para validar o protocolo.</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Nick Hull Emerson Engineering | Low-Friction Systems")
