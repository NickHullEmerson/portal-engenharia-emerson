import streamlit as st
import base64
import urllib.parse
from datetime import datetime
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nick Hull Emerson Engineering | Portal", page_icon="🏗️", layout="centered")

# --- FUNÇÃO PARA CONEXÃO COM GOOGLE DRIVE ---
def upload_to_drive(protocolo, nome_cliente, arquivos_carregados):
    try:
        # Puxa as credenciais de forma segura dos Secrets do Streamlit
        creds_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(creds_info)
        service = build('drive', 'v3', credentials=creds)

        # ID da pasta "Mãe" que você criou no seu Drive
        # Exemplo: se a URL é drive.google.com/drive/folders/1XYZ..., o ID é 1XYZ...
        ID_PASTA_MAE = "COLE_AQUI_O_ID_DA_SUA_PASTA" 

        # 1. Cria a pasta do cliente dentro da pasta mãe
        file_metadata = {
            'name': f"{protocolo} - {nome_cliente}",
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [ID_PASTA_MAE]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')

        # 2. Faz o upload de cada arquivo selecionado
        for uploaded_file in arquivos_carregados:
            file_metadata = {'name': uploaded_file.name, 'parents': [folder_id]}
            media = MediaIoBaseUpload(io.BytesIO(uploaded_file.getvalue()), 
                                      mimetype=uploaded_file.type, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        return folder_id
    except Exception as e:
        st.error(f"Erro na integração com Google Drive: {e}")
        return None

# --- FUNÇÃO PARA TRATAMENTO DE IMAGEM ---
def get_base64_logo(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return None

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
    .protocol-box { background-color: #1c2e2e; padding: 15px; border: 1px solid #25D366; border-radius: 5px; margin-top: 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown('<div class="header-container">', unsafe_allow_html=True)
if bin_str:
    st.markdown(f'<img src="data:image/png;base64,{bin_str}" width="180" style="display: block; margin: 0 auto;">', unsafe_allow_html=True)
st.markdown('<p class="header-text">Portal de Diagnóstico Estratégico</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">Precisão e Estratégia | Nick Hull Emerson Engineering</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- BOAS-VINDAS ---
st.markdown('<div class="welcome-box"><b>Bem-vindo(a)!</b><br><br>Realizamos uma triagem técnica detalhada para garantir a segurança jurídica e estrutural do seu patrimônio de forma ágil e eficiente.<br><br><i>"A engenharia de excelência começa nos detalhes da informação."</i></div>', unsafe_allow_html=True)

# --- FORMULÁRIO ---
nome_resp = st.text_input("Nome Completo do Responsável *")
finalidade = st.selectbox("Finalidade do Trabalho *", [
    "Selecione uma opção...", "Usucapião (Documentação)", "Retificação de Área", "CND de Obra", 
    "Reforço Estrutural", "Contenção | Muro de Arrimo", "Projeto Estrutural", "Avaliação de Imóveis"
])

if finalidade != "Selecione uma opção...":
    st.write("### 📍 Localização e Triagem Fiscal")
    col1, col2 = st.columns([3, 1])
    ender = col1.text_input("Logradouro (Rua/Av) *")
    num = col2.text_input("Nº *")
    
    c1, c2, c3 = st.columns(3)
    cep = c1.text_input("CEP *")
    bairro = c2.text_input("Bairro *")
    cidade = c3.text_input("Cidade *")

    iptu = st.text_input("Número do IPTU (Contribuinte) *")
    area = st.number_input("Área Aproximada (m²) *", min_value=0.0)
    
    st.write("---")
    proprietario = st.text_input("Nome do Proprietário (conforme Matrícula/Contrato) *")
    
    st.write("### 📂 Documentação e Evidências")
    c_mat = st.checkbox("Possuo Matrícula")
    c_cont = st.checkbox("Possuo Contrato de Compra e Venda")

    files = st.file_uploader("Selecione as Fotos ou PDFs", accept_multiple_files=True, type=['pdf','png','jpg','jpeg'])
    lgpd_check = st.checkbox("Concordo com o tratamento dos meus dados (LGPD).")

    if st.button("GERAR PROTOCOLO E FINALIZAR"):
        # Validação via Dicionário (Inovação sugerida por você)
        campos_obrigatorios = {
            "Nome": nome_resp.strip(), "Rua": ender.strip(), "Bairro": bairro.strip(),
            "IPTU": iptu.strip(), "Área": area > 0, "Documento de Posse": (c_mat or c_cont), "LGPD": lgpd_check
        }
        
        erros = [f"O campo '{k}' é obrigatório." for k, v in campos_obrigatorios.items() if not v]

        if erros:
            for e in erros: st.error(e)
        else:
            protocolo_id = f"NH-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            # Executa o upload para o Drive
            with st.spinner('📦 Criando pasta e enviando arquivos para o Google Drive...'):
                drive_folder_id = upload_to_drive(protocolo_id, nome_resp, files)
            
            if drive_folder_id:
                link_drive = f"https://drive.google.com/drive/folders/{drive_folder_id}"
                
                st.markdown(f'<div class="protocol-box">✅ Protocolo: {protocolo_id}<br>Arquivos salvos com sucesso no Drive!</div>', unsafe_allow_html=True)

                msg_whatsapp = f"*NOVO DIAGNÓSTICO*\nID: {protocolo_id}\nCliente: {nome_resp}\nServiço: {finalidade}\nLocal: {bairro}\nDrive: {link_drive}"
                link_wa = f"https://wa.me/5511998511552?text={urllib.parse.quote(wa_msg)}"
                st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:5px; font-weight:bold; cursor:pointer;">📲 ABRIR WHATSAPP DO ENGENHEIRO</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Nick Hull Emerson Engineering | Low-Friction Systems")
