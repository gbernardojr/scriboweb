import streamlit as st
from pathlib import Path
from control import controllerScribo

# Instância do controlador
Control = controllerScribo()

def formatar_data(data):
    """Formata data para o formato DD/MM/AAAA."""
    texto = data.replace("/", "")
    if len(texto) > 2:
        texto = texto[:2] + '/' + texto[2:]
    if len(texto) > 5:
        texto = texto[:5] + '/' + texto[5:]
    return texto[:10]

def formatar_cpf(cpf):
    """Formata CPF para o formato XXX.XXX.XXX-XX."""
    texto = cpf.replace(".", "").replace("-", "")
    if len(texto) > 3:
        texto = texto[:3] + '.' + texto[3:]
    if len(texto) > 7:
        texto = texto[:7] + '.' + texto[7:]
    if len(texto) > 11:
        texto = texto[:11] + '-' + texto[11:]
    return texto[:14]

# Interface do Streamlit
st.title("Scribo - Sistema Médico")

# Formulário para dados do paciente
st.header("Dados do Paciente")
nome = st.text_input("Nome do Paciente")
nascimento = st.text_input("Data de Nascimento", on_change=lambda: formatar_data(nascimento))
cpf = st.text_input("CPF", on_change=lambda: formatar_cpf(cpf))
endereco = st.text_input("Endereço")
cidade = st.text_input("Cidade")
prescricao = st.text_area("Prescrição Médica")

# Botão para gerar PDF
if st.button("Gerar PDF"):
    paciente = {
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "cidade": cidade,
        "prescricao": prescricao,
    }
    file_path = Control.gerar_nome_pdf(paciente)
    senha_leitura = Control.gerar_senha(paciente["cpf"])
    Control.gerar_pdf(paciente=paciente, tipo="prescrição", file_path=file_path, senha_leitura=senha_leitura)
    st.success("PDF gerado com sucesso!")

# Botão para imprimir
if st.button("Imprimir PDF"):
    paciente = {
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "cidade": cidade,
        "prescricao": prescricao,
    }
    file_path = Control.gerar_nome_pdf(paciente)
    senha_leitura = Control.gerar_senha(paciente["cpf"])
    Control.imprimir_pdf(paciente=paciente, tipo="prescrição", file_path=file_path, senha_leitura=senha_leitura)
    st.success("Documento enviado para impressão!")

# Função para envio de e-mail
if st.button("Enviar por E-mail"):
    st.info("Esta funcionalidade ainda precisa ser implementada.")

# Função para envio pelo WhatsApp
if st.button("Enviar por WhatsApp"):
    st.info("Esta funcionalidade ainda precisa ser implementada.")
