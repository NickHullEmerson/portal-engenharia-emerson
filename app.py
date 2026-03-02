import streamlit as st
import base64
import urllib.parse
from datetime import datetime
import random
import requests  # Para API de CEP e CNPJ
import re        # Para validação de CPF/CNPJ/IPTU

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nick Hull Emerson Engineering", page_icon="🏗️", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'logradouro' not in st.session_state: st.session_state.logradouro = ''
if 'bairro' not in st.session_state: st.session_state.bairro = ''
if 'cidade' not in st.session_state: st.session_state.cidade = ''
if 'razao_social' not in st.session_state: st.session_state.razao_social = ''

# --- FUNÇÃO DE BUSCA DE CEP (VIACEP) ---
def buscar_cep():
    if 'cep_input' in st.session_state:
        cep_digitado = st.session_state.cep_input.replace("-", "").replace(".", "").strip()
        if len(cep_digitado) == 8:
            try:
                response = requests.get(f"https://viacep.com.br/ws/{cep_digitado}/json/")
                dados = response.json()
                if "erro" not in dados:
                    st.session_state.logradouro = dados['logradouro']
                    st.session_state.bairro = dados['bairro']
                    st.session_state.cidade = dados['localidade']
                else:
                    st.toast("⚠️ CEP não encontrado.", icon="❌")
            except:
                pass

# --- FUNÇÃO DE BUSCA DE CNPJ (BRASILAPI) ---
def buscar_cnpj():
    if 'cnpj_input' in st.session_state:
        cnpj_digitado = st.session_state.cnpj_input.replace("-", "").replace(".", "").replace("/", "").strip()
        if len(cnpj_digitado) == 14:
            try:
                response = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_digitado}")
                if response.status_code == 200:
                    dados = response.json()
                    st.session_state.razao_social = dados['razao_social']
                    st.toast("✅ Empresa localizada!", icon="🏢")
                else:
                    st.toast("⚠️ CNPJ não encontrado.", icon="❌")
            except:
                pass

