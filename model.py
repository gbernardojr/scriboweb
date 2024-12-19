import pyodbc
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode
import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
from pyhanko.sign import signers
from fpdf import FPDF
from datetime import datetime


tamLabel = 15
tamEntry = 70
tamButton = 15

class dbScribo:

    # Conectar ao banco de dados Paradox (exemplo básico de conexão com Paradox via ODBC)
    def conectar_banco_dados(self):
        conn_str = (
            r'DRIVER={Paradox Driver (*.db)};'
            r'DBQ=C:\Dados Gilberto\WinCli\;'
        )
        conn = pyodbc.connect(conn_str)
        return conn

    # Função para buscar dados do paciente
    def buscar_dados_paciente(self,pacienteID):
        conn = self.conectar_banco_dados()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Med000 WHERE ID=?", pacienteID)
        row = cursor.fetchone()
        if row:
            return row
        conn.close()

    # Função para buscar prescrição do banco
    def buscar_prescricao(self,prescricaoID):
        conn = self.conectar_banco_dados()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Prescricoes WHERE ID=?", prescricaoID)
        row = cursor.fetchone()
        if row:
            return row
        conn.close()

    # Função para buscar modelos de atestados
    def buscar_modelo_atestado(self,atestadoID):
        conn = self.conectar_banco_dados()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ModelosAtestados WHERE ID=?", atestadoID)
        row = cursor.fetchone()
        if row:
            return row[1]
        conn.close()


