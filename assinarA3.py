import subprocess
import PyKCS11
import PyPDF2
import tempfile
import os
from tkinter import simpledialog, Tk

# Função para acessar o certificado digital A3 no repositório do Windows
def get_certificate_from_token():
    #lib = 'C:\\Windows\\System32\\IDPrimePKCS11.dll'
    lib = 'C:\\Program Files (x86)\\Gemalto\\IDGo 800 PKCS#11\\IDPrimePKCS11.dll'  # Caminho correto do driver
    
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(lib)

    slots = pkcs11.getSlotList()
    if not slots:
        raise Exception("Nenhum leitor conectado")

    session = pkcs11.openSession(slots[0])
    
    # Janela para solicitar senha de forma segura
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    password = simpledialog.askstring("Senha", "Digite a senha do certificado:", show="*")
    session.login(password)  # Login com senha do usuário

    # Localiza o certificado no token
    certs = session.findObjects([(PyKCS11.CKA_CLASS, PyKCS11.CKO_CERTIFICATE)])
    if not certs:
        raise Exception("Certificado não encontrado")
    
    certificate = certs[0]  # Retorna o primeiro certificado encontrado
    session.logout()
    return certificate

# Função para desbloquear PDF protegido por senha
def unlock_pdf(input_pdf, output_pdf, password):
    with open(input_pdf, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        if reader.is_encrypted:
            reader.decrypt(password)
        writer = PyPDF2.PdfWriter()
        for page in range(len(reader.pages)):
            writer.add_page(reader.pages[page])
        
        with open(output_pdf, "wb") as out_f:
            writer.write(out_f)

# Função para assinar um PDF usando o certificado do token (PKCS#11)
def sign_pdf_with_token(input_pdf, output_pdf):
    # Comando para assinatura via OpenSSL com PKCS#11
    command = [
        'openssl', 'smime', '-sign', 
        '-in', input_pdf, 
        '-signer', 'NONE',  # Define o certificado pelo token
        '-inkey', 'NONE',  # A chave será fornecida pelo token
        '-engine', 'pkcs11',  # Define o uso do engine PKCS#11
        '-outform', 'DER', 
        '-out', output_pdf
    ]
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"PDF assinado com sucesso: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao assinar PDF: {e.stderr.decode()}")

# Função principal para assinar PDF protegido
def sign_protected_pdf(input_pdf, password, signed_pdf):
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        # Desbloqueia o PDF e salva em um arquivo temporário
        unlock_pdf(input_pdf, temp_pdf.name, password)
        
        # Assina o PDF desbloqueado
        sign_pdf_with_token(temp_pdf.name, signed_pdf)
    
    # Limpeza do arquivo temporário
    os.remove(temp_pdf.name)

# Exemplo de uso
# input_pdf = "protegido.pdf"
# password = "senha_do_pdf"
# signed_pdf = "assinado.pdf"
# sign_protected_pdf(input_pdf, password, signed_pdf)