# --- VALIDAÇÕES DE FORMATO ---
def validar_cpf_formato(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    return len(cpf) == 11

def validar_iptu_formato(iptu_texto):
    if not iptu_texto: return False
    return bool(re.match(r'^[0-9.-]+$', iptu_texto))

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
    
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 1rem !important;
    }
    
    .header-container { 
        text-align: center; 
        padding-bottom: 15px;
        margin-bottom: 10px;
    }
    
    .header-text { 
        font-size: clamp(22px, 5vw, 32px) !important; 
        font-weight: 700; 
        color: #2e7bcf !important; 
        width: 100%; 
        display: block; 
        line-height: 1.1 !important; 
        margin-bottom: 5px !important; 
    }
    
    .subheader-text { 
        font-size: 14px !important; 
        color: #888888 !important; 
        margin-top: 0px !important; 
        font-weight: 500; 
        letter-spacing: 0.5px;
    }
    
    .welcome-box { 
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7bcf; 
        text-align: justify; 
        margin-bottom: 15px;
        font-size: 14px;
        color: #31333F !important; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .custom-info-box { background-color: #e1f5fe; color: #0277bd !important; padding: 15px; border-radius: 8px; border-left: 5px solid #0288d1; margin-bottom: 20px; font-size: 14px; line-height: 1.5; }
    .services-hint { background-color: #fff3cd; color: #856404 !important; padding: 12px; border-radius: 8px; border-left: 5px solid #ffc107; margin-bottom: 10px; font-size: 13px; font-weight: 600; }
    
    .scroll-hint { text-align: center; color: #2e7bcf; font-size: 12px; margin: 15px 0; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    
    .lgpd-box { background-color: #fff9e6; border: 2px solid #ff9800; padding: 15px; border-radius: 8px; margin: 15px 0; }
    .lgpd-box label { color: #e65100 !important; font-weight: 700 !important; font-size: 15px !important; }
    .lgpd-box input[type="checkbox"] { width: 24px !important; height: 24px !important; cursor: pointer !important; }
    
    .doc-list { font-size: 13px; color: #31333F; background: #ffffff; padding: 15px; border-radius: 5px; border: 1px dashed #2e7bcf; line-height: 1.5; }
    .protocol-box { background-color: #e8f5e9; color: #1b5e20; padding: 15px; border: 1px solid #25D366; border-radius: 5px; margin-top: 20px; margin-bottom: 20px; text-align: left; }
    
    .stButton>button { width: 100%; border-radius: 8px; background-color: #2e7bcf; color: white !important; font-weight: bold; height: 4em; border: none; }
    .stButton>button:hover { background-color: #3b8ee0; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO COMPACTO ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if bin_str:
    st.markdown(f'<img src="data:image/png;base64,{bin_str}" style="max-width: 140px; height: auto; display: block; margin: 0 auto 5px auto;">', unsafe_allow_html=True)
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
    segurança jurídica e estrutural do seu patrimônio.
</div>
""", unsafe_allow_html=True)

# --- IDENTIFICAÇÃO (OBRIGATÓRIA) ---
st.write("### 👤 Identificação do Responsável")

tipo_pessoa = st.radio("Tipo de Pessoa:", ["Pessoa Física (CPF)", "Pessoa Jurídica (CNPJ)"], horizontal=True)

nome_resp = ""
doc_resp = ""

if tipo_pessoa == "Pessoa Física (CPF)":
    doc_resp = st.text_input("CPF * (Obrigatório)", placeholder="000.000.000-00")
    if doc_resp and not validar_cpf_formato(doc_resp):
        st.caption("⚠️ O formato do CPF parece incompleto.")
    nome_resp = st.text_input("Nome Completo * (Obrigatório)", placeholder="Ex: João Silva Santos")

else:
    st.info("💡 Digite o CNPJ e aperte Enter para buscar o nome da empresa.")
    doc_resp = st.text_input("CNPJ * (Obrigatório)", key="cnpj_input", on_change=buscar_cnpj, placeholder="00.000.000/0000-00")
    nome_resp = st.text_input("Razão Social * (Obrigatório)", value=st.session_state.razao_social, placeholder="Nome da Empresa Ltda")

# --- DESTAQUE DOS SERVIÇOS ---
st.markdown("""
<div class="services-hint">
    🔍 <b>ATENÇÃO:</b> Selecione abaixo o serviço desejado (Temos 12 opções):
    <br>Usucapião, Perícias, AVCB, Projetos, CND, Avaliações, Reforços e mais.
</div>
""", unsafe_allow_html=True)

# --- INCLUSÃO DO NOVO SERVIÇO ---
finalidade = st.selectbox("Finalidade do Trabalho *", [
    "Selecione uma opção...", 
    "Perícias Técnicas de Engenharia", # NOVO
    "Usucapião (Documentação)", 
    "AVCB/CLCB Bombeiro", 
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
    st.markdown('<div class="scroll-hint">⬇️ Role para baixo para preencher os dados ⬇️</div>', unsafe_allow_html=True)

if finalidade != "Selecione uma opção...":
    # Mensagens de Importância (ATUALIZADO COM PERÍCIAS)
    mensagens = {
        "Perícias": "Produção de prova técnica fundamentada para resolução de conflitos judiciais ou extrajudiciais.",
        "Usucapião": "Valoriza o imóvel em até 40% e garante a propriedade real.",
        "AVCB": "Licença essencial para funcionamento comercial e segurança contra incêndios.",
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
            st.markdown(f"""
            <div class="custom-info-box">
                <b>ℹ️ Importância Estratégica:</b><br>{v}
            </div>
            """, unsafe_allow_html=True)

    if "Usucapião" in finalidade:
        anos = st.number_input("Há quantos anos você possui a posse do imóvel? *", min_value=0, step=1)

    st.write("### 📍 Localização e Triagem Fiscal")
    st.info("💡 Digite o CEP e aperte Enter para preencher o endereço automaticamente.")
    
    col_cep, col_num = st.columns([2, 1])
    with col_cep:
        cep_input = st.text_input("CEP * (Obrigatório)", key="cep_input", on_change=buscar_cep, placeholder="00000000")
    with col_num: 
        num = st.text_input("Nº *", placeholder="123")

    ender = st.text_input("Logradouro", value=st.session_state.logradouro, placeholder="Rua...")
    
    c1, c2 = st.columns(2)
    with c1: bairro = st.text_input("Bairro", value=st.session_state.bairro, placeholder="Bairro...")
    with c2: cidade = st.text_input("Cidade", value=st.session_state.cidade, placeholder="Cidade...")

    # IPTU OBRIGATÓRIO E FILTRADO
    iptu = st.text_input("Número do IPTU * (Obrigatório - Somente nº, ponto ou traço)", placeholder="000.000.000-0")
    
    # ÁREA OBRIGATÓRIA
    area = st.number_input("Área Aproximada (m²) * (Obrigatório)", min_value=0.0, step=10.0)
    
    st.write("Tipo de documentação de posse disponível:")
    c_mat = st.checkbox("Possuo Matrícula")
    c_cont = st.checkbox("Possuo Contrato de Compra e Venda")

    st.write("---")
    proprietario = st.text_input("Nome do Proprietário (conforme Matrícula/Contrato) *", placeholder="Ex: Maria da Silva")
    
    st.write("### 📂 Documentação e Evidências")
    
    # ATUALIZADO COM PERÍCIAS NA LISTA DOCUMENTAL
    servicos_documentais = ["Usucapião", "Retificação", "CND", "Avaliação", "AVCB", "Perícias"]
    
    if any(s in finalidade for s in servicos_documentais):
        req_text = ""
        if "Perícias" in finalidade:
            req_text = "• Número do Processo (se houver)<br>• Projetos da edificação<br>• Relatórios de manutenção<br>• Quesitos (se houver)"
        elif "Usucapião" in finalidade:
            req_text = "• Matrícula ou Contrato<br>• Documento de Identidade<br>• Capa do IPTU<br>• Projeto existente (se houver)"
        elif "Retificação" in finalidade:
            req_text = "• Matrícula ou Transcrição<br>• Documento de Identidade<br>• Capa do IPTU<br>• Levantamento anterior"
        elif "CND" in finalidade:
            req_text = "• Alvará/Projeto Aprovado<br>• Documento de Identidade<br>• Capa do IPTU<br>• Notas Fiscais"
        elif "Avaliação" in finalidade:
            req_text = "• Matrícula atualizada<br>• Capa do IPTU<br>• Documento de Identidade<br>• Projeto arquitetônico"
        elif "AVCB" in finalidade:
            req_text = "• Projeto de Incêndio (se houver)<br>• Notas Fiscais de equipamentos<br>• Área construída exata<br>• CNPJ (se houver)"
        
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

    st.info("ℹ️ Selecione os arquivos abaixo para registro no protocolo. O envio real ocorrerá no WhatsApp.")
    files = st.file_uploader("Pré-Seleção de Arquivos (Inventário)", accept_multiple_files=True, type=['pdf','png','jpg','jpeg'])

    st.write("---")
    
    st.markdown('<div class="lgpd-box">', unsafe_allow_html=True)
    st.write("### 🔒 PASSO OBRIGATÓRIO: Autorização de Dados")
    st.warning("⚠️ Marque a caixa abaixo para prosseguir:")
    lgpd_check = st.checkbox("✅ Concordo com o tratamento dos meus dados pessoais (LGPD) conforme Lei nº 13.709/2018.", key="lgpd_aceite")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("GERAR PROTOCOLO E FINALIZAR"):
        
        erros_criticos = []
        
        # 1. LGPD
        if not lgpd_check:
            erros_criticos.append("⚠️ O aceite da LGPD é obrigatório.")
            
        # 2. Finalidade
        if finalidade == "Selecione uma opção...":
            erros_criticos.append("⚠️ Selecione a finalidade do trabalho.")

        # 3. Nome/Razão Social
        if not nome_resp or len(nome_resp.strip()) < 3:
            erros_criticos.append("⚠️ O Nome/Razão Social é obrigatório.")

        # 4. Documento
        if not doc_resp or len(doc_resp.strip()) < 5:
            erros_criticos.append("⚠️ O CPF ou CNPJ é obrigatório.")

        # 5. CEP
        if not cep_input or len(cep_input.strip()) < 8:
             erros_criticos.append("⚠️ O CEP é obrigatório.")

        # 6. IPTU
        if not iptu:
            erros_criticos.append("⚠️ O Número do IPTU é obrigatório.")
        elif not validar_iptu_formato(iptu):
            erros_criticos.append("⚠️ O IPTU contém caracteres inválidos. Use apenas números, pontos e traços.")

        # 7. Área
        if area <= 0:
            erros_criticos.append("⚠️ A Área aproximada deve ser maior que zero.")
            
        # 8. Usucapião Específico
        if "Usucapião" in finalidade and anos == 0:
            erros_criticos.append("⚠️ Informe o tempo de posse (anos).")

        if erros_criticos:
            for e in erros_criticos: st.error(e)
        else:
            protocolo_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            qtd_arquivos = len(files) if files else 0
            if qtd_arquivos > 0:
                lista_arquivos = [f.name for f in files]
                texto_arquivos = "\n".join([f"- {nome}" for nome in lista_arquivos])
                msg_arquivos = f"{qtd_arquivos} arquivos pré-listados:\n{texto_arquivos}"
            else:
                msg_arquivos = "Nenhum arquivo listado na pré-conferência."

            st.markdown(f"""
            <div class="protocol-box">
                <h3 style="color:#1b5e20; margin:0;">✅ Diagnóstico Iniciado: {protocolo_id}</h3><br>
                <b>Inventário:</b> {qtd_arquivos} arquivos registrados.<br><br>
                <b>PASSO FINAL:</b> Clique abaixo e anexe as mídias no WhatsApp.<br>
                🕒 <b>Prazo:</b> 24h a 48h úteis.
            </div>
            """, unsafe_allow_html=True)
            
            safe_ender = ender if ender else st.session_state.logradouro
            safe_bairro = bairro if bairro else st.session_state.bairro
            safe_cidade = cidade if cidade else st.session_state.cidade
            
            msg_whatsapp = f"""*NOVO DIAGNÓSTICO - NICK HULL EMERSON*
---------------------------------------
🆔 *Protocolo:* {protocolo_id}
👤 *Cliente:* {nome_resp}
📄 *Documento:* {doc_resp}
🏗️ *Serviço:* {finalidade}
⏳ *Anos (Se Usucapião):* {anos if 'Usucapião' in finalidade else 'N/A'}

📍 *Localização:*
{safe_ender}, {num} - {safe_bairro}, {safe_cidade}
CEP: {cep_input}

📐 *Dados Técnicos:*
IPTU: {iptu}
Área: {area} m²
Proprietário: {proprietario}

📂 *INVENTÁRIO:*
{msg_arquivos}

🔐 *LGPD:* Aceite confirmado em {datetime.now().strftime('%d/%m/%Y')}

⚠️ *AÇÃO:* Estou enviando os arquivos listados acima agora:
"""
            msg_encoded = urllib.parse.quote(msg_whatsapp)
            link_wa = f"https://wa.me/5511998511552?text={msg_encoded}"
            
            st.markdown(f'''
                <a href="{link_wa}" target="_blank" style="text-decoration:none;">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:18px;">
                        📲 CONFIRMAR NO WHATSAPP
                    </button>
                </a>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'<div style="text-align:center; font-size:12px; color:#888; margin-top:10px;">Toque para abrir o WhatsApp</div>', unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("---")
st.write("### 💬 Precisa de Ajuda?")
link_sup = "https://wa.me/5511998511552?text=Olá Emerson, preciso de ajuda no Portal."
st.markdown(f'<a href="{link_sup}" target="_blank" style="text-decoration:none;"><div style="padding:15px; border:1px solid #2e7bcf; color:#2e7bcf; border-radius:8px; text-align:center; font-weight:bold;">Falar com o Engenheiro</div></a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 Nick Hull Emerson Engineering | Low-Friction Systems")