class pdfScribo:
            
    # Função para gerar QR Code e salvar a imagem
    def gerar_qrcode(self,share_link,senha_leitura):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        share_link_senha = share_link + '/?_format=application/validador-iti+json&_secretCode='+senha_leitura
        qr.add_data(share_link_senha)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_path = "qrcode.png"
        img.save(img_path)
        return img_path

    # Função para gerar PDF e incluir QR Code no final

    def gerar_pdf(self, paciente, file_id, share_link, file_path, senha_leitura):
        # Caminho onde o PDF será salvo
        pdf_path = file_path
        c = canvas.Canvas(pdf_path, pagesize=A4)

        # Adicionar o Cabeçalho
        c.drawImage("Cabecalho.png", 40, 720, width=300, height=100)

        # Adicionar o texto da prescrição
        c.drawString(40, 680, f"Paciente : {paciente['nome']}")
        c.drawString(40, 665, f"CPF       : {paciente['cpf']}   Nascimento:  {paciente['nascimento']}")
        c.drawString(40, 650, f"Endereço : {paciente['endereco']}  {paciente['cidade']}")

        prescricao_texto = "P R E S C R I Ç Ã O"
        linha_inicial = 40
        linha_final = 500
        y_posicao_texto = 615  # Posição vertical do texto e da linha
        text_width = c.stringWidth(prescricao_texto, "Helvetica", 12)
        x_centralizado = (linha_final - linha_inicial - text_width) / 2 + linha_inicial
        c.drawString(x_centralizado, y_posicao_texto, prescricao_texto)

        text = c.beginText(40, 590)
        text.setFont("Helvetica", 12)
        text.textLines(paciente['prescricao'])
        c.drawText(text)

        # Gerar e adicionar QR Code
        qr_code_path = self.gerar_qrcode(share_link,senha_leitura)
        c.drawImage(qr_code_path, 40, 50, width=100, height=100)
        c.drawString(45, 48, f"ID: {file_id}")

        text.setFont("Helvetica", 9)
        c.drawString(140, 125, "Assinado digitalmente por : JOÃO AUGUSTO CAPELLARI - CRM 43918SP")
        c.drawString(140, 110, "Av. La Salle, 77 - Jardim Primavera, Araraquara - SP, 14802-384")
        c.drawString(140, 95, "Token : ")

        # Posição e tamanho do campo de assinatura
        x_signature = 140  # Posição X do canto inferior esquerdo do campo de assinatura
        y_signature = 70    # Posição Y do canto inferior esquerdo do campo de assinatura
        width_signature = 200  # Largura do campo de assinatura
        height_signature = 20   # Altura do campo de assinatura

        # Criar um campo de assinatura no PDF
        c.rect(x_signature, y_signature, width_signature, height_signature, stroke=1, fill=0)
        c.drawString(x_signature + 2, y_signature + 2, "Assinatura: ___________________")  # Linha para assinatura

        # Salvar o PDF
        c.save()

        # Agora vamos adicionar a senha para leitura usando PyPDF2
        # Abrir o PDF gerado
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()

            # Adicionar todas as páginas do PDF original ao novo PDF com senha
            for page in reader.pages:
                writer.add_page(page)

            # Adicionar senha de leitura
            writer.encrypt(user_password=senha_leitura)

            # Salvar o PDF com senha
            with open(pdf_path, "wb") as f_encrypted:
                writer.write(f_encrypted)

    

    # Função para assinar PDF com certificado A3 (PyHanko)
    def assinar_pdf(self):
        signer = signers.SimpleSigner.load_pkcs12("C:/Dados Gilberto/CertificadoDigital/certificate.p12", b"232404")
        with open("prescricao.pdf", "rb") as doc:
            pdf_out = signers.sign_pdf(doc, signer=signer)
        with open("prescricao_assinada.pdf", "wb") as f_out:
            f_out.write(pdf_out)

    def generate_initial_pdf(self,file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Este é o arquivo sem o QR code ainda.')
        
        # Salvar o PDF sem o QR code
        pdf.output(file_path)


    def gerar_pdf_controle_especial(self, paciente, file_id, share_link, file_path, senha_leitura):
        pdf_path = file_path
        c = canvas.Canvas(pdf_path, pagesize=A4)

        # Adicionar o Cabeçalho
        c.drawImage("Cabecalho.png", 40, 720, width=300, height=100)

        # Adicionar o texto da prescrição
        c.drawString(40, 680, f"Paciente : {paciente['nome']}")
        c.drawString(40, 665, f"CPF       : {paciente['cpf']}   Nascimento:  {paciente['nascimento']}")
        c.drawString(40, 650, f"Endereço : {paciente['endereco']}  {paciente['cidade']}")

        # Adicionar informações do emissor (Médico)
        c.rect(40, 525, 230, 80, stroke=1, fill=0)
        c.setFont("Helvetica", 10)
        c.drawString(45, 590, "Identificação do Emissor (Médico):")
        c.drawString(45, 575, "Nome: João Augusto Capelari")
        c.drawString(45, 560, "CRM : 43918SP")
        c.drawString(45, 545, "Endereço:Av. La Salle 77 Araraquara SP")
        c.drawString(45, 530, "Telefone: (16) 3335-2001")

        prescricao_texto = "R E C E I T U Á R I O    D E    C O N T R O L E    E S P E C I A L"
        linha_inicial = 40
        linha_final = 520
        y_posicao_texto = 615
        text_width = c.stringWidth(prescricao_texto, "Helvetica-Bold", 10)
        x_centralizado = (linha_final - linha_inicial - text_width) / 2 + linha_inicial
        c.drawString(x_centralizado, y_posicao_texto, prescricao_texto)

        # Detalhes do medicamento
        text = c.beginText(40, 490)
        text.setFont("Helvetica", 10)
        text.textLines(paciente['prescricao'])
        c.drawText(text)

        c.line(40, 240, 550, 240)
        # Adicionar informações do comprador (Paciente ou Representante)
        c.drawString(40, 225, "Identificação do Comprador:")
        c.drawString(40, 210, "Nome:____________________________________")
        c.drawString(40, 195, "CPF:_____________________________________")
        c.drawString(40, 180, "Endereço:_________________________________")
        c.drawString(40, 165, "Telefone:__________________________________")

        # Adicionar informações do fornecedor (Farmácia)
        c.drawString(340, 225, "Identificação do Fornecedor (Farmácia):")

        # Gerar e adicionar QR Code
        qr_code_path = self.gerar_qrcode(share_link,senha_leitura)
        c.drawImage(qr_code_path, 40, 50, width=100, height=100)
        c.drawString(47, 48, f"ID: {file_id}")

        c.setFont("Helvetica", 9)
        c.drawString(140, 125, "Assinado digitalmente por : JOÃO AUGUSTO CAPELLARI - CRM 43918SP")
        c.drawString(140, 110, "Av. La Salle, 77 - Jardim Primavera, Araraquara - SP, 14802-384")
        c.drawString(140, 95, "Token : ")

        # Posição e tamanho do campo de assinatura
        x_signature = 140
        y_signature = 70
        width_signature = 200
        height_signature = 20

        # Criar um campo de assinatura no PDF
        c.drawString(x_signature + 2, y_signature + 2, "Assinatura")

        # Salvar o PDF
        c.save()

        # Agora vamos adicionar a senha de leitura usando PyPDF2
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()

            # Copiar as páginas do PDF original para o novo PDF protegido
            for page in reader.pages:
                writer.add_page(page)

            # Definir a senha de leitura
            writer.encrypt(user_password=senha_leitura)

            # Salvar o novo PDF com senha
            with open(pdf_path, "wb") as f_encrypted:
                writer.write(f_encrypted)



