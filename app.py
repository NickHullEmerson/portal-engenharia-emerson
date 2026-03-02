import streamlit as st
import base64
import urllib.parse
from datetime import datetime
import random

# --- CONFIGURAÇÃO DA PÁGINA (Layout Mobile-Friendly) ---
st.set_page_config(page_title="Nick Hull Emerson Engineering", page_icon="🏗️", layout="centered")

# --- FUNÇÃO PARA TRATAMENTO DE IMAGEM ---
def get_base64_logo(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

bin_str = get_base64_logo("logo.png")

# --- ESTILO CSS (CORRIGIDO PARA LEITURA E MOBILE) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Cabeçalho Ajustado */
    .header-container { 
        text-align: center; 
        padding-top: 10px; 
        padding-bottom: 20px; 
    }
    
    .header-text { 
        font-size: 26px !important; 
        font-weight: 700; 
        color: #ffffff !important; 
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    .subheader-text { 
        font-size: 16px !important; 
        color: #2e7bcf !important; 
        font-weight: 500; 
    }
    
    /* Novo Design da Caixa de Boas-Vindas (Legível) */
    .welcome-box { 
        background-color: #262730; /* Cinza mais claro que o fundo */
        color: #ffffff !important; /* Texto branco forçado */
        padding: 20px; 
        border-radius: 8px; 
        border-left: 5px solid #2e7bcf; /* Detalhe azul lateral */
        margin-bottom: 25px;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Protocolo */
    .protocol-box { 
        background-color: #1c2e2e; 
        padding: 15px; 
        border: 1px solid #25D366; 
        border-radius: 5px; 
        margin-top: 20px; 
        margin-bottom: 20px; 
        text-align: left; 
    }
    
    /* Botões Otimizados para Toque */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #2e7bcf; 
        color: white; 
        font-weight: bold; 
        height: 3.8em; 
        border: none; 
        font-size: 16px;
    }
    .stButton>button:hover { background-color: #3b8ee0; border: none; }
    
    .doc-list { 
        font-size: 14px; 
        color: #e0e0e0; 
        background: #1e1e1e; 
        padding: 15px; 
        border-radius: 5px; 
        border: 1px dashed #2e7bcf; 
        line-height: 1.5; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO (CORRIGIDO: LOGO + TEXTO SEMPRE VISÍVEIS) ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# 1. Logo (Se existir)
if bin_str:
    st.markdown(f'<img src="data:image/png;base64,{bin_str}" style="max-width: 140px; height: auto; display: block; margin: 0 auto 15px auto;">', unsafe_allow_html=True)

# 2. Título (Sempre visível agora)
st.markdown('<div class="header-text">🏗️ Nick Hull Emerson Engineering</div>', unsafe_allow_html=True)
st.markdown('<div class="header-text" style="font-size: 20px !important;">Portal de Diagnóstico Estratégico</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-text">Precisão e Estratégia | Low-Friction Systems</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOAS-VINDAS (NOVO DESIGN) ---
st.markdown(f"""
<div class="welcome-box">
    <b>Bem-vindo(a)!</b><br><br>
    Agradecemos a confiança na <b>Nick Hull Emerson Engineering</b>. Realizamos uma triagem técnica detalhada para garantir a 
    segurança jurídica e estrutural do seu patrimônio.<br><br>
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
    
    # Inputs sequenciais para mobile (evita colunas espremidas)
    ender = st.text_input("Logradouro (Rua/Av) *")
    num = st.text_input("Nº *")
    
    col_cep, col_bairro = st.columns(2)
    with col_cep: cep = st.text_input("CEP *")
    with col_bairro: bairro = st.text_input("Bairro *")
    
    cidade = st.text_input("Cidade *")
    iptu = st.text_input("Número do IPTU (Contribuinte) *")
    area = st.number_input("Área Aproximada (m²) *", min_value=0.0)
    
    st.write("Tipo de documentação de posse disponível:")
    c_mat = st.checkbox("Possuo Matrícula")
    c_cont = st.checkbox("Possuo Contrato de Compra e Venda")

    st.write("---")
    proprietario = st.text_input("Nome do Proprietário (conforme Matrícula/Contrato) *")
    
    if nome_resp and proprietario and nome_resp.strip().lower() != proprietario.strip().lower():
        st.error("⚠️ Divergência: O nome do responsável difere do proprietário registrado.")

    st.write("### 📂 Documentação e Evidências")
    
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

    st.info("ℹ️ Selecione os arquivos abaixo para registro no protocolo. O envio real ocorrerá no WhatsApp.")
    files = st.file_uploader("Pré-Seleção de Arquivos (Inventário)", accept_multiple_files=True, type=['pdf','png','jpg','jpeg'])

    st.write("---")
    st.write("### 🔒 Privacidade e Protocolo")
    lgpd_check = st.checkbox("Concordo com o tratamento dos meus dados pessoais (LGPD).")

    if st.button("GERAR PROTOCOLO E FINALIZAR"):
        # Validação Rígida
        campos_obrigatorios = {
            "Nome do Responsável": nome_resp.strip(),
            "Logradouro": ender.strip(),
            "Bairro": bairro.strip(),
            "Cidade": cidade.strip(),
            "CEP": cep.strip(),
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
            protocolo_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            # --- PROCESSAMENTO DO INVENTÁRIO ---
            qtd_arquivos = len(files) if files else 0
            if qtd_arquivos > 0:
                lista_arquivos = [f.name for f in files]
                texto_arquivos = "\n".join([f"- {nome}" for nome in lista_arquivos])
                msg_arquivos = f"{qtd_arquivos} arquivos pré-listados:\n{texto_arquivos}"
            else:
                msg_arquivos = "Nenhum arquivo listado na pré-conferência."

            # --- ÁREA DE SUCESSO ---
            st.markdown(f"""
            <div class="protocol-box">
                <h3 style="color:#25D366; margin:0;">✅ Diagnóstico Iniciado: {protocolo_id}</h3><br>
                <b>Inventário:</b> {qtd_arquivos} arquivos registrados.<br><br>
                <b>PASSO FINAL:</b> Clique abaixo e anexe as mídias no WhatsApp.<br>
                🕒 <b>Prazo:</b> 24h a 48h úteis.
            </div>
            """, unsafe_allow_html=True)
            
            # --- LINK WHATSAPP ---
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

# --- RODAPÉ MOBILE (SUPORTE) ---
st.markdown("---")
st.write("### 💬 Precisa de Ajuda?")
link_sup = "https://wa.me/5511998511552?text=Olá Emerson, preciso de ajuda no Portal."
st.markdown(f'<a href="{link_sup}" target="_blank" style="text-decoration:none;"><div style="padding:15px; border:1px solid #2e7bcf; color:#2e7bcf; border-radius:8px; text-align:center; font-weight:bold;">Falar com o Engenheiro</div></a>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 Nick Hull Emerson Engineering | Low-Friction Systems")
